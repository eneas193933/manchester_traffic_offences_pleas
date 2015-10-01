from __future__ import absolute_import

from apps.state_forms.states import StateWithForm
from apps.state_forms.fsm import FormBasedFSM
from . import forms


class PleaStates(StateWithForm):
    plea_index = 1

    def validate(self):
        if self.form_class is not None:
            if "pleas" not in self.my_data:
                self.my_data["pleas"] = [{"valid": False}]

            my_data = self.my_data["pleas"][self.plea_index-1]

            self.form = self.form_class(data=my_data)
            if self.form.is_valid():
                my_data["valid"] = True
                return True
            else:
                self.form = self.form_class(initial=my_data)

        return True

    def get_next(self):
        charge_count = self.all_data.get("plea", {}).get("number_of_charges", 1)
        if self.plea_index < charge_count:
            return self.name #TODO requires index :(
        else:
            return super(PleaStates, self).get_next()


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

        if post_data is None: post_data = {}
        save_data = {"valid": False}

        if self.form_class is not None:
            self.form = self.form_class(data=post_data)

            if self.form.is_valid():
                save_data = self.form.cleaned_data
                save_data["valid"] = True
        else:
            save_data = {"valid": True}

        self.my_data[self.plea_index] = save_data

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
                                    exits_to=["company_plea_1"])
    company_plea = PleaStates(template="plea.html",
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
                                             "company_plea_1",
                                             "company_finances",
                                             "company_complete"])
    company_complete = StateWithForm(template="complete.html")

    # Defendant path
    defendant_details = StateWithForm(template="your_details.html",
                                      label="Your details",
                                      form_class=forms.YourDetailsForm,
                                      exits_to=["defendant_plea_1"])
    defendant_plea = PleaStates(template="plea.html",
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
                                               "defendant_plea_1",
                                               "defendant_finances",
                                               "defendant_complete"])
    defendant_complete = StateWithForm(template="complete.html")
