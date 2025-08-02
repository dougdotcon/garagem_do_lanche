#!/usr/bin/env python3
"""
Script de teste para a API da Garagem do Lanche
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Testa se a API está funcionando"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print("🔍 Testando health check...")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_cardapio():
    """Testa endpoints do cardápio"""
    try:
        print("\n🍔 Testando cardápio...")
        response = requests.get(f"{BASE_URL}/api/cardapio")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Pratos encontrados: {len(data.get('pratos', []))}")
        
        if data.get('pratos'):
            print(f"Primeiro prato: {data['pratos'][0]['nome']} - R$ {data['pratos'][0]['preco']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no teste do cardápio: {e}")
        return False

def test_acompanhamentos():
    """Testa endpoints dos acompanhamentos"""
    try:
        print("\n🥗 Testando acompanhamentos...")
        response = requests.get(f"{BASE_URL}/api/acompanhamentos")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Acompanhamentos encontrados: {len(data.get('acompanhamentos', []))}")
        
        if data.get('acompanhamentos'):
            for acomp in data['acompanhamentos']:
                print(f"  {acomp['icone']} {acomp['nome']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no teste dos acompanhamentos: {e}")
        return False

def test_criar_pedido():
    """Testa criação de pedido"""
    try:
        print("\n📝 Testando criação de pedido...")
        
        pedido_data = {
            "nome": "João Teste",
            "telefone": "(21) 99999-9999",
            "rua": "Rua de Teste",
            "numero": "123",
            "bairro": "Centro",
            "cep": "25000-000",
            "complemento": "Teste",
            "prato_id": 1,
            "acompanhamento_id": 1,
            "forma_pagamento": "Pix",
            "observacoes": "Pedido de teste"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/pedidos",
            json=pedido_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 201:
            print(f"✅ Pedido criado com ID: {data['pedido']['id']}")
            print(f"Total: R$ {data['pedido']['valor_total']}")
            return data['pedido']['id']
        else:
            print(f"❌ Erro: {data.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Erro no teste de criação de pedido: {e}")
        return None

def test_listar_pedidos():
    """Testa listagem de pedidos"""
    try:
        print("\n📋 Testando listagem de pedidos...")
        response = requests.get(f"{BASE_URL}/api/pedidos")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Pedidos encontrados: {len(data.get('pedidos', []))}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no teste de listagem de pedidos: {e}")
        return False

def test_caixa():
    """Testa endpoints do caixa"""
    try:
        print("\n💰 Testando caixa...")
        response = requests.get(f"{BASE_URL}/api/caixa/dashboard")
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            dashboard = data.get('dashboard', {})
            print(f"Vendas hoje: R$ {dashboard.get('vendas_hoje', 0)}")
            print(f"Pedidos hoje: {dashboard.get('pedidos_hoje', 0)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no teste do caixa: {e}")
        return False

def test_auth():
    """Testa autenticação"""
    try:
        print("\n🔐 Testando autenticação...")
        
        # Teste com senha correta
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"senha": "garagem2025"},
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status login: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login realizado com sucesso")
        
        # Teste verificação de auth
        response = requests.get(f"{BASE_URL}/api/auth/check")
        print(f"Status check: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de autenticação: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 Iniciando testes da API Garagem do Lanche")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Cardápio", test_cardapio),
        ("Acompanhamentos", test_acompanhamentos),
        ("Criar Pedido", test_criar_pedido),
        ("Listar Pedidos", test_listar_pedidos),
        ("Caixa", test_caixa),
        ("Autenticação", test_auth)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DOS TESTES")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("🎉 Todos os testes passaram! API está funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração da API.")

if __name__ == "__main__":
    main()
