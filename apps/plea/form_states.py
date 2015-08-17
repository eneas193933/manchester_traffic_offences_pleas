from __future__ import absolute_import

from apps.state_forms.states import StateWithData
from apps.state_forms.fsm import ConditionalFSM
from . import forms


class PleaState(StateWithData):
    pass


class PleaStates(ConditionalFSM):
    case_stage = PleaState(template="case.html",
                           form_class=forms.CaseForm,
                           exits_to=["defendant_details[plea_made_by=Defendant]",
                                     "company_details"])
    # Company path
    company_details = PleaState(template="company_details.html",
                                form_class=forms.CompanyDetailsForm,
                                exits_to=["company_plea"])
    company_plea = PleaState(template="plea.html",
                             form_class=forms.PleaForm,
                             exits_to=["company_finances[none_guilty=True]",
                                       "company_review"])
    company_finances = PleaState(template="company_finances.html",
                                 form_class=forms.CompanyFinancesForm,
                                 exits_to=["company_review"])
    company_review = PleaState(template="review.html",
                               form_class=forms.ConfirmationForm,
                               exits_to=["company_details",
                                         "company_plea",
                                         "company_finances",
                                         "company_complete"])
    company_complete = PleaState(template="complete.html")

    # Defendant path
    defendant_details = PleaState(template="your_details.html",
                                  form_class=forms.YourDetailsForm,
                                  exits_to=["defendant_plea"])
    defendant_plea = PleaState(template="plea.html",
                               form_class=forms.PleaForm,
                               exits_to=["defendant_finances[none_guilty=True]",
                                         "defendant_review"])
    defendant_finances = PleaState(template="your_finances.html",
                                   form_class=forms.YourMoneyForm,
                                   exits_to=["defendant_expenses[hardship=True]",
                                             "defendant_review"])
    defendant_expenses = PleaState(template="your_expenses.html",
                                   form_class=forms.YourExpensesForm,
                                   exits_to=["defendant_review"])
    defendant_review = PleaState(template="review.html",
                                 form_class=forms.ConfirmationForm,
                                 exits_to=["defendant_details",
                                           "defendant_plea",
                                           "defendant_finances",
                                           "defendant_complete"])
    defendant_complete = PleaState(template="complete.html")
