from django import forms
from django.test import TestCase

from apps.state_forms.fsm import ConditionalFSM
from apps.state_forms.states import BaseState


class TestState(BaseState):
    form = None
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
    step1a = TestState(exits_to=['step2', ])
    step1b = TestState(exits_to=['step2', ])
    step1c = TestState(exits_to=['step2[field1=baz]', 'end'])
    step2 = TestState(exits_to=['step3', 'end'])
    step3 = TestState(exits_to=['end', ])
    end = TestState()


class StateMachineTestsWithData(TestCase):
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
        m.state_data = {"start": {"field1": "bar"}, "step1c": {"field1": "baz"}}
        m.move_to_next()
        self.assertEqual(m.state.name, "step2")
        m.move_to_next()
        self.assertEqual(m.state.name, "step3")