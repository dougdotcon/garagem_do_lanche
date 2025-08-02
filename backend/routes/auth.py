from flask import Blueprint, jsonify, request, session
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Autentica acesso à cozinha"""
    try:
        data = request.get_json()
        
        if not data or not data.get('senha'):
            return jsonify({
                'success': False,
                'error': 'Senha é obrigatória'
            }), 400
        
        if data['senha'] == Config.SENHA_COZINHA:
            session['cozinha_autenticada'] = True
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'authenticated': True
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Senha incorreta'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Faz logout da cozinha"""
    try:
        session.pop('cozinha_autenticada', None)
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth_bp.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Verifica se está autenticado"""
    try:
        authenticated = session.get('cozinha_autenticada', False)
        return jsonify({
            'success': True,
            'authenticated': authenticated
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def require_auth(f):
    """Decorator para rotas que requerem autenticação"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('cozinha_autenticada'):
            return jsonify({
                'success': False,
                'error': 'Acesso não autorizado'
            }), 401
        return f(*args, **kwargs)
    return decorated_function
