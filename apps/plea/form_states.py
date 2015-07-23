from __future__ import absolute_import

from apps.state_forms.states import BaseState
from apps.state_forms.fsm import ConditionalFSM
from . import forms


class PleaState(BaseState):
    template = "base.html"
    form = None


class PleaStates(ConditionalFSM):
    case_stage = PleaState(template="plea/case.html",
                           form=forms.CaseForm,
                           exits_to=["defendant_details[plea_made_by=Defendant]",
                                     "company_details"])
    # Company path
    company_details = PleaState(template="company_details.html",
                                form=forms.CompanyDetailsForm,
                                exits_to=["company_plea"])
    company_plea = PleaState(template="plea/plea.html",
                             form=forms.PleaForm,
                             exits_to=["company_finances[none_guilty=True]",
                                       "company_review"])
    company_finances = PleaState(template="plea/company_finances.html",
                                 form=forms.CompanyFinancesForm,
                                 exits_to=["company_review"])
    company_review = PleaState(template="plea/review.html",
                               form=forms.ConfirmationForm,
                               exits_to=["company_details",
                                         "company_plea",
                                         "company_finances",
                                         "company_complete"])
    company_complete = PleaState(template="plea/complete.html")

    # Defendant path
    defendant_details = PleaState(template="plea/your_details.html",
                                  form=forms.YourDetailsForm,
                                  exits_to=["defendant_plea"])
    defendant_plea = PleaState(template="plea/plea.html",
                               form=forms.PleaForm,
                               exits_to=["defendant_finances[none_guilty=True]",
                                         "defendant_review"])
    defendant_finances = PleaState(template="plea/your_finances.html",
                                   form=forms.YourMoneyForm,
                                   exits_to=["defendant_expenses[hardship=True]",
                                             "defendant_review"])
    defendant_expenses = PleaState(template="plea/your_expenses.html",
                                   form=forms.YourExpensesForm,
                                   exits_to=["defendant_review"])
    defendant_review = PleaState(template="plea/review.html",
                                 form=forms.ConfirmationForm,
                                 exits_to=["defendant_details",
                                           "defendant_plea",
                                           "defendant_finances",
                                           "defendant_complete"])
    defendant_complete = PleaState(template="plea/complete.html")
