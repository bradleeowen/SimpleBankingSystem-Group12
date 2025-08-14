from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    BranchViewSet,
    AccountViewSet,
    CardViewSet,
    LoanViewSet,
    TransactionViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'cards', CardViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'transactions', TransactionViewSet)

# API URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
