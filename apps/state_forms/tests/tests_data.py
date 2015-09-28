from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.govuk_utils.fields import DateWidget
from apps.plea.validators import is_date_in_future, is_date_within_range
from apps.state_forms.fsm import FormBasedFSM
from apps.state_forms.states import StateWithForm




class TestState(StateWithForm):
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


class DateForm(forms.Form):
    date_field = forms.DateField(widget=DateWidget,
                                      validators=[is_date_in_future, is_date_within_range],
                                      required=True)


class TestMachine(FormBasedFSM):
    start = TestState(exits_to=["step1"])
    step1 = TestState(exits_to=['step1a[field1=foo]', 'step1b[field1=bar]', 'step1c'],
                      form_class=Form1a)
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


class DateTestMachine(FormBasedFSM):
    start = TestState(exits_to=["step1"])
    step1 = TestState(exits_to=["end"],
                      form_class=DateForm)
    end = TestState()


class StateMachineTestsWithData(TestCase):
    def test_start_at_the_start(self):
        sm = TestMachine({"start": {}})
        sm.init("start")
        self.assertEqual(sm.state.name, "start")

    def test_skips_start(self):
        state_data = {"start": {"valid": True}}
        sm = TestMachine(state_data)
        sm.init("step1")
        self.assertEqual(sm.state.name, "step1")

    def test_successful_save(self):
        state_data = {"start": {"valid": True}}
        sm = TestMachine(state_data)
        sm.init("step1")
        data = sm.move({"field1": "foo", "field2": "fee"})

        self.assertEqual(data["valid"], True)
        self.assertEqual(sm.state.name, "step1a")
        self.assertEqual(sm.state_data["step1"]["field1"], "foo")
        self.assertEqual(sm.state_data["step1"]["field2"], "fee")
        self.assertEqual(sm.state_data["step1"]["valid"], True)

    def test_get_to_the_end(self):
        state_data = {}
        sm = TestMachine(state_data)
        sm.init("start")
        self.assertEqual(sm.state.name, "start")
        sm.move({})
        self.assertEqual(sm.state.name, "step1")
        data = sm.move({"field1": "foo", "field2": "fee"})
        self.assertEqual(sm.state.name, "step1a")
        data = sm.move({"field1": "test", "field2": "taste"})
        self.assertEqual(sm.state.name, "step2")
        data = sm.move({"field1": "bahh"})
        self.assertEqual(sm.state.name, "step3")
        data = sm.move({"field1": True})
        self.assertEqual(sm.state.name, "end")
        data = sm.move({"field1": True})
        self.assertEqual(sm.state.name, "end")


class StateMachineRegressions(TestCase):
    def test_dates_saved_into_session(self):
        sm = DateTestMachine({"start": {"valid": True},
                              "step1": {"date_field_0": 1, "date_field_1": 12, "date_field_2": 2015}})
        sm.init("end")
        self.assertEqual(sm.state.name, "end")



