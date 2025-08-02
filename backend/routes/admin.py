from flask import Blueprint, jsonify, request, session
from models import db, Usuario, Prato, Acompanhamento, Pedido, MovimentacaoCaixa
from models import TipoUsuario, StatusPedido
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def require_admin(f):
    """Decorator para rotas que requerem acesso de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Acesso não autorizado - faça login'
            }), 401
        
        user = Usuario.query.get(user_id)
        if not user or user.tipo != TipoUsuario.ADMIN:
            return jsonify({
                'success': False,
                'error': 'Acesso negado - apenas administradores'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Login do administrador"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username e senha são obrigatórios'
            }), 400
        
        user = Usuario.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Credenciais inválidas'
            }), 401
        
        if not user.ativo:
            return jsonify({
                'success': False,
                'error': 'Usuário desativado'
            }), 401
        
        # Atualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Criar sessão
        session['user_id'] = user.id
        session['user_type'] = user.tipo.value
        
        return jsonify({
            'success': True,
            'message': 'Login realizado com sucesso',
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Logout do administrador"""
    try:
        session.clear()
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@require_admin
def admin_dashboard():
    """Dashboard administrativo com estatísticas gerais"""
    try:
        # Estatísticas gerais
        total_pedidos = Pedido.query.count()
        total_pratos = Prato.query.filter_by(ativo=True).count()
        total_usuarios = Usuario.query.filter_by(ativo=True).count()
        
        # Pedidos por status
        pedidos_por_status = {}
        for status in StatusPedido:
            count = Pedido.query.filter_by(status=status).count()
            pedidos_por_status[status.value] = count
        
        # Receita total
        receita_total = db.session.query(db.func.sum(MovimentacaoCaixa.valor)).filter(
            MovimentacaoCaixa.tipo == 'entrada'
        ).scalar() or 0
        
        # Pedidos hoje
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        pedidos_hoje = Pedido.query.filter(Pedido.created_at >= hoje).count()
        
        return jsonify({
            'success': True,
            'dashboard': {
                'total_pedidos': total_pedidos,
                'total_pratos': total_pratos,
                'total_usuarios': total_usuarios,
                'pedidos_por_status': pedidos_por_status,
                'receita_total': float(receita_total),
                'pedidos_hoje': pedidos_hoje
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/admin/usuarios', methods=['GET'])
@require_admin
def listar_usuarios():
    """Lista todos os usuários"""
    try:
        usuarios = Usuario.query.all()
        return jsonify({
            'success': True,
            'usuarios': [user.to_dict() for user in usuarios]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/admin/usuarios', methods=['POST'])
@require_admin
def criar_usuario():
    """Cria um novo usuário"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password', 'nome_completo', 'tipo']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Campo {field} é obrigatório'
                }), 400
        
        # Verificar se username já existe
        if Usuario.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'Username já existe'
            }), 400
        
        # Verificar se email já existe
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email já existe'
            }), 400
        
        user = Usuario(
            username=data['username'],
            email=data['email'],
            nome_completo=data['nome_completo'],
            tipo=TipoUsuario(data['tipo']),
            ativo=data.get('ativo', True)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'usuario': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/admin/usuarios/<int:user_id>', methods=['PUT'])
@require_admin
def atualizar_usuario(user_id):
    """Atualiza um usuário"""
    try:
        user = Usuario.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'username' in data:
            # Verificar se novo username já existe
            existing = Usuario.query.filter_by(username=data['username']).first()
            if existing and existing.id != user_id:
                return jsonify({
                    'success': False,
                    'error': 'Username já existe'
                }), 400
            user.username = data['username']
        
        if 'email' in data:
            # Verificar se novo email já existe
            existing = Usuario.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({
                    'success': False,
                    'error': 'Email já existe'
                }), 400
            user.email = data['email']
        
        if 'nome_completo' in data:
            user.nome_completo = data['nome_completo']
        
        if 'tipo' in data:
            user.tipo = TipoUsuario(data['tipo'])
        
        if 'ativo' in data:
            user.ativo = data['ativo']
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'usuario': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/api/admin/usuarios/<int:user_id>', methods=['DELETE'])
@require_admin
def deletar_usuario(user_id):
    """Desativa um usuário (soft delete)"""
    try:
        user = Usuario.query.get_or_404(user_id)
        
        # Não permitir deletar o próprio usuário
        if user.id == session.get('user_id'):
            return jsonify({
                'success': False,
                'error': 'Não é possível deletar seu próprio usuário'
            }), 400
        
        user.ativo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuário desativado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
