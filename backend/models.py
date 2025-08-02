from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class StatusPedido(Enum):
    ACEITO = "aceito"
    PREPARO = "preparo"
    ENTREGA = "entrega"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"

class FormaPagamento(Enum):
    DINHEIRO = "Dinheiro"
    PIX = "Pix"
    CARTAO = "Cartão"

class TipoUsuario(Enum):
    ADMIN = "admin"
    COZINHA = "cozinha"
    FUNCIONARIO = "funcionario"

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.Enum(TipoUsuario), nullable=False, default=TipoUsuario.FUNCIONARIO)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Define a senha do usuário"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nome_completo': self.nome_completo,
            'tipo': self.tipo.value,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Prato(db.Model):
    __tablename__ = 'pratos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'descricao': self.descricao,
            'ativo': self.ativo
        }

class Acompanhamento(db.Model):
    __tablename__ = 'acompanhamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    icone = db.Column(db.String(10))
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'icone': self.icone,
            'ativo': self.ativo
        }

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'created_at': self.created_at.isoformat()
        }

class Endereco(db.Model):
    __tablename__ = 'enderecos'

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    complemento = db.Column(db.String(200))
    taxa_entrega = db.Column(db.Float, nullable=False, default=5.00)

    # Relacionamento
    pedidos = db.relationship('Pedido', backref='endereco', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cep': self.cep,
            'rua': self.rua,
            'numero': self.numero,
            'bairro': self.bairro,
            'complemento': self.complemento,
            'taxa_entrega': self.taxa_entrega
        }

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    prato_id = db.Column(db.Integer, db.ForeignKey('pratos.id'), nullable=False)
    acompanhamento_id = db.Column(db.Integer, db.ForeignKey('acompanhamentos.id'), nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos.id'), nullable=False)

    status = db.Column(db.Enum(StatusPedido), default=StatusPedido.ACEITO)
    forma_pagamento = db.Column(db.Enum(FormaPagamento), nullable=False)

    valor_prato = db.Column(db.Float, nullable=False)
    taxa_entrega = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    prato = db.relationship('Prato', backref='pedidos')
    acompanhamento = db.relationship('Acompanhamento', backref='pedidos')

    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente.to_dict(),
            'prato': self.prato.to_dict(),
            'acompanhamento': self.acompanhamento.to_dict(),
            'endereco': self.endereco.to_dict(),
            'status': self.status.value,
            'forma_pagamento': self.forma_pagamento.value,
            'valor_prato': self.valor_prato,
            'taxa_entrega': self.taxa_entrega,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class MovimentacaoCaixa(db.Model):
    __tablename__ = 'movimentacoes_caixa'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'entrada', 'saida', 'fiado'
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    pedido = db.relationship('Pedido', backref='movimentacoes')

    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'tipo': self.tipo,
            'valor': self.valor,
            'descricao': self.descricao,
            'created_at': self.created_at.isoformat()
        }
