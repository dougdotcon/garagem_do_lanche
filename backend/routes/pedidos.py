from flask import Blueprint, jsonify, request
from models import db, Pedido, Cliente, Endereco, Prato, Acompanhamento, MovimentacaoCaixa
from models import StatusPedido, FormaPagamento
from database import calcular_taxa_entrega
from datetime import datetime

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/api/pedidos', methods=['POST'])
def criar_pedido():
    """Cria um novo pedido"""
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['nome', 'telefone', 'rua', 'numero', 'bairro', 
                          'prato_id', 'acompanhamento_id', 'forma_pagamento']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Campo {field} é obrigatório'
                }), 400
        
        # Verificar se prato e acompanhamento existem
        prato = Prato.query.get(data['prato_id'])
        acompanhamento = Acompanhamento.query.get(data['acompanhamento_id'])
        
        if not prato or not prato.ativo:
            return jsonify({
                'success': False,
                'error': 'Prato não encontrado ou inativo'
            }), 400
            
        if not acompanhamento or not acompanhamento.ativo:
            return jsonify({
                'success': False,
                'error': 'Acompanhamento não encontrado ou inativo'
            }), 400
        
        # Criar ou buscar cliente
        cliente = Cliente.query.filter_by(telefone=data['telefone']).first()
        if not cliente:
            cliente = Cliente(
                nome=data['nome'],
                telefone=data['telefone']
            )
            db.session.add(cliente)
            db.session.flush()  # Para obter o ID
        
        # Calcular taxa de entrega
        taxa_entrega = calcular_taxa_entrega(data['bairro'])
        
        # Criar endereço
        endereco = Endereco(
            cep=data.get('cep', ''),
            rua=data['rua'],
            numero=data['numero'],
            bairro=data['bairro'],
            complemento=data.get('complemento', ''),
            taxa_entrega=taxa_entrega
        )
        db.session.add(endereco)
        db.session.flush()
        
        # Calcular valores
        valor_prato = prato.preco
        valor_total = valor_prato + taxa_entrega
        
        # Criar pedido
        pedido = Pedido(
            cliente_id=cliente.id,
            prato_id=prato.id,
            acompanhamento_id=acompanhamento.id,
            endereco_id=endereco.id,
            forma_pagamento=FormaPagamento(data['forma_pagamento']),
            valor_prato=valor_prato,
            taxa_entrega=taxa_entrega,
            valor_total=valor_total,
            observacoes=data.get('observacoes', ''),
            status=StatusPedido.ACEITO
        )
        
        db.session.add(pedido)
        db.session.flush()
        
        # Registrar movimentação no caixa
        movimentacao = MovimentacaoCaixa(
            pedido_id=pedido.id,
            tipo='entrada',
            valor=valor_total,
            descricao=f'Pedido #{pedido.id} - {prato.nome}'
        )
        db.session.add(movimentacao)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pedidos_bp.route('/api/pedidos', methods=['GET'])
def listar_pedidos():
    """Lista todos os pedidos com filtros opcionais"""
    try:
        # Parâmetros de filtro
        status = request.args.get('status')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = Pedido.query
        
        if status:
            query = query.filter(Pedido.status == StatusPedido(status))
        
        if data_inicio:
            data_inicio = datetime.fromisoformat(data_inicio)
            query = query.filter(Pedido.created_at >= data_inicio)
            
        if data_fim:
            data_fim = datetime.fromisoformat(data_fim)
            query = query.filter(Pedido.created_at <= data_fim)
        
        pedidos = query.order_by(Pedido.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'pedidos': [pedido.to_dict() for pedido in pedidos]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pedidos_bp.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    """Retorna um pedido específico"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pedidos_bp.route('/api/pedidos/<int:pedido_id>/status', methods=['PUT'])
def atualizar_status_pedido(pedido_id):
    """Atualiza o status de um pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'Status é obrigatório'
            }), 400
        
        novo_status = StatusPedido(data['status'])
        pedido.status = novo_status
        pedido.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'pedido': pedido.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pedidos_bp.route('/api/pedidos/cozinha', methods=['GET'])
def pedidos_cozinha():
    """Retorna pedidos para o painel da cozinha (aceitos e em preparo)"""
    try:
        pedidos = Pedido.query.filter(
            Pedido.status.in_([StatusPedido.ACEITO, StatusPedido.PREPARO])
        ).order_by(Pedido.created_at.asc()).all()
        
        return jsonify({
            'success': True,
            'pedidos': [pedido.to_dict() for pedido in pedidos]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
