from django.db import models
from usuarios.models import User

class Bank(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.code} - {self.name}"

class DailyRate(models.Model):
    date = models.DateField(unique=True)
    market_rate = models.DecimalField(max_digits=10, decimal_places=4)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=4)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=4)
    def __str__(self):
        return f"Taxa de {self.date}"

class RemittanceRequest(models.Model):
    STATUSES = (
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('em_processamento', 'Em Processamento'),
        ('concluida', 'Concluída'),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    retailer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'varejista'}, related_name='remittances')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'atacadista'}, related_name='payments_to_process', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='pendente')
    daily_rate = models.ForeignKey(DailyRate, on_delete=models.PROTECT)
    total_amount_reals = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    expected_dollars = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dollars_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    def __str__(self):
        return f"Remessa {self.id} - {self.retailer.username}"

class BeneficiaryPayment(models.Model):
    STATUSES = (
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
        ('invalido', 'Inválido'),
    )
    PIX_KEY_TYPES = (
        ('cpf', 'CPF'),
        ('email', 'Email'),
        ('phone', 'Telefone'),
        ('random', 'Chave Aleatória'),
    )
    remittance_request = models.ForeignKey(RemittanceRequest, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    beneficiary_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, blank=True)
    agency = models.CharField(max_length=10, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    cpf = models.CharField(max_length=14, blank=True)
    pix_key_type = models.CharField(max_length=10, choices=PIX_KEY_TYPES, blank=True)
    pix_key = models.CharField(max_length=100, blank=True)
    amount_reals = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUSES, default='pendente')
    payment_date = models.DateField(null=True, blank=True)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    observation = models.TextField(blank=True)
    reason = models.TextField(blank=True)  # Novo campo para motivo
    def __str__(self):
        return f"Pagamento para {self.beneficiary_name}"

class DollarPurchase(models.Model):
    remittance_request = models.ForeignKey(RemittanceRequest, on_delete=models.CASCADE, related_name='purchases')
    amount_dollars = models.DecimalField(max_digits=15, decimal_places=2)
    date_received = models.DateField()
    def __str__(self):
        return f"Compra de {self.amount_dollars} USD"

class SellTransaction(models.Model):
    TRANSFER_TYPES = (
        ('wire', 'Wire Transfer'),
        ('usdt', 'USDT'),
    )
    date = models.DateField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'cliente'})
    amount_dollars_sold = models.DecimalField(max_digits=15, decimal_places=2)
    daily_rate = models.ForeignKey(DailyRate, on_delete=models.PROTECT)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=4)
    transfer_type = models.CharField(max_length=10, choices=TRANSFER_TYPES)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    fee_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_to_receive = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    amount_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return f"Venda de {self.amount_dollars_sold} USD para {self.client.username}"

class AdvancePayment(models.Model):
    STATUSES = (
        ('pendente', 'Pendente'),
        ('liquidado', 'Liquidado'),
    )
    payee = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='pendente')
    def __str__(self):
        return f"Antecipação de {self.amount} para {self.payee.username}"

class Receipt(models.Model):
    PAYMENT_TYPES = (
        ('beneficiario', 'Beneficiário'),
        ('antecipado', 'Antecipado'),
    )
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPES)
    related_id = models.PositiveIntegerField()
    file = models.FileField(upload_to='receipts/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Recibo {self.id} - {self.payment_type}"