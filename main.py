from datetime import date
from typing import List
import unittest

# Command Interface
class Command:
    def execute(self) -> None:
        pass

# Invoker
class CommandInvoker:
    def __init__(self):
        self.__commands = []

    def add_command(self, command: Command) -> None:
        self.__commands.append(command)

    def execute_commands(self) -> None:
        for command in self.__commands:
            command.execute()

    def clear_commands(self) -> None:
        self.__commands = []

# Base User Class
class User:
    def __init__(self, user_id: str, name: str, password: str, role: str, email: str):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.role = role
        self.email = email

    def login(self, user_id: str, password: str) -> bool:
        if self.user_id == user_id and self.password == password:
            print(f"{self.name} logged in.")
            return True
        else:
            print("Login failed.")
            return False

    def logout(self) -> None:
        print(f"{self.name} logged out.")

    def view_details(self) -> None:
        print(f"User ID: {self.user_id}, Name: {self.name}, Role: {self.role}, Email: {self.email}")

# Contributor Class
class Contributor(User):
    def __init__(self, user_id: str, name: str, password: str, email: str, contact_details: str, bank_details: str):
        super().__init__(user_id, name, password, "Contributor", email)
        self.contact_details = contact_details
        self.bank_details = bank_details
        self.fee_agreements: List['FeeAgreement'] = []

    def update_details(self, contact_details: str = None, bank_details: str = None) -> None:
        if contact_details:
            self.contact_details = contact_details
        if bank_details:
            self.bank_details = bank_details
        print(f"Details updated for {self.name}.")

    def view_details(self) -> None:
        super().view_details()
        print(f"Contact Details: {self.contact_details}, Bank Details: {self.bank_details}")

    def retrieve_fee_agreements(self) -> None:
        for agreement in self.fee_agreements:
            print(agreement)

# Editor Class
class Editor(User):
    def __init__(self, user_id: str, name: str, password: str, email: str):
        super().__init__(user_id, name, password, "Editor", email)
        self.fee_agreements: List['FeeAgreement'] = []

    def retrieve_fee_agreements(self) -> None:
        for agreement in self.fee_agreements:
            print(agreement)

    def change_dispute_status(self, agreement: 'FeeAgreement', dispute_status: bool) -> None:
        agreement.dispute_status = dispute_status
        print(f"Dispute status for agreement {agreement} changed to {dispute_status}.")

    def create_issue(self, issue_number: int) -> 'MagazineIssue':
        issue = MagazineIssue(issue_number, self)
        print(f"Issue {issue_number} created successfully by {self.name}.")
        return issue

# Accountant Class
class Accountant(User):
    def __init__(self, user_id: str, name: str, password: str, email: str):
        super().__init__(user_id, name, password, "Accountant", email)

    def process_payments(self, contributors: List[Contributor], latest_issue: 'MagazineIssue') -> None:
        print("Processing payments for contributors...")
        for contributor in contributors:
            for agreement in contributor.fee_agreements:
                if agreement.magazine_issue == latest_issue and not agreement.fee_paid and not agreement.dispute_status and contributor.bank_details:
                    agreement.fee_paid = True
                    print(f"Paid {contributor.name} (${agreement.fee_amount}).")

    def retrieve_all_fee_agreements(self, contributors: List[Contributor]) -> None:
        for contributor in contributors:
            for agreement in contributor.fee_agreements:
                print(agreement)

    def retrieve_unpaid_fee_agreements(self, contributors: List[Contributor]) -> None:
        for contributor in contributors:
            for agreement in contributor.fee_agreements:
                if not agreement.fee_paid:
                    print(agreement)

    def retrieve_paid_fee_agreements(self, contributors: List[Contributor]) -> None:
        for contributor in contributors:
            for agreement in contributor.fee_agreements:
                if agreement.fee_paid:
                    print(agreement)

    def retrieve_disputed_fee_agreements(self, contributors: List[Contributor]) -> None:
        for contributor in contributors:
            for agreement in contributor.fee_agreements:
                if agreement.dispute_status:
                    print(agreement)

    def retrieve_invalid_bank_details(self, contributors: List[Contributor]) -> None:
        for contributor in contributors:
            if not contributor.bank_details:
                for agreement in contributor.fee_agreements:
                    print(agreement)

# MagazineIssue Class
class MagazineIssue:
    def __init__(self, issue_number: int, editor: Editor):
        self.issue_number = issue_number
        self.editor = editor
        self.contributions: List[Contributor] = []
        self.published = False

    def publish(self) -> None:
        self.published = True
        print(f"Magazine Issue {self.issue_number} published.")

# FeeAgreement Class
class FeeAgreement:
    def __init__(self, fee_amount: int, date_agreed: date, contributor: Contributor, editor: Editor, magazine_issue: MagazineIssue):
        self.fee_amount = fee_amount
        self.date_agreed = date_agreed
        self.contributor = contributor
        self.editor = editor
        self.magazine_issue = magazine_issue
        self.fee_paid = False
        self.dispute_status = False

    def __str__(self):
        return f"FeeAgreement(Amount: {self.fee_amount}, Paid: {self.fee_paid}, Disputed: {self.dispute_status})"

# Command to Process Payments
class ProcessPaymentsCommand(Command):
    def __init__(self, accountant: Accountant, contributors: List[Contributor], latest_issue: MagazineIssue):
        self.accountant = accountant
        self.contributors = contributors
        self.latest_issue = latest_issue

    def execute(self) -> None:
        self.accountant.process_payments(self.contributors, self.latest_issue)

# Command to Retrieve Fee Agreements
class RetrieveFeeAgreementsCommand(Command):
    def __init__(self, accountant: Accountant, contributors: List[Contributor]):
        self.accountant = accountant
        self.contributors = contributors

    def execute(self) -> None:
        self.accountant.retrieve_all_fee_agreements(self.contributors)

# Unit Testing Class
class TestITMagazineSystem(unittest.TestCase):
    def setUp(self):
        # Create 1 accountant
        self.accountant = Accountant("A001", "Accountant Alice", "pass123", "accountant@example.com")

        # Create 2 editors
        self.editor1 = Editor("E001", "Editor John", "pass123", "editor.john@example.com")
        self.editor2 = Editor("E002", "Editor Jane", "pass456", "editor.jane@example.com")

        # Create 4 contributors
        self.contributor1 = Contributor("C001", "Contributor A", "pass123", "contributor.a@example.com", "1234567890", "1111-2222")
        self.contributor2 = Contributor("C002", "Contributor B", "pass456", "contributor.b@example.com", "9876543210", "3333-4444")
        self.contributor3 = Contributor("C003", "Contributor C", "pass789", "contributor.c@example.com", "1122334455", "5555-6666")
        self.contributor4 = Contributor("C004", "Contributor D", "pass000", "contributor.d@example.com", "9988776655", "7777-8888")

        # Assign contributors to editors
        self.editor1_contributors = [self.contributor1, self.contributor2]
        self.editor2_contributors = [self.contributor3, self.contributor4]

        # Create magazine issues
        self.issue1 = MagazineIssue(1, self.editor1)
        self.issue2 = MagazineIssue(2, self.editor1)
        self.issue3 = MagazineIssue(3, self.editor2)
        self.issue4 = MagazineIssue(4, self.editor2)

        # Publish some issues
        self.issue1.publish()
        self.issue3.publish()

        # Create fee agreements
        self.agreement1 = FeeAgreement(200, date.today(), self.contributor1, self.editor1, self.issue1)
        self.agreement2 = FeeAgreement(250, date.today(), self.contributor2, self.editor1, self.issue1)
        self.agreement3 = FeeAgreement(300, date.today(), self.contributor3, self.editor2, self.issue3)
        self.agreement4 = FeeAgreement(350, date.today(), self.contributor4, self.editor2, self.issue3)

        # Assign agreements to contributors
        self.contributor1.fee_agreements.append(self.agreement1)
        self.contributor2.fee_agreements.append(self.agreement2)
        self.contributor3.fee_agreements.append(self.agreement3)
        self.contributor4.fee_agreements.append(self.agreement4)

        # Assign contributors to issues
        self.issue1.contributions.extend([self.contributor1, self.contributor2])
        self.issue3.contributions.extend([self.contributor3, self.contributor4])

    def test_login(self):
        self.assertTrue(self.editor1.login("E001", "pass123"))
        self.assertFalse(self.editor2.login("E002", "wrongpass"))

    def test_view_details(self):
        self.contributor1.view_details()

    def test_update_details(self):
        self.contributor1.update_details(contact_details="1111111111", bank_details="9999-0000")
        self.assertEqual(self.contributor1.contact_details, "1111111111")
        self.assertEqual(self.contributor1.bank_details, "9999-0000")

    def test_process_payments(self):
        self.accountant.process_payments(self.editor1_contributors, self.issue1)
        self.assertTrue(self.agreement1.fee_paid)
        self.assertTrue(self.agreement2.fee_paid)

    def test_dispute_fee_agreement(self):
        self.editor2.change_dispute_status(self.agreement3, True)
        self.assertTrue(self.agreement3.dispute_status)

    def test_retrieve_fee_agreements(self):
        self.accountant.retrieve_all_fee_agreements(self.editor1_contributors)

if __name__ == "__main__":
    unittest.main()
