from flask import Blueprint, jsonify, request
from models import db, MovimentacaoCaixa, Pedido
from sqlalchemy import func, and_
from datetime import datetime, timedelta

caixa_bp = Blueprint('caixa', __name__)

@caixa_bp.route('/api/caixa/relatorio', methods=['GET'])
def relatorio_caixa():
    """Gera relatório do caixa com entradas, saídas e fiado"""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        # Se não especificado, usar o dia atual
        if not data_inicio:
            data_inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            data_inicio = datetime.fromisoformat(data_inicio)
            
        if not data_fim:
            data_fim = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            data_fim = datetime.fromisoformat(data_fim)
        
        # Query base
        query = MovimentacaoCaixa.query.filter(
            and_(
                MovimentacaoCaixa.created_at >= data_inicio,
                MovimentacaoCaixa.created_at <= data_fim
            )
        )
        
        # Calcular totais por tipo
        entradas = query.filter(MovimentacaoCaixa.tipo == 'entrada').all()
        saidas = query.filter(MovimentacaoCaixa.tipo == 'saida').all()
        fiados = query.filter(MovimentacaoCaixa.tipo == 'fiado').all()
        
        total_entradas = sum(mov.valor for mov in entradas)
        total_saidas = sum(mov.valor for mov in saidas)
        total_fiados = sum(mov.valor for mov in fiados)
        
        saldo = total_entradas - total_saidas
        
        # Movimentações detalhadas
        todas_movimentacoes = query.order_by(MovimentacaoCaixa.created_at.desc()).all()
        
        # Estatísticas de pedidos
        pedidos_periodo = Pedido.query.filter(
            and_(
                Pedido.created_at >= data_inicio,
                Pedido.created_at <= data_fim
            )
        ).all()
        
        total_pedidos = len(pedidos_periodo)
        ticket_medio = total_entradas / total_pedidos if total_pedidos > 0 else 0
        
        return jsonify({
            'success': True,
            'relatorio': {
                'periodo': {
                    'inicio': data_inicio.isoformat(),
                    'fim': data_fim.isoformat()
                },
                'resumo': {
                    'total_entradas': total_entradas,
                    'total_saidas': total_saidas,
                    'total_fiados': total_fiados,
                    'saldo': saldo,
                    'total_pedidos': total_pedidos,
                    'ticket_medio': round(ticket_medio, 2)
                },
                'movimentacoes': [mov.to_dict() for mov in todas_movimentacoes]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@caixa_bp.route('/api/caixa/movimentacao', methods=['POST'])
def criar_movimentacao():
    """Cria uma nova movimentação no caixa"""
    try:
        data = request.get_json()
        
        if not data or not data.get('tipo') or not data.get('valor'):
            return jsonify({
                'success': False,
                'error': 'Tipo e valor são obrigatórios'
            }), 400
        
        if data['tipo'] not in ['entrada', 'saida', 'fiado']:
            return jsonify({
                'success': False,
                'error': 'Tipo deve ser: entrada, saida ou fiado'
            }), 400
        
        movimentacao = MovimentacaoCaixa(
            tipo=data['tipo'],
            valor=float(data['valor']),
            descricao=data.get('descricao', ''),
            pedido_id=data.get('pedido_id')
        )
        
        db.session.add(movimentacao)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'movimentacao': movimentacao.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@caixa_bp.route('/api/caixa/dashboard', methods=['GET'])
def dashboard_caixa():
    """Retorna dados para dashboard do caixa"""
    try:
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        fim_hoje = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Vendas de hoje
        vendas_hoje = MovimentacaoCaixa.query.filter(
            and_(
                MovimentacaoCaixa.tipo == 'entrada',
                MovimentacaoCaixa.created_at >= hoje,
                MovimentacaoCaixa.created_at <= fim_hoje
            )
        ).all()
        
        total_hoje = sum(venda.valor for venda in vendas_hoje)
        
        # Pedidos de hoje
        pedidos_hoje = Pedido.query.filter(
            and_(
                Pedido.created_at >= hoje,
                Pedido.created_at <= fim_hoje
            )
        ).count()
        
        # Fiados pendentes
        fiados_pendentes = MovimentacaoCaixa.query.filter(
            MovimentacaoCaixa.tipo == 'fiado'
        ).all()
        
        total_fiados = sum(fiado.valor for fiado in fiados_pendentes)
        
        # Vendas dos últimos 7 dias
        sete_dias_atras = hoje - timedelta(days=7)
        vendas_semana = db.session.query(
            func.date(MovimentacaoCaixa.created_at).label('data'),
            func.sum(MovimentacaoCaixa.valor).label('total')
        ).filter(
            and_(
                MovimentacaoCaixa.tipo == 'entrada',
                MovimentacaoCaixa.created_at >= sete_dias_atras
            )
        ).group_by(func.date(MovimentacaoCaixa.created_at)).all()
        
        return jsonify({
            'success': True,
            'dashboard': {
                'vendas_hoje': total_hoje,
                'pedidos_hoje': pedidos_hoje,
                'fiados_pendentes': total_fiados,
                'ticket_medio_hoje': round(total_hoje / pedidos_hoje, 2) if pedidos_hoje > 0 else 0,
                'vendas_semana': [
                    {
                        'data': venda.data.isoformat(),
                        'total': float(venda.total)
                    } for venda in vendas_semana
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
