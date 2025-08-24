from rest_framework import serializers
from django.db import transaction as db_transaction
from .models import Customer, Branch, Account, Card, Loan, Transaction
from datetime import date




class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    class Meta:
        model = Customer
        fields = '__all__'
        


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for Branch model."""
    class Meta:
        model = Branch
        fields = '__all__'
    def validate_code(self, value):
        """Normalize branch code to uppercase and ensure min length."""
        v = (value or "").strip().upper()
        if len(v) < 3:
            raise serializers.ValidationError("Code must be at least 3 characters")
        return v


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model."""
    class Meta:
        model = Account
        fields = '__all__'

    def validate_balance(self, value):
        """Ensure account balance is not negative."""
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative")
        return value
    
    def validate_account_number(self, value):
        """Ensure account_number is trimmed and reasonably long."""
        v = (value or "").strip()
        if len(v) < 5:
            raise serializers.ValidationError("Account number must be at least 5 characters")
        return v



class CardSerializer(serializers.ModelSerializer):
    """Serializer for Card model."""
    class Meta:
        model = Card
        fields = '__all__'

    def validate_card_number(self, value):
        """Ensure card number is exactly 16 digits."""
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Card number must be 16 digits")
        return value
    
    def validate_expiry_date(self, value):
        """Card expiry must be in the future."""
        if value and value <= date.today():
            raise serializers.ValidationError("Card expiry date must be in the future")
        return value



class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model."""
    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, attrs):
        """Validate loan amounts/rates and date ordering."""
        # keep your existing checks:
        if attrs['principal_amount'] <= 0:
            raise serializers.ValidationError({"principal_amount": "Must be positive"})
        if attrs['interest_rate'] < 0:
            raise serializers.ValidationError({"interest_rate": "Cannot be negative"})

        # NEW: start_date < end_date (if both provided)
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and start >= end:
            raise serializers.ValidationError({"end_date": "Must be after start_date"})

        return attrs



class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['performed_at']

    def validate(self, attrs):
        """Validate transaction rules."""
        account = attrs['account']
        txn_type = attrs['txn_type']
        amount = attrs['amount']

        if amount <= 0:
            raise serializers.ValidationError({"amount": "Must be positive"})

        if txn_type == Transaction.WITHDRAW and account.balance < amount:
            raise serializers.ValidationError("Insufficient balance for withdrawal")

        if not account.is_active:
            raise serializers.ValidationError("Account is not active")

        return attrs

    def create(self, validated_data):
        """
        Create a transaction and update account balance atomically.
        Ensures withdrawals cannot exceed the account balance.
        """
        with db_transaction.atomic():
            account = validated_data['account']
            amount = validated_data['amount']
            txn_type = validated_data['txn_type']

            if txn_type == Transaction.DEPOSIT:
                account.balance += amount
            elif txn_type == Transaction.WITHDRAW:
                if account.balance < amount:
                    raise serializers.ValidationError("Insufficient balance for withdrawal")
                account.balance -= amount

            account.save(update_fields=['balance', 'updated_at'])
            return super().create(validated_data)
