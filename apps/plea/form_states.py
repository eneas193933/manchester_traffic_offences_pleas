from __future__ import absolute_import

from django.core.urlresolvers import reverse

from apps.state_forms.states import StateWithForm
from apps.state_forms.fsm import FormBasedFSM
from . import forms


class PleaIndexState(StateWithForm):
    plea_index = 1

    def get_url(self):
        return reverse("state_form_step", kwargs={"state": self.name})

    @property
    def my_data(self):
        if self.name not in self.all_data:
            self.all_data[self.name] = {"data": [{}]}

        if len(self.all_data[self.name]["data"]) < self.plea_index:
            self.all_data[self.name]["data"].append({"valid": False})

        return self.all_data[self.name]["data"][self.plea_index-1]

    def get_next(self):
        charge_count = self.all_data.get("case", {}).get("number_of_charges", 1)
        if self.plea_index < charge_count:
            self.plea_index += 1
            return self
        else:
            return super(PleaIndexState, self).get_next()

    def validate(self):
        if self.form_class is not None:
            self.form = self.form_class(data=self.my_data)
            if self.form.is_valid():
                self.my_data["valid"] = True
                return True
            else:
                return False

        return True

    def load(self):
        """
        Loads the state, returns a form with initial set to the data
        stored in the key in self.data for this state. If form_class
        is None then None is returned.

        :return: form
        """
        if self.form_class is not None:
            self.form = self.form_class(initial=self.my_data[self.plea_index])

    def save(self, post_data=None, count=None):
        """
        Validates the form with post_data and returns the data with
        valid=True set.

        :param post_data: a dict containing values to validate
        :return: the validated data or None if invalid
        """

        if post_data is None:
            post_data = {}

        save_data = {"valid": False}

        if self.form_class is not None:
            self.form = self.form_class(data=post_data)

            if self.form.is_valid():
                save_data = self.form.cleaned_data
                save_data["valid"] = True
        else:
            save_data = {"valid": True}

        self.my_data["data"][self.plea_index] = save_data

        self.my_data["none_guilty"] = True

        for plea in self.my_data:
            if plea["plea"] == "Guilty":
                self.my_data["none_guilty"] = False

        return self.my_data


class PleaStates(FormBasedFSM):
    case = StateWithForm(template="case.html",
                         label="Case details",
                         form_class=forms.CaseForm,
                         exits_to=["defendant_details[plea_made_by=Defendant]",
                                   "company_details"])

    # Company path
    company_details = StateWithForm(template="company_details.html",
                                    label="Company details",
                                    form_class=forms.CompanyDetailsForm,
                                    exits_to=["company_plea"])
    company_plea = PleaIndexState(template="plea.html",
                                  label="Your plea",
                                  form_class=forms.PleaForm,
                                  exits_to=["company_finances[none_guilty=True]",
                                            "company_review"])
    company_finances = StateWithForm(template="company_finances.html",
                                     label="Your finances",
                                     form_class=forms.CompanyFinancesForm,
                                     exits_to=["company_review"])
    company_review = StateWithForm(template="review.html",
                                   label="Review",
                                   form_class=forms.ConfirmationForm,
                                   exits_to=["company_details",
                                             "company_plea",
                                             "company_finances",
                                             "company_complete"])
    company_complete = StateWithForm(template="complete.html")

    # Defendant path
    defendant_details = StateWithForm(template="your_details.html",
                                      label="Your details",
                                      form_class=forms.YourDetailsForm,
                                      exits_to=["defendant_plea"])
    defendant_plea = PleaIndexState(template="plea.html",
                                label="Your plea",
                                form_class=forms.PleaForm,
                                exits_to=["defendant_finances[none_guilty=True]",
                                          "defendant_review"])
    defendant_finances = StateWithForm(template="your_finances.html",
                                       label="Your finances",
                                       form_class=forms.YourMoneyForm,
                                       exits_to=["defendant_expenses[hardship=True]",
                                                 "defendant_review"])
    defendant_expenses = StateWithForm(template="your_expenses.html",
                                       label="Your expenses",
                                       form_class=forms.YourExpensesForm,
                                       exits_to=["defendant_review"])
    defendant_review = StateWithForm(template="review.html",
                                     label="Review",
                                     form_class=forms.ConfirmationForm,
                                     exits_to=["defendant_details",
                                               "defendant_plea",
                                               "defendant_finances",
                                               "defendant_complete"])
    defendant_complete = StateWithForm(template="complete.html")
