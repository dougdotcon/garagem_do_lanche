import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'garagem-do-lanche-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///garagem_lanche.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações específicas do sistema
    SENHA_COZINHA = "garagem2025"
    
    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:5500", "*"]
