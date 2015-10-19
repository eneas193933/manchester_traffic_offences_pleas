from django.utils.translation import ugettext_lazy as _

ERROR_MESSAGES = {
    "NOTICE_TYPE_REQUIRED": _("Tell us if the notice has the words 'Single Justice Procedure Notice' written at the top"),
    "URN_REQUIRED": _("Enter your unique reference number (URN)"),
    "URN_INVALID": _("The unique reference number (URN) isn't valid. Enter the number exactly as it appears on page 1 of the notice"),
    "URN_ALREADY_USED": _("Enter the correct URN"),
    "URN_INCORRECT": _("You've entered incorrect details"),
    "HEARING_DATE_REQUIRED": _("Provide a court hearing date"),
    "HEARING_DATE_INVALID": _("The court hearing date isn't a valid format"),
    "HEARING_DATE_PASSED": _("The court hearing date must be after today"),
    "HEARING_DATE_INCORRECT": _("Enter the correct hearing date"),
    "POSTING_DATE_REQUIRED": _("Provide a posting date"),
    "POSTING_DATE_INVALID": _("The posting date isn't a valid format"),
    "POSTING_DATE_IN_FUTURE": _("The posting date must be before today"),
    "POSTING_DATE_INCORRECT": _("Enter the correct posting date"),
    "NUMBER_OF_CHARGES_REQUIRED": _("Select the number of charges against you"),
    "PLEA_MADE_BY_REQUIRED": _("You must tell us if you are the person named in the notice or pleading on behalf of a company"),
    "FIRST_NAME_REQUIRED": _("Enter your first name"),
    "LAST_NAME_REQUIRED": _("Enter your last name"),
    "CORRECT_ADDRESS_REQUIRED": _("You must tell us if the address on the notice we sent to you is correct"),
    "UPDATED_ADDRESS_REQUIRED": _("Enter your correct address"),
    "COMPANY_CORRECT_ADDRESS_REQUIRED": _("Tell us if the company's address, as it's written on the notice, is correct"),
    "COMPANY_UPDATED_ADDRESS_REQUIRED": _("Enter the correct company address"),
    "EMAIL_ADDRESS_REQUIRED": _("You must provide an email address"),
    "EMAIL_ADDRESS_INVALID": _("Email address isn't a valid format"),
    "CONTACT_NUMBER_REQUIRED": _("You must provide a contact number"),
    "CONTACT_NUMBER_INVALID": _("The contact number isn't a valid format"),
    "DATE_OF_BIRTH_REQUIRED": _("Tell us your date of birth"),
    "DATE_OF_BIRTH_INVALID": _("The date of birth isn't a valid format"),
    "DATE_OF_BIRTH_IN_FUTURE": _("The date of birth must be before today"),
    "HAVE_NI_NUMBER_REQUIRED": _("Tell us if you have a National Insurance number"),
    "NI_NUMBER_REQUIRED": _("Tell us your National Insurance number"),
    "HAVE_DRIVING_LICENCE_NUMBER_REQUIRED": _("Tell us if you have a UK driving licence"),
    "DRIVING_LICENCE_NUMBER_REQUIRED": _("Tell us your driving licence number"),
    "COMPANY_NAME_REQUIRED": _("Enter the company name"),
    "POSITION_REQUIRED": _("You must tell us your position in the company"),
    "COMPANY_CONTACT_NUMBER_REQUIRED": _("Enter a contact number"),
    "PLEA_REQUIRED": _("You must select a plea for this charge"),
    "COME_TO_COURT_REQUIRED": _("You must tell us if you want to come to court to plead guilty"),
    "NOT_GUILTY_REQUIRED": _("Tell us why you believe you are not guilty"),
    "INTERPRETER_NEEDED_REQUIRED": _("You must tell us if you need an interpreter in court"),
    "INTERPRETER_LANGUAGE_REQUIRED": _("You must tell us which language"),
    "DISAGREE_WITH_EVIDENCE_REQUIRED": _("Tell us if you disagree with any of the evidence we sent to you"),
    "DISAGREE_WITH_EVIDENCE_DETAILS_REQUIRED": _("You need to tell us the name of the witness and what you disagree with"),
    "WITNESS_NEEDED_REQUIRED": _("You must tell us if you want to call a defence witness"),
    "WITNESS_DETAILS_REQUIRED": _("Tell us the name, address and date of birth of your defence witness"),
    "WITNESS_INTERPRETER_NEEDED_REQUIRED": _("Tell us if your witness needs an interpreter in court"),
    "WITNESS_INTERPRETER_LANGUAGE_REQUIRED": _("Your witness needs an interpreter in court - tell us which language"),
    "YOU_ARE_REQUIRED": _("You must let us know if you're employed, receiving benefits or other"),
    "PAY_PERIOD_REQUIRED": _("Tell us how often you get paid"),
    "PAY_AMOUNT_REQUIRED": _("Enter your take home pay"),
    "BENEFITS_DETAILS_REQUIRED": _("Tell us which benefits you receive"),
    "BENEFITS_DEPENDANTS_REQUIRED": _("Tell us if this includes payment for dependants"),
    "HARDSHIP_REQUIRED": _("Tell us if paying a fine would cause you serious financial problems"),
    "UNDERSTAND_REQUIRED": _("You must confirm that you have read and understand the important information"),
    "OTHER_INFO_REQUIRED": _("Tell us how you earn your money"),
    "HARDSHIP_DETAILS_REQUIRED": _("You must tell us why paying a fine will cause you serious financial problems"),
    "OTHER_BILL_PAYERS_REQUIRED": _("You must tell us if anyone else contributes to your household bills"),
    "HOUSEHOLD_ACCOMMODATION_REQUIRED": _("Accommodation is a required field"),
    "HOUSEHOLD_ACCOMMODATION_INVALID": _("Accommodation must be a number"),
    "HOUSEHOLD_ACCOMMODATION_MIN": _("Accommodation must be a number greater than, or equal to, 0"),
    "HOUSEHOLD_UTILITY_BILLS_REQUIRED": _("Utility bills is a required field"),
    "HOUSEHOLD_UTILITY_BILLS_INVALID": _("Utility bills must be a number"),
    "HOUSEHOLD_UTILITY_BILLS_MIN": _("Utility bills must be a number greater than, or equal to, 0"),
    "HOUSEHOLD_INSURANCE_REQUIRED": _("Insurance is a required field"),
    "HOUSEHOLD_INSURANCE_INVALID": _("Insurance must be a number"),
    "HOUSEHOLD_INSURANCE_MIN": _("Insurance must be a number greater than, or equal to, 0"),
    "HOUSEHOLD_COUNCIL_TAX_REQUIRED": _("Council tax is a required field"),
    "HOUSEHOLD_COUNCIL_TAX_INVALID": _("Council tax must be a number"),
    "HOUSEHOLD_COUNCIL_TAX_MIN": _("Council tax must be a number greater than, or equal to, 0"),
    "OTHER_TV_SUBSCRIPTION_REQUIRED": _("TV subscription is a required field"),
    "OTHER_TV_SUBSCRIPTION_INVALID": _("TV subscription must be a number"),
    "OTHER_TV_SUBSCRIPTION_MIN": _("TV subscription must be a number greater than, or equal to, 0"),
    "OTHER_TRAVEL_EXPENSES_REQUIRED": _("Travel expenses is a required field"),
    "OTHER_TRAVEL_EXPENSES_INVALID": _("Travel expenses must be a number"),
    "OTHER_TRAVEL_EXPENSES_MIN": _("Travel expenses must be a number greater than, or equal to, 0"),
    "OTHER_TELEPHONE_REQUIRED": _("Telephone is a required field"),
    "OTHER_TELEPHONE_INVALID": _("Telephone must be a number"),
    "OTHER_TELEPHONE_MIN": _("Telephone must be a number greater than, or equal to, 0"),
    "OTHER_LOAN_REPAYMENTS_REQUIRED": _("Loan repayment is a required field"),
    "OTHER_LOAN_REPAYMENTS_INVALID": _("Loan repayment must be a number"),
    "OTHER_LOAN_REPAYMENTS_MIN": _("Loan repayment must be a number greater than, or equal to, 0"),
    "OTHER_COURT_PAYMENTS_REQUIRED": _("Court payments is a required field"),
    "OTHER_COURT_PAYMENTS_INVALID": _("Court payments must be a number"),
    "OTHER_COURT_PAYMENTS_MIN": _("Court payments must be a number greater than, or equal to, 0"),
    "OTHER_CHILD_MAINTENANCE_REQUIRED": _("Child maintenance is a required field"),
    "OTHER_CHILD_MAINTENANCE_INVALID": _("Child maintenance must be a number"),
    "OTHER_CHILD_MAINTENANCE_MIN": _("Child maintenance must be a number greater than, or equal to, 0"),
    "COMPANY_TRADING_PERIOD": _("You must tell us if the company has been trading for more than 12 months"),
    "COMPANY_NUMBER_EMPLOYEES": _("Enter the number of employees"),
    "COMPANY_GROSS_TURNOVER": _("Enter the company's gross turnover"),
    "COMPANY_NET_TURNOVER": _("Enter the company's net turnover"),
    "COMPANY_GROSS_TURNOVER_PROJECTED": _("Enter the company's projected gross turnover"),
    "COMPANY_NET_TURNOVER_PROJECTED": _("Enter the company's projected net turnover"),
    "RECEIVE_EMAIL_UPDATES_REQUIRED": _("Tell us if you want to receive email updates about this case"),
    "UPDATES_EMAIL_REQUIRED": _("You must provide an email address if you want to receive email updates about this case")
}
