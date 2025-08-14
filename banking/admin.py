from django.contrib import admin
from .models import Customer, Branch, Account, Card, Loan, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city")
    search_fields = ("name", "code", "city")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_number", "customer", "branch", "account_type",
        "balance", "is_active"
    )
    search_fields = ("account_number",)
    list_filter = ("account_type", "is_active")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("card_number", "account", "card_type", "expiry_date", "is_active")
    search_fields = ("card_number",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "id", "customer", "principal_amount", "interest_rate",
        "status", "start_date"
    )
    list_filter = ("status",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "account", "txn_type", "amount", "reference", "performed_at"
    )
    search_fields = ("reference",)
    list_filter = ("txn_type",)
