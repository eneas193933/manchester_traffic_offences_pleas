from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.state_forms.fsm import ConditionalFSM
from apps.state_forms.states import StateWithData


class TestState(StateWithData):
    form_class = None
    template = "base.html"


class Form1a(forms.Form):
    field1 = forms.CharField(max_length=10, required=True)
    field2 = forms.CharField(max_length=10, required=False)


class Form1b(forms.Form):
    field1 = forms.CharField(max_length=10, required=True)
    field2 = forms.CharField(max_length=10, required=False)


class Form1c(forms.Form):
    field1 = forms.CharField(max_length=10, required=True)
    field2 = forms.CharField(max_length=10, required=False)


class Form2(forms.Form):
    field1 = forms.CharField(max_length=10, required=True)
    field2 = forms.CharField(max_length=10, required=False)


class Form3(forms.Form):
    field1 = forms.BooleanField(required=True)


class TestMachine(ConditionalFSM):
    start = TestState(exits_to=['step1a[field1=foo]', 'step1b[field1=bar]', 'step1c'])
    step1a = TestState(exits_to=['step2', ],
                       form_class=Form1a)
    step1b = TestState(exits_to=['step2', ],
                       form_class=Form1b)
    step1c = TestState(exits_to=['step2[field1=baz]', 'end'],
                       form_class=Form1c)
    step2 = TestState(exits_to=['step3', 'end'],
                       form_class=Form2)
    step3 = TestState(exits_to=['end', ],
                       form_class=Form3)
    end = TestState()


class StateMachineTestsWithData(TestCase):
    def test_start_at_the_start(self):
        m = TestMachine({})
        self.assertEqual(m.state.name, "start")

    def test_what_happens_at_the_end(self):
        m = TestMachine({"start": {},
                         "step1c": {"field1": "foo foo", "field2": "bar bar"}})
        self.assertEqual(m.state.name, "start")
        m.move_to_next()
        self.assertEqual(m.state.name, "step1c")
        m.move_to_next()
        self.assertEqual(m.state.name, "end")
        m.move_to_next()
        self.assertEqual(m.state.name, "end")

    def test_default_path_no_data(self):
        m = TestMachine({})
        self.assertEqual(m.state.name, "start")
        m.move_to_next()
        m.move_to_next()
        self.assertEqual(m.state.name, "step1c")

    def test_default_path_with_data(self):
        m = TestMachine({"start": {},
                         "step1c": {"field1": "foo", "field2": "bar"},
                         "end": {"field1": True}})

        self.assertEqual(m.state.name, "start")
        m.move_to_next()
        self.assertEqual(m.state.name, "step1c")
        m.move_to_next()
        self.assertEqual(m.state.name, "end")

    def test_condition_field1_foo(self):
        m = TestMachine(state_data={"start": {"field1": "foo"}})
        self.assertEqual(m.state.name, "start")
        m.move_to_next()
        self.assertEqual(m.state.name, "step1a")

    def test_condition_field1_bar(self):
        m = TestMachine(state_data={"start": {"field1": "bar"}})
        self.assertEqual(m.state.name, "start")
        m.move_to_next()
        self.assertEqual(m.state.name, "step1b")

    def test_condition_field1_baz(self):
        m = TestMachine({})
        self.assertEqual(m.state.name, "start")
        m.move_to_next()
        self.assertEqual(m.state.name, "step1c")
        m.state_data = {"start": {"field1": "bar"},
                        "step1c": {"field1": "baz"},
                        "step2": {"field1": "baz", "field2": "alice"}}
        m.move_to_next()
        self.assertEqual(m.state.name, "step2")
        m.move_to_next()
        self.assertEqual(m.state.name, "step3")