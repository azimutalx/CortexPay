from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from operacoes.views import (
    UserViewSet, BankViewSet, DailyRateViewSet, RemittanceRequestViewSet,
    BeneficiaryPaymentViewSet, DollarPurchaseViewSet, SellTransactionViewSet,
    AdvancePaymentViewSet, ReceiptViewSet
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'banks', BankViewSet)
router.register(r'daily-rates', DailyRateViewSet)
router.register(r'remittance-requests', RemittanceRequestViewSet)
router.register(r'beneficiary-payments', BeneficiaryPaymentViewSet)
router.register(r'dollar-purchases', DollarPurchaseViewSet)
router.register(r'sell-transactions', SellTransactionViewSet)
router.register(r'advance-payments', AdvancePaymentViewSet)
router.register(r'receipts', ReceiptViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Rotas da API
    path('api/', include('operacoes.urls')),  # Rotas do app operacoes (para o frontend e outras APIs)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Gera o schema OpenAPI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Interface Swagger
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/api/remittances/'), name='logout'),
]