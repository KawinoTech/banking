import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from application.main import app
from application.models.accounts import Account
from ...database import  get_db
from ... import oauth
class TestTransferEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        # Mock database session
        self.mock_db = MagicMock()

        # Example user
        self.mock_current_user = "test_user"

        # Mock dependencies for db and current user
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[oauth.get_current_user] = lambda: self.mock_current_user

    def tearDown(self):
        # Clear dependency overrides
        app.dependency_overrides = {}

    def test_successful_transfer(self):
        # Mock account with sufficient balance
        mock_account = MagicMock(spec=Account)
        mock_account.account_no = "12345"
        mock_account.account_balance = 1000

        # Mock DB query to return the account
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        # Mock payload
        transaction_data = {
            "payload": {
                "account": "12345",
                "amount": 500
            }
        }

        # Make POST request
        response = self.client.post("/transfer", json=transaction_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertIn("ref_no", response.json())

    def test_account_not_found(self):
        # Mock DB query to return None (account not found)
        self.mock_db.query.return_value.filter.return_value.first.return_value = None

        # Mock payload
        transaction_data = {
            "payload": {
                "account": "99999",  # Non-existent account
                "amount": 500
            }
        }

        # Make POST request
        response = self.client.post("/transfer", json=transaction_data)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Account does not exist.")

    def test_insufficient_funds(self):
        # Mock account with insufficient balance
        mock_account = MagicMock(spec=Account)
        mock_account.account_no = "12345"
        mock_account.account_balance = 300  # Less than transfer amount

        # Mock DB query
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        # Mock payload
        transaction_data = {
            "payload": {
                "account": "12345",
                "amount": 500
            }
        }

        # Make POST request
        response = self.client.post("/transfer", json=transaction_data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Failed. Insufficient Funds")

    def test_invalid_amount(self):
        # Mock account (balance won't be checked due to invalid amount)
        mock_account = MagicMock(spec=Account)
        mock_account.account_no = "12345"

        # Mock DB query
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        # Mock payload
        transaction_data = {
            "payload": {
                "account": "12345",
                "amount": -100  # Invalid amount
            }
        }

        # Make POST request
        response = self.client.post("/transfer", json=transaction_data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Transaction amount must be greater than zero.")

    def test_database_error(self):
        # Mock account with sufficient balance
        mock_account = MagicMock(spec=Account)
        mock_account.account_no = "12345"
        mock_account.account_balance = 1000

        # Mock DB query
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_account

        # Simulate a database IntegrityError during commit
        self.mock_db.commit.side_effect = IntegrityError

        # Mock payload
        transaction_data = {
            "payload": {
                "account": "12345",
                "amount": 500
            }
        }

        # Make POST request
        response = self.client.post("/transfer", json=transaction_data)

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Database error occurred.")

if __name__ == "__main__":
    unittest.main()
