# leituras/views_dashboard.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from collections import defaultdict
from .models import Contador, Leitura
import json

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('/admin/')

    contadores = Contador.objects.filter(user=request.user, active=True)
    if not contadores.exists():
        return render(request, 'dashboard.html', {'no_device': True})

    # SELETOR DE CONTADOR
    contador_id = request.GET.get('contador')
    if contador_id:
        try:
            contador_atual = contadores.get(id=contador_id)
        except Contador.DoesNotExist:
            contador_atual = contadores.first()
    else:
        contador_atual = contadores.first()

    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # === DADOS DO CONTADOR SELECIONADO ===
    leituras_mes = Leitura.objects.filter(
        contador=contador_atual,
        captured_at__gte=inicio_mes
    ).order_by('captured_at')

    total_mes_m3 = round((leituras_mes.aggregate(t=Sum('volume'))['t'] or 0) / 1000, 3)
    total_geral_m3 = round((Leitura.objects.filter(contador=contador_atual)
                           .aggregate(t=Sum('volume'))['t'] or 0) / 1000, 3)

    # === GRÁFICO ===
    dados_diarios = defaultdict(float)
    current_day = inicio_mes
    while current_day.date() <= hoje.date():
        dia_str = current_day.strftime('%d/%m')
        vol = leituras_mes.filter(captured_at__date=current_day.date()).aggregate(v=Sum('volume'))['v'] or 0
        dados_diarios[dia_str] = round(vol / 1000, 3)
        current_day += timedelta(days=1)

    # === HISTÓRICO MENSAL DO CONTADOR ATUAL ===
    historico_mensal = []
    anos_disponiveis = set()

    todas_leituras = Leitura.objects.filter(contador=contador_atual).order_by('captured_at')
    if todas_leituras.exists():
        mes_atual = None
        total_mes = 0
        ano_atual = None
        for l in todas_leituras:
            ano = l.captured_at.year
            mes_key = l.captured_at.strftime('%Y-%m')
            anos_disponiveis.add(ano)

            if mes_key != mes_atual:
                if mes_atual:
                    historico_mensal.append({
                        'ano': ano_atual,
                        'mes': datetime.strptime(mes_atual, '%Y-%m').strftime('%B %Y'),
                        'total': round(total_mes / 1000, 3)
                    })
                mes_atual = mes_key
                total_mes = 0
                ano_atual = ano
            total_mes += float(l.volume or 0)

        if mes_atual:
            historico_mensal.append({
                'ano': ano_atual,
                'mes': datetime.strptime(mes_atual, '%Y-%m').strftime('%B %Y'),
                'total': round(total_mes / 1000, 3)
            })

    context = {
        'contadores': contadores,
        'contador_atual': contador_atual,
        'total_mes': total_mes_m3,
        'total_geral': total_geral_m3,
        'ultima_leitura': leituras_mes.last(),
        'chart_labels': list(dados_diarios.keys()),
        'chart_data': list(dados_diarios.values()),
        'mes_atual': hoje.strftime('%B %Y'),
        'historico_mensal': historico_mensal,
        'anos_disponiveis': sorted(anos_disponiveis),
        'chart_labels': json.dumps(list(dados_diarios.keys())),
        'chart_data': json.dumps(list(dados_diarios.values())),
    }
    return render(request, 'dashboard.html', context)