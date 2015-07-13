from django.test import TestCase

import ex
from fsm import FSM
from states import BaseState


class TestMachine(FSM):
    start = BaseState(exits_to=['step1a', 'step1b', 'step1c'])
    step1a = BaseState(exits_to=['step2', ])
    step1b = BaseState(exits_to=['step2', ])
    step1c = BaseState(exits_to=['step2', 'end'])
    step2 = BaseState(exits_to=['end', 'step3', ])
    step3 = BaseState(exits_to=['end', ])
    end = BaseState()


class StateMachineTests(TestCase):
    def test_verify(self):
        """ Should raise a FSM_VerificationError """
        testmachine = TestMachine()
        testmachine.states["random"] = (BaseState("random", [
            "doesntexist", "alsodoesnexist"]))
        with self.assertRaises(ex.VerificationError):
            testmachine.verify()

    def test_save_fail(self):
        """Should raise a StateMachineNotAllowed, messing with the
        state outside of the machine.

        """
        testmachine = TestMachine()

        with self.assertRaises(ex.TransitionNotAllowed):
            testmachine.state = "Testing"

    def test_full_transition(self):
        """ End to end smoke test of the transitions """
        testmachine = TestMachine()
        testmachine.change("step1a")
        testmachine.change("step2")
        #reload to check state is saved and reinstated
        self.assertEqual(testmachine.state.name, "step2")
        testmachine.change("step3")
        testmachine.change("end")

    def test_invalid_transition(self):
        """ Testing invalid transitions """
        testmachine = TestMachine()
        # check we are starting at "start"
        self.assertEqual(testmachine.state.name, "start")

        with self.assertRaises(ex.TransitionNotAllowed):
            testmachine.change("step3")

        # check we are still at "start" after a failed transition
        self.assertEqual(testmachine.state.name, "start")

    def test_entry_action(self):
        """ Tests an action set to run on entry to a state """
        def entry_func(entered, row):
            row.field1 = 500
        testmachine = TestMachine()
        testmachine.states["step3"].entry_action = entry_func
        testmachine.change("step1a")
        testmachine.change("step2")
        testmachine.change("step3", testmachine)
        self.assertEqual(testmachine.field1, 500)

    def test_exit_action(self):
        """ Tests an action set to run on entry to a state """
        def exit_func(entered, row):
            row.field1 = 10
            row.field2 = "Chickens"

        testmachine = TestMachine()
        testmachine.states["start"].exit_action = exit_func
        testmachine.change("step1a", testmachine)

        self.assertEqual(testmachine.field1, 10)
        self.assertEqual(testmachine.field2, "Chickens")

    def test_cancel_action(self):
        def cancel_change(from_state):
            if from_state.name == "step1c":
                raise ex.CancelTransition("Didn't want to continue")

        testmachine = TestMachine()
        testmachine.states["step2"].entry_action = cancel_change
        testmachine.change("step1c")
        testmachine.change("step2")

        self.assertEqual(testmachine.state.name, "step1c")

        testmachine2 = TestMachine()
        testmachine.states["step2"].exit_action = cancel_change
        testmachine2.change("step1b")
        testmachine2.change("step2")

        self.assertEqual(testmachine2.state.name, "step2")

    def test_redirect_action(self):
        def redirect_change(from_state):
            if from_state.name == "step1c":
                raise ex.RedirectTransition(testmachine.states["end"])

        testmachine = TestMachine()
        testmachine.states["step2"].entry_action = redirect_change
        testmachine.change("step1c")
        testmachine.change("step2")

        self.assertEqual(testmachine.state.name, "end")