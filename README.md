Aqui está uma versão resumida, clara e bem explicada de tudo que documentamos até agora em Markdown. Ela cobre o essencial do projeto `CortexPay`, incluindo ambiente, modelos e API, mantendo a simplicidade para seu nível inferior a um desenvolvedor júnior. Você pode copiar isso diretamente para o `README.md`.

---

# **CortexPay - Sistema de Gestão de Câmbio**
**Data**: 21 de março de 2025  
**Autor**: [Seu nome] com assistência de Grok (xAI)  
**Objetivo**: Criar um backend para gerenciar operações de câmbio (remessas, taxas, pagamentos) usando Django, PostgreSQL e Docker, com API REST para um futuro frontend em React.

---

## **Visão Geral**
O `CortexPay` gerencia transações entre varejistas (compra de ouro) e clientes, com foco em taxas diárias, remessas, pagamentos e recibos. Até agora, configuramos o ambiente, criamos modelos, aplicamos migrações e adicionamos uma API com documentação interativa.

---

## **Estrutura do Projeto**
```
CortexPay/
├── django-server/         # Backend Django
│   ├── django_server/    # Configurações Django
│   ├── operacoes/        # App de operações
│   ├── usuarios/         # App de usuários
│   ├── Dockerfile        # Contêiner Django
│   ├── manage.py         # Gerenciador Django
│   └── requirements.txt  # Dependências
├── docker-compose.yml     # Serviços Docker
└── README.md             # Documentação
```

---

## **Configuração do Ambiente**
- **Tecnologias**:
  - Python 3.11, Django 4.2.11, Django REST Framework 3.15.1.
  - PostgreSQL 15 (banco de dados).
  - Docker (contêineres).
  - Dependências: `psycopg2-binary`, `dj-database-url`, `drf-spectacular`.
- **Passos**:
  1. Criado `Dockerfile` e `docker-compose.yml` para rodar Django e PostgreSQL.
  2. Projeto Django iniciado com `django-admin startproject`.
  3. Apps `usuarios` e `operacoes` criados e configurados em `settings.py`.
  4. Banco conectado via `DATABASE_URL`.

- **Comandos úteis**:
  - Iniciar: `docker-compose up -d --build`
  - Parar: `docker-compose down`
  - Logs: `docker-compose logs`

---

## **Modelos**
### **App `usuarios`**
- **`User`**:
  - **Campos**: `role` (atacadista, varejista, cliente), `name` (opcional).
  - **Propósito**: Gerenciar usuários com papéis.
  - **No admin**: Sim.

### **App `operacoes`**
- **`Bank`**:
  - **Campos**: `code` (ex.: "001"), `name` (ex.: "Banco do Brasil").
  - **Propósito**: Lista de bancos para pagamentos.
  - **No admin**: Sim.

- **`DailyRate`**:
  - **Campos**: `date`, `market_rate`, `buy_rate`, `sell_rate`.
  - **Propósito**: Taxas diárias de câmbio.
  - **No admin**: Sim.

- **`RemittanceRequest`**:
  - **Campos**: `date_created`, `retailer` (varejista), `status` (pendente, aceita, etc.), `daily_rate`, valores em reais e dólares.
  - **Propósito**: Solicitações de remessa.
  - **No admin**: Sim.

- **`BeneficiaryPayment`**:
  - **Campos**: `remittance_request`, `beneficiary_name`, `account_number`, `agency`, `bank` (ForeignKey), `cpf`, `pix_key_type` (cpf, email, etc.), `pix_key`, `amount_reals`, `status`, etc.
  - **Propósito**: Pagamentos a beneficiários.
  - **No admin**: Sim.

- **`DollarPurchase`**:
  - **Campos**: `remittance_request`, `amount_dollars`, `date_received`.
  - **Propósito**: Registro de dólares recebidos.
  - **No admin**: Sim.

- **`SellTransaction`**:
  - **Campos**: `date`, `client`, `amount_dollars_sold`, `daily_rate`, `sell_rate`, `transfer_type`, taxas e valores.
  - **Propósito**: Venda de dólares.
  - **No admin**: Sim.

- **`AdvancePayment`**:
  - **Campos**: `payee`, `amount`, `date`, `reference`, `status`.
  - **Propósito**: Pagamentos antecipados.
  - **No admin**: Sim.

- **`Receipt`**:
  - **Campos**: `payment_type`, `related_id`, `file`, `uploaded_by`, `upload_date`.
  - **Propósito**: Armazenar recibos.
  - **No admin**: Sim.

- **Migrações**: Aplicadas com `makemigrations` e `migrate`.

---

## **API**
- **Configuração**:
  - Usado Django REST Framework com `drf-spectacular` para documentação.
  - Serializers em `operacoes/serializers.py`.
  - Views em `operacoes/views.py` (ModelViewSet).
  - URLs em `django_server/urls.py`.

- **Endpoints**:
  - `/api/users/`
  - `/api/banks/`
  - `/api/daily-rates/`
  - `/api/remittance-requests/`
  - `/api/beneficiary-payments/`
  - `/api/dollar-purchases/`
  - `/api/sell-transactions/`
  - `/api/advance-payments/`
  - `/api/receipts/`

- **Documentação**:
  - Acessível em: `http://localhost:8000/api/schema/swagger-ui/`.
  - Interface Swagger para testar endpoints.

- **Exemplo**:
  - GET `/api/banks/` retorna:
    ```json
    [{"id": 1, "code": "001", "name": "Banco do Brasil"}]
    ```

---

## **Estado Atual**
- Backend funcionando com Docker.
- Modelos criados e visíveis no admin (`http://localhost:8000/admin/`).
- API configurada e documentada.
- Superusuário: `admin` / `1234`.
