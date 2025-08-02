#!/usr/bin/env python3
"""
Script para inicializar a API da Garagem do Lanche
"""

import os
import sys
from app import create_app

if __name__ == '__main__':
    # Verificar se o arquivo de banco existe
    db_path = 'garagem_lanche.db'
    if not os.path.exists(db_path):
        print("🗄️  Criando banco de dados SQLite...")
    
    # Criar aplicação
    app = create_app()
    
    # Configurações de desenvolvimento
    if len(sys.argv) > 1 and sys.argv[1] == '--prod':
        # Modo produção
        print("🚀 Iniciando em modo PRODUÇÃO")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        # Modo desenvolvimento
        print("🔧 Iniciando em modo DESENVOLVIMENTO")
        app.run(host='0.0.0.0', port=5000, debug=True)
