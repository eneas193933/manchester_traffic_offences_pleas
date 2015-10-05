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

    def get_case_data(self, override=None):
        hearing_date = datetime.date.today()+datetime.timedelta(30)
        case_data = {"date_of_hearing": str(hearing_date),
                     "urn": "06/AA/000000000",
                     "number_of_charges": 3,
                     "plea_made_by": "Defendant"}
        case_data.update(override or {})
        return case_data

    def get_defendant_details(self, override=None):
        details = {"first_name": "Joe",
                   "last_name": "Bloggs",
                   "correct_address": True,
                   "contact_number": "0161 800 9000",
                   "date_of_birth": datetime.date(1970, 1, 1)}
        details.update(override or {})
        return details

    def get_defendant_plea(self, override=None):
        return {}

    def test_start_at_the_start(self):
        m = PleaStates({})
        self.assertEqual(m.state.name, "case")

    def test_use_defendant_path(self):
        m = PleaStates(state_data={"case": self.get_case_data()})
        m.init("defendant_details")
        print "E:", m.state.form.errors
        self.assertEqual(m.state.name, "defendant_details")

    def txest_use_company_path(self):
        m = PleaStates(state_data={"case": self.get_case_data({"plea_made_by": "Company representative"})})
        m.init("company_details")
        self.assertEqual(m.state.name, "company_details")

    def txest_defendant_details_path(self):
        m = PleaStates(state_data={"case": self.get_case_data(),
                                   "defendant_details": self.get_defendant_details()})
        m.init("defendant_plea", 1)
        self.assertEqual(m.state.name, "defendant_plea")
        self.assertEqual(m.state.plea_index, 1)

    def txest_defendant_details_2_path(self):
        m = PleaStates(state_data={"case": self.get_case_data(),
                                   "defendant_details": self.get_defendant_details(),
                                   "defendant_plea": {"data": [self.get_defendant_plea()]}})
        m.init("defendant_plea", 2)
        self.assertEqual(m.state.name, "defendant_plea")
        self.assertEqual(m.state.plea_index, 2)
