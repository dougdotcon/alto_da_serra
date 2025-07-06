from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json

def login_view(request):
    """View para login do usuário"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Chama a API de login
            response = requests.post(f"{settings.API_BASE_URL}/login", json={
                "email": email,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                # Salva dados do usuário na sessão
                request.session['autenticado'] = True
                request.session['usuario_nome'] = data['nome']
                request.session['usuario_tipo'] = data['tipo']
                request.session['usuario_user'] = data['user']

                messages.success(request, 'Login realizado com sucesso!')
                return redirect('mesas:dashboard')
            else:
                messages.error(request, 'Credenciais inválidas')

        except Exception as e:
            messages.error(request, f'Erro ao conectar com o servidor: {str(e)}')

    return render(request, 'mesas/login.html')

def logout_view(request):
    """View para logout do usuário"""
    request.session.flush()
    messages.info(request, 'Logout realizado com sucesso!')
    return redirect('mesas:login')

def dashboard_view(request):
    """View principal do dashboard"""
    if not request.session.get('autenticado'):
        return redirect('mesas:login')

    try:
        # Busca dados das mesas
        mesas_response = requests.get(f"{settings.API_BASE_URL}/mesas")
        mesas = mesas_response.json() if mesas_response.status_code == 200 else []

        # Busca configuração
        config_response = requests.get(f"{settings.API_BASE_URL}/configuracao")
        config = config_response.json() if config_response.status_code == 200 else {}

    except Exception as e:
        messages.error(request, f'Erro ao carregar dados: {str(e)}')
        mesas = []
        config = {}

    context = {
        'mesas': mesas,
        'config': config,
        'usuario_nome': request.session.get('usuario_nome', ''),
        'usuario_tipo': request.session.get('usuario_tipo', ''),
    }

    return render(request, 'mesas/dashboard.html', context)

def mesa_detail_view(request, mesa_id):
    """View para detalhes de uma mesa específica"""
    if not request.session.get('autenticado'):
        return redirect('mesas:login')

    try:
        # Busca dados da mesa específica
        mesas_response = requests.get(f"{settings.API_BASE_URL}/mesas")
        mesas = mesas_response.json() if mesas_response.status_code == 200 else []
        mesa = next((m for m in mesas if m['id'] == mesa_id), None)

        if not mesa:
            messages.error(request, 'Mesa não encontrada')
            return redirect('mesas:dashboard')

        # Busca consumo da mesa
        consumo_response = requests.get(f"{settings.API_BASE_URL}/consumo/{mesa_id}")
        consumo = consumo_response.json() if consumo_response.status_code == 200 else []

        # Busca produtos disponíveis
        produtos_response = requests.get(f"{settings.API_BASE_URL}/produtos")
        produtos = produtos_response.json() if produtos_response.status_code == 200 else []

    except Exception as e:
        messages.error(request, f'Erro ao carregar dados da mesa: {str(e)}')
        return redirect('mesas:dashboard')

    context = {
        'mesa': mesa,
        'consumo': consumo,
        'produtos': produtos,
        'total_consumo': sum(item['total'] for item in consumo),
        'usuario_nome': request.session.get('usuario_nome', ''),
        'usuario_tipo': request.session.get('usuario_tipo', ''),
    }

    return render(request, 'mesas/mesa_detail.html', context)

def produtos_view(request):
    """View para listagem de produtos"""
    if not request.session.get('autenticado'):
        return redirect('mesas:login')

    try:
        produtos_response = requests.get(f"{settings.API_BASE_URL}/produtos")
        produtos = produtos_response.json() if produtos_response.status_code == 200 else []
    except Exception as e:
        messages.error(request, f'Erro ao carregar produtos: {str(e)}')
        produtos = []

    context = {
        'produtos': produtos,
        'usuario_nome': request.session.get('usuario_nome', ''),
        'usuario_tipo': request.session.get('usuario_tipo', ''),
    }

    return render(request, 'mesas/produtos.html', context)

def estoque_view(request):
    """View para página de gestão de estoque"""
    if not request.session.get('autenticado'):
        return redirect('mesas:login')

    try:
        produtos_response = requests.get(f"{settings.API_BASE_URL}/produtos")
        produtos = produtos_response.json() if produtos_response.status_code == 200 else []
    except Exception as e:
        messages.error(request, f'Erro ao carregar produtos: {str(e)}')
        produtos = []

    context = {
        'produtos': produtos,
        'usuario_nome': request.session.get('usuario_nome', ''),
        'usuario_tipo': request.session.get('usuario_tipo', ''),
    }

    return render(request, 'mesas/estoque.html', context)

def cozinha_view(request):
    """View para página de gestão da cozinha"""
    if not request.session.get('autenticado'):
        return redirect('mesas:login')

    context = {
        'usuario_nome': request.session.get('usuario_nome', ''),
        'usuario_tipo': request.session.get('usuario_tipo', ''),
    }

    return render(request, 'mesas/cozinha.html', context)

# API Views para integração com o frontend
@csrf_exempt
def api_mesas(request):
    """API para buscar dados das mesas"""
    try:
        response = requests.get(f"{settings.API_BASE_URL}/mesas")
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_consumo(request, mesa_id):
    """API para buscar consumo de uma mesa"""
    try:
        response = requests.get(f"{settings.API_BASE_URL}/consumo/{mesa_id}")
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_produtos(request):
    """API para buscar produtos"""
    try:
        response = requests.get(f"{settings.API_BASE_URL}/produtos")
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_adicionar_pedido(request):
    """API para adicionar pedido"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = requests.post(f"{settings.API_BASE_URL}/adicionar_pedido", json=data)
            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_abater_consumo(request):
    """API para abater consumo"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = requests.post(f"{settings.API_BASE_URL}/abater_consumo", json=data)
            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_atualizar_mesa(request):
    """API para atualizar mesa"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = requests.post(f"{settings.API_BASE_URL}/atualizar_mesa", json=data)
            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_finalizar_conta(request):
    """API para finalizar conta de uma mesa"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"FINALIZAR CONTA - Dados recebidos: {data}")

            # Dados para finalização
            finalizacao_data = {
                'mesa_id': data.get('mesa_id'),
                'forma_pagamento': data.get('forma_pagamento'),
                'valor_pago': data.get('valor_pago'),
                'desconto': data.get('desconto', 0),
                'observacoes': data.get('observacoes', ''),
                'total': data.get('total', 0)
            }
            print(f"FINALIZAR CONTA - Enviando para API: {finalizacao_data}")

            response = requests.post(f"{settings.API_BASE_URL}/finalizar_conta", json=finalizacao_data)
            print(f"FINALIZAR CONTA - Status: {response.status_code}, Resposta: {response.text}")

            if response.status_code == 200:
                return JsonResponse({'success': True, 'message': 'Conta finalizada com sucesso'})
            else:
                error_data = response.json() if response.content else {'detail': 'Erro desconhecido'}
                return JsonResponse({'error': error_data.get('detail', 'Erro ao finalizar conta')}, status=400)
        except Exception as e:
            print(f"FINALIZAR CONTA - Exceção: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_editar_mesa(request):
    """API para editar dados de uma mesa"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"EDITAR MESA - Dados recebidos: {data}")

            # Dados para edição
            edicao_data = {
                'mesa_id': data.get('mesa_id'),
                'cliente': data.get('cliente', ''),
                'cpf_cnpj': data.get('cpf_cnpj', '')
            }
            print(f"EDITAR MESA - Enviando para API: {edicao_data}")

            response = requests.post(f"{settings.API_BASE_URL}/editar-mesa", json=edicao_data)
            print(f"EDITAR MESA - Status: {response.status_code}, Resposta: {response.text}")

            if response.status_code == 200:
                return JsonResponse({'success': True, 'message': 'Mesa atualizada com sucesso'})
            else:
                error_data = response.json() if response.content else {'detail': 'Erro desconhecido'}
                return JsonResponse({'error': error_data.get('detail', 'Erro ao atualizar mesa')}, status=400)
        except Exception as e:
            print(f"EDITAR MESA - Exceção: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
