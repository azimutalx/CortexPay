from django.contrib import admin
from .models import DailyRate, RemittanceRequest, BeneficiaryPayment, DollarPurchase, SellTransaction, AdvancePayment, Receipt, Bank

admin.site.register(DailyRate)
admin.site.register(RemittanceRequest)
admin.site.register(BeneficiaryPayment)
admin.site.register(DollarPurchase)
admin.site.register(SellTransaction)
admin.site.register(AdvancePayment)
admin.site.register(Receipt)
admin.site.register(Bank)