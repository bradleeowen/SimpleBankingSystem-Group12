from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?[0-9]{7,15}$", "Enter a valid phone number")],
        unique=True,
    )
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Branch(TimeStampedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Account(TimeStampedModel):
    SAVINGS = 'SAV'
    CURRENT = 'CUR'
    ACCOUNT_TYPES = [
        (SAVINGS, 'Savings'),
        (CURRENT, 'Current'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPES, default=SAVINGS)
    balance = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.account_number} ({self.get_account_type_display()})"


class Card(TimeStampedModel):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    CARD_TYPES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='card')
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=6, choices=CARD_TYPES, default=DEBIT)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.card_number} ({self.card_type})"


class Loan(TimeStampedModel):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REPAID = 'REPAID'
    STATUSES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REPAID, 'Repaid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    principal_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])  # % per annum
    status = models.CharField(max_length=10, choices=STATUSES, default=PENDING)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Loan {self.id} - {self.customer}"


class Transaction(TimeStampedModel):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'
    TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    txn_type = models.CharField(max_length=8, choices=TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0.01)])
    reference = models.CharField(max_length=64, unique=True)
    performed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-performed_at']

    def __str__(self):
        return f"{self.txn_type} {self.amount} on {self.account}"

