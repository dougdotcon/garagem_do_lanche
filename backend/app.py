from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from database import init_database

# Importar blueprints
from routes.cardapio import cardapio_bp
from routes.pedidos import pedidos_bp
from routes.caixa import caixa_bp
from routes.auth import auth_bp

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar CORS
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(cardapio_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(caixa_bp)
    app.register_blueprint(auth_bp)
    
    # Rota de teste
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'message': 'API da Garagem do Lanche está funcionando!',
            'version': '1.0.0'
        })
    
    # Rota para informações da API
    @app.route('/api/info', methods=['GET'])
    def api_info():
        return jsonify({
            'success': True,
            'api': 'Garagem do Lanche API',
            'version': '1.0.0',
            'endpoints': {
                'cardapio': '/api/cardapio',
                'acompanhamentos': '/api/acompanhamentos',
                'pedidos': '/api/pedidos',
                'caixa': '/api/caixa',
                'auth': '/api/auth'
            }
        })
    
    # Handler para erros 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint não encontrado'
        }), 404
    
    # Handler para erros 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500
    
    # Inicializar banco de dados
    init_database(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🍔 Iniciando API da Garagem do Lanche...")
    print("📊 Banco de dados SQLite configurado")
    print("🌐 CORS habilitado para frontend")
    print("🔗 API disponível em: http://localhost:5000")
    print("\n📋 Endpoints disponíveis:")
    print("   GET  /api/health - Status da API")
    print("   GET  /api/info - Informações da API")
    print("   GET  /api/cardapio - Listar pratos")
    print("   GET  /api/acompanhamentos - Listar acompanhamentos")
    print("   POST /api/pedidos - Criar pedido")
    print("   GET  /api/pedidos - Listar pedidos")
    print("   GET  /api/pedidos/cozinha - Pedidos para cozinha")
    print("   GET  /api/caixa/relatorio - Relatório do caixa")
    print("   GET  /api/caixa/dashboard - Dashboard do caixa")
    print("   POST /api/auth/login - Login da cozinha")
    print("\n🚀 Servidor rodando...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
