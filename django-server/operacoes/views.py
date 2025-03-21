from rest_framework import viewsets
from rest_framework.response import Response  # Import adicionado
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

    def create(self, request, *args, **kwargs):
        data = request.data
        payment_ids = data.get('payments', [])  # Pegar os IDs dos pagamentos
        payments = BeneficiaryPayment.objects.filter(id__in=payment_ids, remittance_request__isnull=True)

        if not payments.exists():
            return Response({"error": "Nenhum pagamento válido encontrado"}, status=400)

        # Calcular total em reais e dólares
        total_amount_reals = sum(payment.amount_reals for payment in payments)
        daily_rate = DailyRate.objects.get(id=data['daily_rate'])
        expected_dollars = total_amount_reals / daily_rate.buy_rate

        # Criar a remessa
        remittance = RemittanceRequest.objects.create(
            retailer_id=data['retailer'],
            payer_id=data.get('payer'),
            daily_rate_id=data['daily_rate'],
            total_amount_reals=total_amount_reals,
            expected_dollars=expected_dollars,
            status='pendente'
        )

        # Associar os pagamentos à remessa
        payments.update(remittance_request=remittance)

        # Serializar e retornar
        serializer = self.get_serializer(remittance)
        return Response(serializer.data, status=201)
    
class BeneficiaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = BeneficiaryPayment.objects.all()
    serializer_class = BeneficiaryPaymentSerializer

    def update(self, request, *args, **kwargs):
        payment = self.get_object()  # Pega o pagamento atual
        user = request.user  # Usuário fazendo a requisição

        # Se o pagamento já está 'pago', aplicar restrições
        if payment.status == 'pago':
            # Verificar se há uma remessa associada e se o usuário é o pagador
            if not payment.remittance_request or payment.remittance_request.payer != user:
                raise PermissionDenied("Apenas o pagador pode alterar um pagamento concluído.")
            
            # Verificar se o motivo foi fornecido
            new_reason = request.data.get('reason', payment.reason)
            if not new_reason:
                raise ValidationError({"reason": "É necessário fornecer uma justificativa para alterar um pagamento concluído."})
            
            # Atualizar o reason se fornecido
            request.data['reason'] = new_reason

        # Prosseguir com a atualização padrão
        return super().update(request, *args, **kwargs)

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