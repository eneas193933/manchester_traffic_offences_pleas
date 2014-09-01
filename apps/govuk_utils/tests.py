from datetime import datetime, date
from mock import patch

from django import forms
from django.forms.formsets import formset_factory
from django.http import Http404
from django.test import TestCase
from .forms import MultiStageForm, FormStage
from .serializers import DateAwareSerializer


def reverse(url_name, args=None):
    return "/path/to/" + url_name + "/" + args[0]


class TestForm1(forms.Form):
    field1 = forms.CharField()
    field2 = forms.IntegerField()


class TestForm2(forms.Form):
    field3 = forms.CharField()
    field4 = forms.EmailField()


class TestForm3(forms.Form):
    field5 = forms.BooleanField()


class Intro(FormStage):
    name = "intro"
    template = "test/intro.html"
    form_classes = []


class Stage2(FormStage):
    name = "stage_2"
    template = "test/stage2.html"
    form_classes = [TestForm1, ]


class Stage3(FormStage):
    name = "stage_3"
    template = "test/stage3.html"
    form_classes = [TestForm3, TestForm2]

    def load_forms(self, data=None, initial=False):
        count = self.all_data["stage_2"].get("field2", 1)

        TestForm2Factory = formset_factory(TestForm2, extra=count)
        if initial:
            initial_factory_data = self.all_data[self.name].get("Factory", [])
            initial_form_data = self.all_data[self.name]
            self.forms.append(TestForm2Factory(initial=initial_factory_data))
            self.forms.append(TestForm3(initial=initial_form_data))
        else:
            self.forms.append(TestForm2Factory(data))
            self.forms.append(TestForm3(data))

    def save_forms(self):
        form_data = {}

        for form in self.forms:
            if hasattr(form, "management_form"):
                form_data["Factory"] = form.cleaned_data
            else:
                form_data.update(form.cleaned_data)

        return form_data


class Review(FormStage):
    name = "review"
    template = "test/review.html"
    form_classes = []


class MultiStageFormTest(MultiStageForm):
    stage_classes = [Intro, Stage2, Stage3, Review]


class TestMultiStageForm(TestCase):
    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_404_raised_if_no_stage(self):
        with self.assertRaises(Http404):
            msf = MultiStageFormTest("Rabbits", "msf-url", {})

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_form_intro_loads(self):
        request_context = {}
        msf = MultiStageFormTest("intro", "msf-url", {})
        response = msf.load(request_context)

        self.assertContains(response, "<h1>Test intro page</h1>")

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_form_stage2_loads(self):
        request_context = {}
        msf = MultiStageFormTest("stage_2", "msf-url", {})
        response = msf.load(request_context)
        self.assertContains(response, "id_field1")
        self.assertContains(response, "id_field2")

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_form_stage2_saves(self):
        request_context = {}
        msf = MultiStageFormTest("stage_2", "msf-url", {})
        msf.load(request_context)
        response = msf.save({"field1": "Joe",
                             "field2": 10},
                            request_context)

        self.assertEqual(msf.all_data["stage_2"]["field1"], "Joe")
        self.assertEqual(msf.all_data["stage_2"]["field2"], 10)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response._headers['location'][1],
                         "/path/to/msf-url/stage_3")

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_form_stage3_loads(self):
        request_context = {}
        msf = MultiStageFormTest("stage_3", "msf-url", {})
        msf.all_data["stage_2"]["field2"] = 2
        response = msf.load(request_context)
        self.assertContains(response, "id_field5")
        self.assertContains(response, "id_form-0-field3")
        self.assertContains(response, "id_form-0-field4")
        self.assertContains(response, "id_form-1-field3")
        self.assertContains(response, "id_form-1-field4")

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_form_stage3_saves(self):
        request_context = {}
        msf = MultiStageFormTest("stage_3", "msf_url", {})
        msf.all_data["field2"] = 2
        mgmt_data = {"form-TOTAL_FORMS": "2",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}
        form_data = {"form-0-field3": "Jim Smith",
                     "form-0-field4": "jim.smith@example.org",
                     "form-1-field3": "Jill Smith",
                     "form-1-field4": "jill.smith@example.org",
                     "field5": True}
        form_data.update(mgmt_data)
        response = msf.save(form_data, request_context)

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_form_review_loads(self):
        request_context = {}
        msf = MultiStageFormTest("review", "msf-url", {})
        response = msf.load(request_context)
        self.assertContains(response, "<h1>Review</h1>")

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_save_doesnt_blank_storage_dict_and_nothing_is_added(self):
        request_context = {}
        fake_storage = {"extra": {"field0": "Not on the form"}}
        msf = MultiStageFormTest("intro",  "msf_url", fake_storage)
        msf.load(request_context)
        msf.save({}, request_context)
        self.assertTrue(fake_storage["extra"]["field0"], "Not on the form")
        self.assertEqual(len(fake_storage["extra"]), 1)

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_save_data_persists_between_stages(self):
        request_context = {}
        fake_storage = {}
        msf = MultiStageFormTest("stage_2", "msf_url", fake_storage)
        msf.load(request_context)

        response = msf.save({"field1": "Joe",
                             "field2": 2},
                            request_context)

        msf = MultiStageFormTest("stage_3", "msf_url", fake_storage)
        mgmt_data = {"form-TOTAL_FORMS": "2",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}
        form_data = {"form-0-field3": "Jim Smith",
                     "form-0-field4": "jim.smith@example.org",
                     "form-1-field3": "Jill Smith",
                     "form-1-field4": "jill.smith@example.org",
                     "field5": True}
        form_data.update(mgmt_data)
        response = msf.save(form_data, request_context)

        self.assertEqual(fake_storage["stage_2"]["field1"], "Joe")
        self.assertEqual(fake_storage["stage_2"]["field2"], 2)
        self.assertEqual(fake_storage["stage_3"]["Factory"][0]["field3"], "Jim Smith")
        self.assertEqual(fake_storage["stage_3"]["Factory"][0]["field4"], "jim.smith@example.org")
        self.assertEqual(fake_storage["stage_3"]["Factory"][1]["field3"], "Jill Smith")
        self.assertEqual(fake_storage["stage_3"]["Factory"][1]["field4"], "jill.smith@example.org")

    @patch("apps.govuk_utils.forms.reverse", reverse)
    def test_stage_standard_single_form_validation(self):
        request_context = {}
        msf = MultiStageFormTest("stage_2", "msf-url", {})
        msf.load(request_context)
        response = msf.save({"field1": "",
                             "field2": "This is not an integer"},
                            request_context)

        # check it doesn't redirect
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a whole number")
        self.assertContains(response, "This field is required")


class DateAwareSerializerTests(TestCase):
    def test_serializer_dumps_plain(self):
        test_str = """{"key2": 2, "key1": "value1"}"""
        test_dict = {"key1": "value1",
                     "key2": 2}

        ds = DateAwareSerializer().dumps(test_dict)
        self.assertEqual(ds, test_str)

    def test_serializer_loads_plain(self):
        test_str = """{"key2": 2, "key1": "value1"}"""
        test_dict = {"key1": "value1",
                     "key2": 2}

        ds = DateAwareSerializer().loads(test_str)
        self.assertEqual(ds, test_dict)

    def test_serializer_dumps_datetime(self):
        test_str = """{"key2": "2014-06-03T00:00:00", "key1": "value1"}"""
        test_dict = {"key1": "value1",
                     "key2": datetime(2014, 6, 3, 0, 0)}

        ds = DateAwareSerializer().dumps(test_dict)
        self.assertEqual(ds, test_str)
