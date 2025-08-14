from rest_framework import viewsets, permissions
from .models import Customer, Branch, Account, Card, Loan, Transaction
from .serializers import (
    CustomerSerializer, BranchSerializer, AccountSerializer,
    CardSerializer, LoanSerializer, TransactionSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.select_related('customer', 'branch').all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.select_related('account').all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.select_related('customer').all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related('account').all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
 