# API Garagem do Lanche

Backend em Flask para o sistema ERP da Garagem do Lanche.

## 🚀 Instalação e Execução

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação
```bash
python app.py
```
ou
```bash
python run.py
```

### 3. Modo produção
```bash
python run.py --prod
```

## 📊 Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **pratos** - Cardápio do restaurante
- **acompanhamentos** - Opções de acompanhamento
- **clientes** - Dados dos clientes
- **enderecos** - Endereços de entrega
- **pedidos** - Pedidos realizados
- **movimentacoes_caixa** - Controle financeiro

## 🔗 Endpoints da API

### Cardápio
- `GET /api/cardapio` - Listar pratos
- `GET /api/cardapio/{id}` - Buscar prato específico
- `POST /api/cardapio` - Criar novo prato
- `PUT /api/cardapio/{id}` - Atualizar prato
- `DELETE /api/cardapio/{id}` - Desativar prato

### Acompanhamentos
- `GET /api/acompanhamentos` - Listar acompanhamentos

### Pedidos
- `POST /api/pedidos` - Criar pedido
- `GET /api/pedidos` - Listar pedidos (com filtros)
- `GET /api/pedidos/{id}` - Buscar pedido específico
- `PUT /api/pedidos/{id}/status` - Atualizar status do pedido
- `GET /api/pedidos/cozinha` - Pedidos para painel da cozinha

### Caixa
- `GET /api/caixa/relatorio` - Relatório financeiro
- `GET /api/caixa/dashboard` - Dashboard do caixa
- `POST /api/caixa/movimentacao` - Criar movimentação

### Autenticação
- `POST /api/auth/login` - Login da cozinha
- `POST /api/auth/logout` - Logout
- `GET /api/auth/check` - Verificar autenticação

### Utilitários
- `GET /api/health` - Status da API
- `GET /api/info` - Informações da API

## 📝 Exemplo de Uso

### Criar um pedido
```json
POST /api/pedidos
{
  "nome": "João Silva",
  "telefone": "(21) 99999-9999",
  "rua": "Rua das Flores",
  "numero": "123",
  "bairro": "Centro",
  "cep": "25000-000",
  "complemento": "Apto 101",
  "prato_id": 1,
  "acompanhamento_id": 1,
  "forma_pagamento": "Pix",
  "observacoes": "Sem cebola"
}
```

### Atualizar status do pedido
```json
PUT /api/pedidos/1/status
{
  "status": "preparo"
}
```

## 🔧 Configuração

As configurações estão no arquivo `config.py`:

- **SECRET_KEY**: Chave secreta da aplicação
- **DATABASE_URL**: URL do banco SQLite
- **SENHA_COZINHA**: Senha para acesso à cozinha
- **CORS_ORIGINS**: Origens permitidas para CORS

## 📦 Estrutura do Projeto

```
backend/
├── app.py              # Aplicação principal
├── config.py           # Configurações
├── models.py           # Modelos do banco
├── database.py         # Inicialização do banco
├── requirements.txt    # Dependências
├── run.py             # Script de execução
├── routes/            # Rotas da API
│   ├── __init__.py
│   ├── cardapio.py
│   ├── pedidos.py
│   ├── caixa.py
│   └── auth.py
└── garagem_lanche.db  # Banco SQLite (criado automaticamente)
```

## 🍔 Dados Iniciais

O sistema é inicializado com:

### Pratos
- X-Burger Clássico (R$ 15,00)
- X-Bacon (R$ 18,00)
- X-Tudo (R$ 22,00)
- X-Frango (R$ 16,00)
- X-Calabresa (R$ 17,00)
- Misto Quente (R$ 8,00)
- Bauru (R$ 12,00)
- Hot Dog Simples (R$ 10,00)
- Hot Dog Especial (R$ 14,00)

### Acompanhamentos
- 🍟 Fritas
- 🥦 Legumes
- 🥔 Purê
- 🥒 Salada Verde

## 💰 Taxa de Entrega

O sistema calcula automaticamente a taxa de entrega baseada no bairro:

- Gramacho: R$ 1,00
- Centro: R$ 2,00
- Parque/Vila: R$ 3,00
- Jardim/Mutuá: R$ 4,00
- Outros: R$ 5,00

## 🔐 Autenticação

Senha padrão da cozinha: `garagem2025`

## 📱 Integração com Frontend

A API está configurada para funcionar com o frontend existente, mantendo compatibilidade com o localStorage e as funcionalidades já implementadas.
