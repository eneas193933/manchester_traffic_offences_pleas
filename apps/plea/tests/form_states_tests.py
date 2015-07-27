import datetime

from django.test import TestCase

from apps.plea.form_states import PleaStates
from apps.plea.models import Court

class StateMachineTestsWithData(TestCase):
    def setUp(self):
        self.court = Court.objects.create(
            court_code="0000",
            region_code="06",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="test@test.com",
            submission_email=True,
            plp_email="test@test.com",
            enabled=True,
            test_mode=False)

    def get_good_case_data(self, override=None):
        hearing_date = datetime.date.today()+datetime.timedelta(30)
        case_data = {"date_of_hearing_0": str(hearing_date.day),
                     "date_of_hearing_1": str(hearing_date.month),
                     "date_of_hearing_2": str(hearing_date.year),
                     "urn_0": "06",
                     "urn_1": "AA",
                     "urn_2": "0000000",
                     "urn_3": "00",
                     "number_of_charges": 3,
                     "plea_made_by": "Defendant"}
        case_data.update(override or {})
        return case_data

    def test_start_at_the_start(self):
        m = PleaStates({})
        self.assertEqual(m.state.name, "case_stage")

    def test_use_defendant_path(self):
        m = PleaStates(state_data={"case_stage": self.get_good_case_data()})
        m.move_to_next()
        self.assertEqual(m.state.name, "defendant_details")

    def test_use_company_path(self):
        m = PleaStates(state_data={"case_stage": self.get_good_case_data({"plea_made_by": "Company representative"})})
        m.move_to_next()
        self.assertEqual(m.state.name, "company_details")