from rest_framework import serializers
from .models import Bank, DailyRate, RemittanceRequest, BeneficiaryPayment, DollarPurchase, SellTransaction, AdvancePayment, Receipt
from usuarios.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'name']

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'code', 'name']

class DailyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRate
        fields = ['id', 'date', 'market_rate', 'buy_rate', 'sell_rate']

class BeneficiaryPaymentSerializer(serializers.ModelSerializer):  # Movido para cima
    class Meta:
        model = BeneficiaryPayment
        fields = ['id', 'remittance_request', 'beneficiary_name', 'account_number', 'agency', 'bank', 'cpf', 'pix_key_type', 'pix_key', 'amount_reals', 'status', 'payment_date', 'receipt', 'is_urgent', 'observation', 'reason']

class RemittanceRequestSerializer(serializers.ModelSerializer):
    payments = BeneficiaryPaymentSerializer(many=True, read_only=True)  # Agora funciona
    class Meta:
        model = RemittanceRequest
        fields = ['id', 'date_created', 'retailer', 'payer', 'status', 'daily_rate', 'total_amount_reals', 'expected_dollars', 'dollars_received', 'payments']

class DollarPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DollarPurchase
        fields = ['id', 'remittance_request', 'amount_dollars', 'date_received']

class SellTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellTransaction
        fields = ['id', 'date', 'client', 'amount_dollars_sold', 'daily_rate', 'sell_rate', 'transfer_type', 'fee_percentage', 'fee_amount', 'total_to_receive', 'amount_received', 'is_paid']

class AdvancePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancePayment
        fields = ['id', 'payee', 'amount', 'date', 'reference', 'status']

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'payment_type', 'related_id', 'file', 'uploaded_by', 'upload_date']