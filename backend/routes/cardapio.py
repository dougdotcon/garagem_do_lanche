from flask import Blueprint, jsonify, request
from models import db, Prato, Acompanhamento

cardapio_bp = Blueprint('cardapio', __name__)

@cardapio_bp.route('/api/cardapio', methods=['GET'])
def get_cardapio():
    """Retorna todos os pratos ativos do cardápio"""
    try:
        pratos = Prato.query.filter_by(ativo=True).all()
        return jsonify({
            'success': True,
            'pratos': [prato.to_dict() for prato in pratos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cardapio_bp.route('/api/cardapio/<int:prato_id>', methods=['GET'])
def get_prato(prato_id):
    """Retorna um prato específico"""
    try:
        prato = Prato.query.get_or_404(prato_id)
        return jsonify({
            'success': True,
            'prato': prato.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cardapio_bp.route('/api/acompanhamentos', methods=['GET'])
def get_acompanhamentos():
    """Retorna todos os acompanhamentos ativos"""
    try:
        acompanhamentos = Acompanhamento.query.filter_by(ativo=True).all()
        return jsonify({
            'success': True,
            'acompanhamentos': [acomp.to_dict() for acomp in acompanhamentos]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cardapio_bp.route('/api/cardapio', methods=['POST'])
def criar_prato():
    """Cria um novo prato no cardápio"""
    try:
        data = request.get_json()
        
        if not data or not data.get('nome') or not data.get('preco'):
            return jsonify({
                'success': False,
                'error': 'Nome e preço são obrigatórios'
            }), 400
        
        prato = Prato(
            nome=data['nome'],
            preco=float(data['preco']),
            descricao=data.get('descricao', ''),
            ativo=data.get('ativo', True)
        )
        
        db.session.add(prato)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'prato': prato.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cardapio_bp.route('/api/cardapio/<int:prato_id>', methods=['PUT'])
def atualizar_prato(prato_id):
    """Atualiza um prato existente"""
    try:
        prato = Prato.query.get_or_404(prato_id)
        data = request.get_json()
        
        if 'nome' in data:
            prato.nome = data['nome']
        if 'preco' in data:
            prato.preco = float(data['preco'])
        if 'descricao' in data:
            prato.descricao = data['descricao']
        if 'ativo' in data:
            prato.ativo = data['ativo']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'prato': prato.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cardapio_bp.route('/api/cardapio/<int:prato_id>', methods=['DELETE'])
def deletar_prato(prato_id):
    """Desativa um prato (soft delete)"""
    try:
        prato = Prato.query.get_or_404(prato_id)
        prato.ativo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prato desativado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
