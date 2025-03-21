from rest_framework import viewsets
from .models import Bank, DailyRate, RemittanceRequest, BeneficiaryPayment, DollarPurchase, SellTransaction, AdvancePayment, Receipt
from usuarios.models import User
from .serializers import (
    UserSerializer, BankSerializer, DailyRateSerializer, RemittanceRequestSerializer,
    BeneficiaryPaymentSerializer, DollarPurchaseSerializer, SellTransactionSerializer,
    AdvancePaymentSerializer, ReceiptSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class DailyRateViewSet(viewsets.ModelViewSet):
    queryset = DailyRate.objects.all()
    serializer_class = DailyRateSerializer

class RemittanceRequestViewSet(viewsets.ModelViewSet):
    queryset = RemittanceRequest.objects.all()
    serializer_class = RemittanceRequestSerializer

class BeneficiaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = BeneficiaryPayment.objects.all()
    serializer_class = BeneficiaryPaymentSerializer

class DollarPurchaseViewSet(viewsets.ModelViewSet):
    queryset = DollarPurchase.objects.all()
    serializer_class = DollarPurchaseSerializer

class SellTransactionViewSet(viewsets.ModelViewSet):
    queryset = SellTransaction.objects.all()
    serializer_class = SellTransactionSerializer

class AdvancePaymentViewSet(viewsets.ModelViewSet):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer