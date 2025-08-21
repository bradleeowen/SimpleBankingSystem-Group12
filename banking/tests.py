from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Branch, Account, Transaction, Loan, Card
from django.utils import timezone
from django.contrib.auth.models import User


class BankingAPITests(APITestCase):
    def setUp(self):
        
        # Create test user and authenticate
        self.user = User.objects.create_user(username="test_user", password="pass12345")
        self.client.login(username="test_user", password="pass12345")
        
        # Create a customer
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone="+12345678901",
            address="123 Test Street"
        )

        # Create a branch
        self.branch = Branch.objects.create(
            name="Main Branch",
            code="MB001",
            city="Test City"
        )

        # Create an account
        self.account = Account.objects.create(
            customer=self.customer,
            branch=self.branch,
            account_number="ACC12345",
            account_type=Account.SAVINGS,
            balance=1000.00
        )

        # URL endpoints
        self.customers_url = reverse('customer-list')
        self.accounts_url = reverse('account-list')
        self.transactions_url = reverse('transaction-list')
        self.loans_url = reverse('loan-list')
        self.cards_url = reverse('card-list')

    # Customers
    def test_create_customer(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "phone": "+19876543210",
            "address": "456 Example Ave"
        }
        response = self.client.post(self.customers_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_get_customers(self):
        response = self.client.get(self.customers_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # Accounts
    def test_create_account(self):
        data = {
            "customer": self.customer.id,
            "branch": self.branch.id,
            "account_number": "ACC67890",
            "account_type": Account.CURRENT,
            "balance": 500.00,
            "is_active": True
        }
        response = self.client.post(self.accounts_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_get_accounts(self):
        response = self.client.get(self.accounts_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Transactions
    def test_create_transaction_deposit(self):
        data = {
            "account": self.account.id,
            "txn_type": Transaction.DEPOSIT,
            "amount": 200.00,
            "reference": "TXN001"
        }
        response = self.client.post(self.transactions_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account.refresh_from_db()
        self.assertEqual(float(self.account.balance), 1200.00)  # balance updated

    def test_create_transaction_withdraw_insufficient_balance(self):
        data = {
            "account": self.account.id,
            "txn_type": Transaction.WITHDRAW,
            "amount": 999999.00,
            "reference": "TXN002"
        }
        response = self.client.post(self.transactions_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_withdraw_success(self):
        data = {
            "account": self.account.id,
            "txn_type": Transaction.WITHDRAW,
            "amount": 500.00,
            "reference": "TXN003"
        }
        response = self.client.post(self.transactions_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account.refresh_from_db()
        self.assertEqual(float(self.account.balance), 500.00)

    # Loans
    def test_create_loan(self):
        data = {
            "customer": self.customer.id,
            "principal_amount": 1000.00,
            "interest_rate": 5.0,
            "status": Loan.PENDING,
            "start_date": timezone.now().date(),
            "end_date": None
        }
        response = self.client.post(self.loans_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        
    # Cards
    def test_create_card(self):
        data = {
            "account": self.account.id,
            "card_number": "1111222233334444",
            "card_type": Card.DEBIT,
            "expiry_date": "2030-12-31",
            "is_active": True
        }
        response = self.client.post(self.cards_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)



