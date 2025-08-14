from django.contrib import admin
from .models import Customer, Branch, Account, Card, Loan, Transaction

admin.site.register(Customer)
admin.site.register(Branch)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Loan)
admin.site.register(Transaction)

