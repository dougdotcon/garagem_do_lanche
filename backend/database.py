from models import db, Prato, Acompanhamento, Cliente, Endereco, Pedido, MovimentacaoCaixa, Usuario
from models import StatusPedido, FormaPagamento, TipoUsuario

def init_database(app):
    """Inicializa o banco de dados e cria as tabelas"""
    with app.app_context():
        db.create_all()
        seed_initial_data()

def seed_initial_data():
    """Popula o banco com dados iniciais"""

    # Verificar se já existem dados
    if Prato.query.first() is not None:
        return

    # Criar usuário administrador padrão
    admin_user = Usuario(
        username='admin',
        email='admin@garagemdoburger.com',
        nome_completo='Administrador do Sistema',
        tipo=TipoUsuario.ADMIN
    )
    admin_user.set_password('admin123')  # Senha padrão - deve ser alterada
    db.session.add(admin_user)

    # Criar usuário da cozinha
    cozinha_user = Usuario(
        username='cozinha',
        email='cozinha@garagemdoburger.com',
        nome_completo='Operador da Cozinha',
        tipo=TipoUsuario.COZINHA
    )
    cozinha_user.set_password('garagem2025')  # Mesma senha atual
    db.session.add(cozinha_user)

    # Pratos do cardápio
    pratos_iniciais = [
        {'nome': 'X-Burger Clássico', 'preco': 15.00, 'descricao': 'Hambúrguer, queijo, alface, tomate'},
        {'nome': 'X-Bacon', 'preco': 18.00, 'descricao': 'Hambúrguer, bacon, queijo, alface, tomate'},
        {'nome': 'X-Tudo', 'preco': 22.00, 'descricao': 'Hambúrguer, bacon, queijo, ovo, alface, tomate'},
        {'nome': 'X-Frango', 'preco': 16.00, 'descricao': 'Frango grelhado, queijo, alface, tomate'},
        {'nome': 'X-Calabresa', 'preco': 17.00, 'descricao': 'Calabresa, queijo, cebola, alface, tomate'},
        {'nome': 'Misto Quente', 'preco': 8.00, 'descricao': 'Presunto e queijo no pão de forma'},
        {'nome': 'Bauru', 'preco': 12.00, 'descricao': 'Presunto, queijo, tomate, orégano'},
        {'nome': 'Hot Dog Simples', 'preco': 10.00, 'descricao': 'Salsicha, molho, batata palha'},
        {'nome': 'Hot Dog Especial', 'preco': 14.00, 'descricao': 'Salsicha, queijo, bacon, molho, batata palha'}
    ]

    for prato_data in pratos_iniciais:
        prato = Prato(**prato_data)
        db.session.add(prato)

    # Acompanhamentos
    acompanhamentos_iniciais = [
        {'nome': 'Fritas', 'icone': '🍟'},
        {'nome': 'Legumes', 'icone': '🥦'},
        {'nome': 'Purê', 'icone': '🥔'},
        {'nome': 'Salada Verde', 'icone': '🥒'}
    ]

    for acomp_data in acompanhamentos_iniciais:
        acompanhamento = Acompanhamento(**acomp_data)
        db.session.add(acompanhamento)

    db.session.commit()
    print("Dados iniciais inseridos no banco de dados!")

def calcular_taxa_entrega(bairro):
    """Calcula a taxa de entrega baseada no bairro"""
    if not bairro:
        return 5.00

    nome = bairro.lower()
    if "gramacho" in nome:
        return 1.00
    elif "centro" in nome:
        return 2.00
    elif "parque" in nome or "vila" in nome:
        return 3.00
    elif "jardim" in nome or "mutuá" in nome:
        return 4.00
    else:
        return 5.00
