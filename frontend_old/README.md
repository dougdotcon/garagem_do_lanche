# 🍔 Sistema ERP Garagem do Lanche

Sistema completo de gestão para restaurante com frontend moderno e backend robusto em Python Flask.

## 📋 Funcionalidades

### 🛒 Para Clientes
- **Cardápio Digital**: Visualização de pratos com preços e descrições
- **Pedidos Online**: Sistema completo de pedidos com dados de entrega
- **Cálculo Automático**: Taxa de entrega baseada no bairro
- **Acompanhamento**: Status em tempo real do pedido

### 🍳 Para Cozinha
- **Painel de Pedidos**: Visualização de todos os pedidos recebidos
- **Gestão de Status**: Atualização do status dos pedidos
- **Impressão**: Funcionalidade para imprimir pedidos
- **Autenticação**: Acesso protegido por senha

### ⚙️ Para Administradores
- **Dashboard Completo**: Estatísticas e métricas do negócio
- **Gestão de Usuários**: Criar, editar e gerenciar usuários
- **Controle de Cardápio**: Adicionar, editar e remover pratos
- **Relatórios Financeiros**: Controle completo do caixa
- **Gestão de Pedidos**: Visualização e controle de todos os pedidos

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.10+**
- **Flask 2.3.3** - Framework web
- **SQLAlchemy 2.0.21** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte a CORS
- **Werkzeug** - Segurança e hash de senhas

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização moderna e responsiva
- **JavaScript ES6+** - Interatividade e comunicação com API
- **Fetch API** - Requisições HTTP
- **LocalStorage** - Armazenamento local

## 📦 Estrutura do Projeto

```
garagem-do-lanche/
├── backend/                    # API Backend
│   ├── app.py                 # Aplicação principal
│   ├── config.py              # Configurações
│   ├── models.py              # Modelos do banco de dados
│   ├── database.py            # Inicialização do banco
│   ├── requirements.txt       # Dependências Python
│   ├── routes/                # Rotas da API
│   │   ├── auth.py           # Autenticação
│   │   ├── admin.py          # Administração
│   │   ├── cardapio.py       # Gestão do cardápio
│   │   ├── pedidos.py        # Gestão de pedidos
│   │   └── caixa.py          # Controle financeiro
│   └── instance/
│       └── garagem_lanche.db  # Banco SQLite
├── frontend/                   # Interface do usuário
│   ├── index.html             # Cardápio principal
│   ├── entrega.html           # Formulário de pedido
│   ├── status.html            # Status do pedido
│   ├── login.html             # Login da cozinha
│   ├── cozinha.html           # Painel da cozinha
│   ├── admin-login.html       # Login administrativo
│   ├── admin-dashboard.html   # Painel administrativo
│   ├── api.js                 # Cliente da API
│   ├── styles.css             # Estilos globais
│   └── *.js                   # Scripts específicos
└── README.md                   # Esta documentação
```

## 🔧 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.10 ou superior
- Navegador web moderno

### 2. Instalação do Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Executar a Aplicação
```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

### 4. Acessar o Frontend
Abra o arquivo `frontend/index.html` em um navegador ou use um servidor local:

```bash
# Usando Python
cd frontend
python -m http.server 8000

# Ou usando Node.js
npx serve .
```

## 👥 Usuários Padrão

### Administrador
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Acesso**: Painel administrativo completo

### Cozinha
- **Usuário**: `cozinha`
- **Senha**: `garagem2025`
- **Acesso**: Painel da cozinha

## 🗄️ Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **usuarios** - Usuários do sistema (admin, cozinha, funcionários)
- **pratos** - Cardápio do restaurante
- **acompanhamentos** - Opções de acompanhamento
- **clientes** - Dados dos clientes
- **enderecos** - Endereços de entrega
- **pedidos** - Pedidos realizados
- **movimentacoes_caixa** - Controle financeiro

## 🔗 Endpoints da API

### Públicos
- `GET /api/health` - Status da API
- `GET /api/cardapio` - Listar pratos
- `GET /api/acompanhamentos` - Listar acompanhamentos
- `POST /api/pedidos` - Criar pedido

### Cozinha
- `POST /api/auth/login` - Login da cozinha
- `GET /api/pedidos/cozinha` - Pedidos para cozinha
- `PUT /api/pedidos/{id}/status` - Atualizar status

### Administrativos
- `POST /api/admin/login` - Login administrativo
- `GET /api/admin/dashboard` - Dashboard
- `GET /api/admin/usuarios` - Listar usuários
- `POST /api/admin/usuarios` - Criar usuário
- `GET /api/caixa/relatorio` - Relatório financeiro

## 💰 Sistema de Preços

### Taxa de Entrega por Bairro
- **Gramacho**: R$ 1,00
- **Centro**: R$ 2,00
- **Parque/Vila**: R$ 3,00
- **Jardim/Mutuá**: R$ 4,00
- **Outros bairros**: R$ 5,00

## 🎨 Características do Frontend

- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Interface Moderna**: Design limpo e intuitivo
- **Feedback Visual**: Loading states e mensagens de erro
- **Navegação Fluida**: Transições suaves entre páginas
- **Acessibilidade**: Estrutura semântica e contraste adequado

## 🔐 Segurança

- **Autenticação por Sessão**: Controle de acesso seguro
- **Hash de Senhas**: Senhas criptografadas com Werkzeug
- **Validação de Dados**: Validação tanto no frontend quanto backend
- **CORS Configurado**: Controle de origens permitidas
- **Sanitização**: Prevenção contra XSS e injeção

## 📱 Funcionalidades Especiais

### Integração com ViaCEP
- Preenchimento automático de endereço por CEP
- Validação de CEP em tempo real

### Sistema de Status
- **Aceito**: Pedido confirmado pelo restaurante
- **Preparo**: Pedido sendo preparado na cozinha
- **Entrega**: Pedido saiu para entrega
- **Finalizado**: Pedido entregue ao cliente

### Relatórios Financeiros
- Vendas por período
- Controle de entradas e saídas
- Gestão de fiados
- Dashboard com métricas importantes

## 🚀 Próximas Funcionalidades

- [ ] Notificações em tempo real
- [ ] Sistema de cupons e promoções
- [ ] Integração com WhatsApp
- [ ] App mobile nativo
- [ ] Sistema de avaliações
- [ ] Múltiplas formas de pagamento online

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- 📧 Email: suporte@garagemdoburger.com
- 📱 WhatsApp: (21) 99999-9999
- 🌐 Site: www.garagemdoburger.com

---

**Desenvolvido com ❤️ para a Garagem do Lanche**
