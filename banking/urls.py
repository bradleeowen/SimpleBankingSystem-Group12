from rest_framework.routers import DefaultRouter
from banking.views import (
    CustomerViewSet, BranchViewSet, AccountViewSet,
    CardViewSet, LoanViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'cards', CardViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = router.urls
