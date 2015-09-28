from __future__ import absolute_import

from apps.state_forms.states import StateWithForm
from apps.state_forms.fsm import FormBasedFSM
from . import forms


class PleaStates(FormBasedFSM):
    def _init_states(self ):
        charge_count = self.state_data.get("case", {}).get("number_of_charges", 0)
        if charge_count > 0:
            self.add_plea_states(charge_count)

    def add_state(self, name, state):
        state.name = name
        self.states[name] = state

    def add_plea_states(self, count):
        for i in range(1, count+1):
            if i < count:
                self.add_state("company_plea_{}".format(i), StateWithForm(template="plea.html",
                                                                          form_class=forms.PleaForm,
                                                                          exits_to=["company_plea_{}".format(i+1)]))
                self.add_state("defendant_plea_{}".format(i), StateWithForm(template="plea.html",
                                                                            form_class=forms.PleaForm,
                                                                            exits_to=["defendant_plea_{}".format(i+1)]))
            else:
                self.add_state("company_plea_{}".format(i), StateWithForm(template="plea.html",
                                                                          form_class=forms.PleaForm,
                                                                          exits_to=["company_finances[none_guilty=True]",
                                                                                    "company_review"]))
                self.add_state("defendant_plea_{}".format(i), StateWithForm(template="plea.html",
                                                                            form_class=forms.PleaForm,
                                                                            exits_to=["defendant_finances[none_guilty=True]",
                                                                                      "defendant_review"]))


    case = StateWithForm(template="case.html",
                         form_class=forms.CaseForm,
                         exits_to=["defendant_details[plea_made_by=Defendant]",
                                   "company_details"])
    # Company path
    company_details = StateWithForm(template="company_details.html",
                                    form_class=forms.CompanyDetailsForm,
                                    exits_to=["company_plea_1"])
    company_plea_1 = StateWithForm(template="plea.html",
                                   form_class=forms.PleaForm,
                                   exits_to=["company_finances[none_guilty=True]",
                                             "company_review"])
    company_finances = StateWithForm(template="company_finances.html",
                                     form_class=forms.CompanyFinancesForm,
                                     exits_to=["company_review"])
    company_review = StateWithForm(template="review.html",
                                   form_class=forms.ConfirmationForm,
                                   exits_to=["company_details",
                                             "company_plea_1",
                                             "company_finances",
                                             "company_complete"])
    company_complete = StateWithForm(template="complete.html")

    # Defendant path
    defendant_details = StateWithForm(template="your_details.html",
                                      form_class=forms.YourDetailsForm,
                                      exits_to=["defendant_plea_1"])
    defendant_plea_1 = StateWithForm(template="plea.html",
                                     form_class=forms.PleaForm,
                                     exits_to=["defendant_finances[none_guilty=True]",
                                               "defendant_review"])
    defendant_finances = StateWithForm(template="your_finances.html",
                                       form_class=forms.YourMoneyForm,
                                       exits_to=["defendant_expenses[hardship=True]",
                                                 "defendant_review"])
    defendant_expenses = StateWithForm(template="your_expenses.html",
                                       form_class=forms.YourExpensesForm,
                                       exits_to=["defendant_review"])
    defendant_review = StateWithForm(template="review.html",
                                     form_class=forms.ConfirmationForm,
                                     exits_to=["defendant_details",
                                               "defendant_plea_1",
                                               "defendant_finances",
                                               "defendant_complete"])
    defendant_complete = StateWithForm(template="complete.html")
