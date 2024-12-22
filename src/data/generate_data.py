import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import time
from tqdm import tqdm
import os

ordem_colunas = {
    'produtos': ['produto_id', 'nome', 'categoria', 'preco_base', 'custo', 
                 'colecao', 'e_atemporal', 'meses_venda', 'data_inclusao'],
    
    'clientes': ['cliente_id', 'data_cadastro', 'idade', 'genero', 'estado_civil', 
                 'estado', 'faixa_renda', 'dispositivo_principal', 'canal_aquisicao', 
                 'tem_filhos', 'frequencia_compras'],
    
    'vendas': ['venda_id', 'cliente_id', 'data_venda', 'valor_total', 'desconto', 
               'valor_final', 'metodo_pagamento', 'parcelas', 'status'],
    
    'itens_venda': ['venda_id', 'produto_id', 'quantidade', 'valor_unitario', 
                    'valor_total', 'margem'],
    
    'carrinhos_abandonados': ['cliente_id', 'data_abandono', 'valor_total', 'num_itens', 
                             'dispositivo', 'razao_abandono', 'itens'],
    
    'navegacao': ['cliente_id', 'produto_id', 'data_sessao', 'tempo_visualizacao', 
                  'adicionou_carrinho', 'dispositivo', 'origem_trafego', 'horario', 
                  'dia_semana'],
    
    'campanhas': ['campanha_id', 'nome', 'plataforma', 'tipo_midia', 'objetivo', 
                  'data_inicio', 'data_fim', 'status', 'budget_planejado', 'segmentacao'],
    
    'metricas_campanhas': ['campanha_id', 'data_metrica', 'impressoes', 'cliques', 'ctr', 
                          'cpc', 'cpm', 'custo_total', 'conversoes', 'valor_conversoes', 
                          'roas', 'bounce_rate', 'visualizacoes_pagina'],
    
    'criativos': ['criativo_id', 'campanha_id', 'tipo', 'formato', 'nome', 'status', 
                  'data_criacao'],
    
    'metricas_criativos': ['criativo_id', 'data_metrica', 'impressoes', 'cliques', 
                          'ctr', 'custo', 'conversoes']
}

def log_progress(message):
    """Função auxiliar para log com timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def gerar_produtos():
    """Gera catálogo de produtos com informações de coleção/estação"""
    log_progress("Iniciando geração de produtos...")
    start_time = time.time()
    
    categorias = {
        'Camisetas': {'min_price': 29.99, 'max_price': 129.99, 'qtd': 100},
        'Calças': {'min_price': 89.99, 'max_price': 299.99, 'qtd': 80},
        'Vestidos': {'min_price': 99.99, 'max_price': 499.99, 'qtd': 120},
        'Acessórios': {'min_price': 19.99, 'max_price': 199.99, 'qtd': 150},
        'Sapatos': {'min_price': 99.99, 'max_price': 599.99, 'qtd': 100},
        'Blusas': {'min_price': 49.99, 'max_price': 199.99, 'qtd': 90},
        'Saias': {'min_price': 79.99, 'max_price': 249.99, 'qtd': 70},
        'Jaquetas': {'min_price': 149.99, 'max_price': 699.99, 'qtd': 60},
        'Lingerie': {'min_price': 29.99, 'max_price': 149.99, 'qtd': 100},
        'Moda Praia': {'min_price': 59.99, 'max_price': 249.99, 'qtd': 80}
    }
    
    colecoes = {
        'Verão': ['Dezembro', 'Janeiro', 'Fevereiro', 'Março'],
        'Outono': ['Março', 'Abril', 'Maio', 'Junho'],
        'Inverno': ['Junho', 'Julho', 'Agosto', 'Setembro'],
        'Primavera': ['Setembro', 'Outubro', 'Novembro', 'Dezembro']
    }
    
    produtos = []
    total_produtos = sum(info['qtd'] for info in categorias.values())
    log_progress(f"Gerando {total_produtos} produtos em {len(categorias)} categorias...")
    
    produto_id = 1
    for categoria, info in tqdm(categorias.items(), desc="Categorias"):
        for _ in range(info['qtd']):
            colecao_principal = random.choice(list(colecoes.keys()))
            e_atemporal = random.random() < 0.3
            
            preco_base = random.uniform(info['min_price'], info['max_price'])
            if not e_atemporal:
                preco_base *= 1.2
            
            nome = f"{categoria} Modelo {produto_id}"
            custo = round(preco_base * 0.4, 2)
            
            produtos.append({
                'produto_id': produto_id,
                'nome': nome,
                'categoria': categoria,
                'preco_base': round(preco_base, 2),
                'custo': custo,
                'colecao': colecao_principal,
                'e_atemporal': e_atemporal,
                'meses_venda': ','.join(colecoes[colecao_principal]) if not e_atemporal else 'Todos',
                'data_inclusao': datetime.now() - timedelta(days=random.randint(1, 365))
            })
            produto_id += 1
    
    df = pd.DataFrame(produtos)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de produtos concluída em {duration} segundos")
    
    return df

def gerar_clientes(num_clientes=100000):
    """Gera dados de clientes com informações demográficas expandidas"""
    log_progress(f"Iniciando geração de {num_clientes:,} clientes...")
    start_time = time.time()
    
    dispositivos = ['Mobile', 'Desktop', 'Tablet']
    dispositivos_weights = [0.65, 0.30, 0.05]
    
    canais = ['Google Organic', 'Google Ads', 'Facebook Ads', 'Instagram Ads', 
              'Direct', 'Email', 'Referral', 'Instagram Organic', 'Facebook Organic']
    canais_weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.05, 0.05, 0.03, 0.02]
    
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'SC', 'DF', 'GO', 'PE', 'CE', 'PA', 'ES', 'MT', 'MS']
    estados_weights = [0.3, 0.15, 0.1, 0.08, 0.07, 0.05, 0.05, 0.04, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02]
    
    estado_civil = ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União Estável']
    estado_civil_weights = [0.45, 0.35, 0.10, 0.03, 0.07]
    
    faixas_renda = ['Até 2.000', '2.001-4.000', '4.001-8.000', '8.001-12.000', 'Acima de 12.000']
    renda_weights = [0.25, 0.35, 0.25, 0.10, 0.05]
    
    clientes = []
    for cliente_id in tqdm(range(1, num_clientes + 1), desc="Clientes"):
        idade = random.randint(18, 70)
        genero = random.choices(['F', 'M', 'O'], weights=[0.65, 0.30, 0.05])[0]
        estado_civil_cliente = random.choices(estado_civil, weights=estado_civil_weights)[0]
        
        # Ajusta probabilidades de renda baseado na idade
        renda_weights_adj = renda_weights.copy()
        if idade < 25:
            renda_weights_adj = [0.40, 0.35, 0.15, 0.07, 0.03]
        elif idade > 45:
            renda_weights_adj = [0.15, 0.25, 0.35, 0.15, 0.10]
        
        clientes.append({
            'cliente_id': cliente_id,
            'data_cadastro': datetime.now() - timedelta(days=random.randint(1, 365)),
            'idade': idade,
            'genero': genero,
            'estado_civil': estado_civil_cliente,
            'estado': random.choices(estados, weights=estados_weights)[0],
            'faixa_renda': random.choices(faixas_renda, weights=renda_weights_adj)[0],
            'dispositivo_principal': random.choices(dispositivos, weights=dispositivos_weights)[0],
            'canal_aquisicao': random.choices(canais, weights=canais_weights)[0],
            'tem_filhos': random.choices([True, False], weights=[0.4, 0.6])[0],
            'frequencia_compras': random.choices(['Baixa', 'Média', 'Alta'], weights=[0.4, 0.4, 0.2])[0]
        })
    
    df = pd.DataFrame(clientes)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de clientes concluída em {duration} segundos")
    
    return df
def calcular_preco_ajustado(preco_base, data_venda, colecao, e_atemporal):
    """Calcula preço ajustado baseado na sazonalidade"""
    mes = data_venda.month
    dia = data_venda.day
    
    fator = 1.0
    
    if not e_atemporal:
        estacoes = {
            'Verão': [12, 1, 2, 3],
            'Outono': [3, 4, 5, 6],
            'Inverno': [6, 7, 8, 9],
            'Primavera': [9, 10, 11, 12]
        }
        
        if mes in estacoes[colecao]:
            fator *= 1.2
        else:
            fator *= 0.8
    
    # Ajustes por datas especiais
    if (mes == 11 and dia >= 25) or (mes == 11 and dia <= 30):  # Black Friday
        fator *= 0.6
    elif mes == 12 and dia >= 15:  # Natal
        fator *= 0.85
    elif mes == 5 and dia <= 14:  # Dia das Mães
        fator *= 0.9
    elif mes == 8 and dia <= 13:  # Dia dos Pais
        fator *= 0.9
    elif mes == 6 and dia <= 12:  # Dia dos Namorados
        fator *= 0.9
    
    fator *= random.uniform(0.95, 1.05)
    
    return round(preco_base * fator, 2)

def gerar_vendas(df_produtos, df_clientes, num_vendas=500000):
    """Gera histórico de vendas com comportamentos específicos por perfil"""
    log_progress(f"Iniciando geração de {num_vendas:,} vendas...")
    start_time = time.time()
    
    vendas = []
    itens_venda = []
    carrinhos_abandonados = []
    
    metodos_pagamento = ['Cartão de Crédito', 'Boleto', 'Pix']
    metodos_weights = [0.70, 0.15, 0.15]
    
    status_pedido = ['Aprovado', 'Cancelado', 'Em processamento', 'Devolvido']
    status_weights = [0.85, 0.08, 0.05, 0.02]
    
    # Carrinhos abandonados
    num_carrinhos_abandonados = int(num_vendas * 0.7)
    log_progress(f"Gerando {num_carrinhos_abandonados:,} carrinhos abandonados...")
    
    razoes_abandono = [
        'Preço alto',
        'Frete caro',
        'Indecisão',
        'Problemas técnicos',
        'Comparando preços',
        'Método de pagamento',
        'Tempo de entrega'
    ]
    
    for _ in tqdm(range(num_carrinhos_abandonados), desc="Carrinhos abandonados"):
        cliente = df_clientes.sample(n=1).iloc[0]
        data_abandono = datetime.now() - timedelta(days=random.randint(1, 365))
        
        num_itens = random.choices(range(1, 6), weights=[0.4, 0.3, 0.2, 0.07, 0.03])[0]
        produtos_carrinho = df_produtos.sample(n=num_itens)
        
        valor_total = 0
        itens = []
        
        for _, produto in produtos_carrinho.iterrows():
            preco_ajustado = calcular_preco_ajustado(
                produto['preco_base'], 
                data_abandono,
                produto['colecao'],
                produto['e_atemporal']
            )
            quantidade = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
            valor_item = preco_ajustado * quantidade
            valor_total += valor_item
            
            itens.append({
                'produto_id': produto['produto_id'],
                'quantidade': quantidade,
                'valor_unitario': preco_ajustado
            })
        
        carrinhos_abandonados.append({
            'cliente_id': cliente['cliente_id'],
            'data_abandono': data_abandono,
            'valor_total': valor_total,
            'num_itens': num_itens,
            'dispositivo': cliente['dispositivo_principal'],
            'razao_abandono': random.choice(razoes_abandono),
            'itens': json.dumps(itens)
        })
    
    # Vendas concluídas
    log_progress(f"Gerando {num_vendas:,} vendas concluídas...")
    for venda_id in tqdm(range(1, num_vendas + 1), desc="Vendas"):
        cliente = df_clientes.sample(n=1).iloc[0]
        data_venda = datetime.now() - timedelta(days=random.randint(1, 365))
        
        if cliente['frequencia_compras'] == 'Alta':
            num_itens = random.choices(range(1, 9), weights=[0.2, 0.2, 0.2, 0.15, 0.1, 0.05, 0.05, 0.05])[0]
        else:
            num_itens = random.choices(range(1, 6), weights=[0.4, 0.3, 0.2, 0.07, 0.03])[0]
        
        produtos_venda = df_produtos.sample(n=num_itens)
        valor_total = 0
        
        for _, produto in produtos_venda.iterrows():
            preco_ajustado = calcular_preco_ajustado(
                produto['preco_base'],
                data_venda,
                produto['colecao'],
                produto['e_atemporal']
            )
            
            quantidade = random.choices([1, 2, 3, 4], weights=[0.7, 0.2, 0.07, 0.03])[0]
            valor_item = preco_ajustado * quantidade
            valor_total += valor_item
            
            itens_venda.append({
                'venda_id': venda_id,
                'produto_id': produto['produto_id'],
                'quantidade': quantidade,
                'valor_unitario': preco_ajustado,
                'valor_total': valor_item,
                'margem': valor_item - (produto['custo'] * quantidade)
            })
        
        if 'Até' in cliente['faixa_renda']:
            metodos_weights = [0.50, 0.30, 0.20]
        elif 'Acima' in cliente['faixa_renda']:
            metodos_weights = [0.85, 0.05, 0.10]
        
        vendas.append({
            'venda_id': venda_id,
            'cliente_id': cliente['cliente_id'],
            'data_venda': data_venda,
            'valor_total': valor_total,
            'desconto': 0,
            'valor_final': valor_total,
            'metodo_pagamento': random.choices(metodos_pagamento, weights=metodos_weights)[0],
            'parcelas': random.choices(range(1, 13), weights=[0.3, 0.1, 0.2, 0.1, 0.1, 0.05, 0.05, 0.03, 0.02, 0.02, 0.02, 0.01])[0],
            'status': random.choices(status_pedido, weights=status_weights)[0]
        })
    
    df_vendas = pd.DataFrame(vendas)
    df_itens_venda = pd.DataFrame(itens_venda)
    df_carrinhos = pd.DataFrame(carrinhos_abandonados)
    
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de vendas concluída em {duration} segundos")
    log_progress(f"- Total de vendas: {len(df_vendas):,}")
    log_progress(f"- Total de itens: {len(df_itens_venda):,}")
    log_progress(f"- Total de carrinhos abandonados: {len(df_carrinhos):,}")
    
    return df_vendas, df_itens_venda, df_carrinhos

def gerar_navegacao(df_clientes, df_produtos, num_sessoes=2000000):
    """Gera dados de navegação com comportamentos específicos por perfil"""
    log_progress(f"Iniciando geração de {num_sessoes:,} sessões de navegação...")
    start_time = time.time()
    
    navegacao = []
    
    for _ in tqdm(range(num_sessoes), desc="Sessões de navegação"):
        cliente = df_clientes.sample(n=1).iloc[0]
        data_sessao = datetime.now() - timedelta(days=random.randint(1, 365))
        
        # Ajusta comportamento baseado no perfil
        if cliente['frequencia_compras'] == 'Alta':
            num_produtos = random.choices(range(1, 11), 
                                       weights=[0.1, 0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05])[0]
            prob_carrinho = 0.4
        else:
            num_produtos = random.choices(range(1, 8), 
                                       weights=[0.3, 0.25, 0.2, 0.1, 0.05, 0.05, 0.05])[0]
            prob_carrinho = 0.2
        
        produtos_vistos = df_produtos.sample(n=num_produtos)
        
        # Ajusta probabilidade baseado no estado civil
        if cliente['estado_civil'] == 'Solteiro(a)':
            categorias_interesse = ['Moda Praia', 'Vestidos', 'Acessórios']
        elif cliente['estado_civil'] == 'Casado(a)':
            categorias_interesse = ['Vestidos', 'Calças', 'Blusas']
        else:
            categorias_interesse = list(set(produtos_vistos['categoria']))
        
        for _, produto in produtos_vistos.iterrows():
            tempo_produto = int(np.random.exponential(90 if produto['categoria'] in categorias_interesse else 45))
            tempo_produto = min(tempo_produto, 600)
            
            navegacao.append({
                'cliente_id': cliente['cliente_id'],
                'produto_id': produto['produto_id'],
                'data_sessao': data_sessao,
                'tempo_visualizacao': tempo_produto,
                'adicionou_carrinho': random.random() < (prob_carrinho * 1.5 if produto['categoria'] in categorias_interesse else prob_carrinho),
                'dispositivo': cliente['dispositivo_principal'],
                'origem_trafego': cliente['canal_aquisicao'],
                'horario': data_sessao.hour,
                'dia_semana': data_sessao.strftime('%A')
            })
    
    df = pd.DataFrame(navegacao)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de navegação concluída em {duration} segundos")
    log_progress(f"- Total de interações: {len(df):,}")
    
    return df

def gerar_campanhas(data_inicio=None, num_campanhas=50):
    """Gera dados de campanhas de marketing"""
    log_progress(f"Iniciando geração de {num_campanhas} campanhas...")
    start_time = time.time()
    
    if data_inicio is None:
        data_inicio = datetime.now() - timedelta(days=365)
    
    plataformas = {
        'Google Ads': {
            'tipos': ['Search', 'Display', 'Shopping'],
            'objetivos': ['Conversões', 'Tráfego', 'Reconhecimento'],
            'peso': 0.35
        },
        'Meta Ads': {
            'tipos': ['Feed', 'Stories', 'Reels', 'Catalog'],
            'objetivos': ['Conversões', 'Engajamento', 'Tráfego', 'Alcance'],
            'peso': 0.35
        },
        'TikTok Ads': {
            'tipos': ['In-Feed', 'TopView', 'Branded Effects'],
            'objetivos': ['Conversões', 'Engajamento', 'Alcance'],
            'peso': 0.15
        },
        'Pinterest Ads': {
            'tipos': ['Shopping', 'Carousel', 'Collection'],
            'objetivos': ['Conversões', 'Tráfego', 'Catálogo'],
            'peso': 0.15
        }
    }
    
    campanhas = []
    
    for campanha_id in tqdm(range(1, num_campanhas + 1), desc="Campanhas"):
        plataforma = random.choices(
            list(plataformas.keys()),
            weights=[p['peso'] for p in plataformas.values()]
        )[0]
        
        duracao = random.randint(15, 90)
        data_inicio_camp = data_inicio + timedelta(days=random.randint(0, 365-duracao))
        data_fim = data_inicio_camp + timedelta(days=duracao)
        
        budget_diario = random.uniform(100, 1000)
        budget_planejado = budget_diario * duracao
        
        segmentacao = {
            'idade_min': random.randint(18, 35),
            'idade_max': random.randint(35, 65),
            'generos': random.choices(['all', 'female', 'male'], weights=[0.3, 0.5, 0.2])[0],
            'localizacao': random.choices(['BR', 'BR-SP', 'BR-RJ', 'BR-MG'], weights=[0.4, 0.3, 0.2, 0.1])[0],
            'interesses': random.sample(['moda', 'lifestyle', 'shopping', 'luxury', 'sports'], k=random.randint(1, 3)),
            'dispositivos': random.choices(['all', 'mobile', 'desktop'], weights=[0.6, 0.3, 0.1])[0]
        }
        
        campanhas.append({
            'campanha_id': campanha_id,
            'nome': f'CAMP_{plataforma}_{data_inicio_camp.strftime("%Y%m")}_{campanha_id}',
            'plataforma': plataforma,
            'tipo_midia': random.choice(plataformas[plataforma]['tipos']),
            'objetivo': random.choice(plataformas[plataforma]['objetivos']),
            'data_inicio': data_inicio_camp,
            'data_fim': data_fim,
            'status': 'Encerrada' if data_fim < datetime.now() else 'Ativa',
            'budget_planejado': round(budget_planejado, 2),
            'segmentacao': json.dumps(segmentacao)
        })
    
    df = pd.DataFrame(campanhas)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de campanhas concluída em {duration} segundos")
    
    return df

def gerar_metricas_campanhas(df_campanhas):
    """Gera métricas diárias para cada campanha"""
    log_progress("Iniciando geração de métricas de campanhas...")
    start_time = time.time()
    
    metricas = []
    total_dias = sum((c['data_fim'] - c['data_inicio']).days for _, c in df_campanhas.iterrows())
    log_progress(f"Gerando métricas para {len(df_campanhas)} campanhas, total de {total_dias} dias...")
    
    for _, campanha in tqdm(df_campanhas.iterrows(), desc="Campanhas"):
        base_metrics = {
            'Google Ads': {'ctr': 0.035, 'cpc': 2.5, 'conv_rate': 0.02},
            'Meta Ads': {'ctr': 0.015, 'cpc': 1.8, 'conv_rate': 0.015},
            'TikTok Ads': {'ctr': 0.02, 'cpc': 1.5, 'conv_rate': 0.01},
            'Pinterest Ads': {'ctr': 0.025, 'cpc': 2.0, 'conv_rate': 0.018}
        }
        
        platform_metrics = base_metrics[campanha['plataforma']]
        data_atual = campanha['data_inicio']
        
        while data_atual <= campanha['data_fim']:
            budget_diario = campanha['budget_planejado'] / (campanha['data_fim'] - campanha['data_inicio']).days
            
            daily_variation = random.uniform(0.7, 1.3)
            impressions = int(budget_diario * 1000 * daily_variation)
            
            ctr = platform_metrics['ctr'] * random.uniform(0.8, 1.2)
            clicks = int(impressions * ctr)
            
            cpc = platform_metrics['cpc'] * random.uniform(0.9, 1.1)
            cost = clicks * cpc
            
            conv_rate = platform_metrics['conv_rate'] * random.uniform(0.9, 1.1)
            conversions = int(clicks * conv_rate)
            
            avg_conv_value = random.uniform(150, 300)
            conversion_value = conversions * avg_conv_value
            
            roas = conversion_value / cost if cost > 0 else 0
            
            metricas.append({
                'campanha_id': campanha['campanha_id'],
                'data_metrica': data_atual.date(),
                'impressoes': impressions,
                'cliques': clicks,
                'ctr': round(ctr, 4),
                'cpc': round(cpc, 2),
                'cpm': round((cost / impressions) * 1000 if impressions > 0 else 0, 2),
                'custo_total': round(cost, 2),
                'conversoes': conversions,
                'valor_conversoes': round(conversion_value, 2),
                'roas': round(roas, 2),
                'bounce_rate': round(random.uniform(0.3, 0.7), 2),
                'visualizacoes_pagina': int(clicks * random.uniform(1.5, 3.0))
            })
            
            data_atual += timedelta(days=1)
    
    df = pd.DataFrame(metricas)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de métricas de campanhas concluída em {duration} segundos")
    log_progress(f"- Total de registros diários: {len(df):,}")
    
    return df

def gerar_criativos(df_campanhas):
    """Gera dados dos criativos das campanhas"""
    log_progress("Iniciando geração de criativos...")
    start_time = time.time()
    
    criativos = []
    criativo_id = 1
    
    tipos_formato = {
        'Imagem': ['Square', 'Story', 'Banner', 'Landscape'],
        'Video': ['Story', 'Feed', 'In-Stream', 'Vertical'],
        'Carrossel': ['Product', 'Collection', 'Multi-Image'],
        'Texto': ['Headline', 'Description', 'Call-to-Action']
    }
    
    for _, campanha in tqdm(df_campanhas.iterrows(), desc="Criativos por campanha"):
        num_criativos = random.randint(3, 8)
        
        for _ in range(num_criativos):
            tipo = random.choice(list(tipos_formato.keys()))
            
            criativos.append({
                'criativo_id': criativo_id,
                'campanha_id': campanha['campanha_id'],
                'tipo': tipo,
                'formato': random.choice(tipos_formato[tipo]),
                'nome': f'CRIA_{campanha["plataforma"]}_{criativo_id}',
                'status': 'Ativo',
                'data_criacao': campanha['data_inicio'] - timedelta(days=random.randint(1, 7))
            })
            
            criativo_id += 1
    
    df = pd.DataFrame(criativos)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de criativos concluída em {duration} segundos")
    log_progress(f"- Total de criativos: {len(df):,}")
    
    return df

def gerar_metricas_criativos(df_criativos, df_metricas_campanhas):
    """Gera métricas diárias para cada criativo"""
    log_progress("Iniciando geração de métricas de criativos...")
    start_time = time.time()
    
    metricas = []
    
    # Agrupa métricas por campanha e data
    log_progress("Agregando métricas das campanhas...")
    metricas_camp = df_metricas_campanhas.groupby(['campanha_id', 'data_metrica']).agg({
        'impressoes': 'sum',
        'cliques': 'sum',
        'conversoes': 'sum',
        'custo_total': 'sum'
    }).reset_index()
    
    log_progress("Gerando métricas por criativo...")
    for _, criativo in tqdm(df_criativos.iterrows(), desc="Criativos"):
        metricas_campanha = metricas_camp[metricas_camp['campanha_id'] == criativo['campanha_id']]
        
        for _, metrica_dia in metricas_campanha.iterrows():
            peso_criativo = random.uniform(0.1, 0.4)
            
            impressoes = int(metrica_dia['impressoes'] * peso_criativo)
            cliques = int(metrica_dia['cliques'] * peso_criativo)
            conversoes = int(metrica_dia['conversoes'] * peso_criativo)
            custo = metrica_dia['custo_total'] * peso_criativo
            
            metricas.append({
                'criativo_id': criativo['criativo_id'],
                'data_metrica': metrica_dia['data_metrica'],
                'impressoes': impressoes,
                'cliques': cliques,
                'ctr': round(cliques / impressoes if impressoes > 0 else 0, 4),
                'custo': round(custo, 2),
                'conversoes': conversoes
            })
    
    df = pd.DataFrame(metricas)
    duration = round(time.time() - start_time, 2)
    log_progress(f"Geração de métricas de criativos concluída em {duration} segundos")
    log_progress(f"- Total de registros: {len(df):,}")
    
    return df

def salvar_dataframe(df, nome_arquivo, ordem_colunas):
    """Salva DataFrame com ordem específica de colunas"""
    df_ordenado = df[ordem_colunas[nome_arquivo.replace('.csv', '')]]
    df_ordenado.to_csv(nome_arquivo, index=False)
    print(f"Arquivo {nome_arquivo} salvo com {len(df_ordenado)} registros")

    
    df.to_csv(nome_arquivo, index=False)
    
    tamanho = os.path.getsize(nome_arquivo) / (1024 * 1024)  # Tamanho em MB
    num_registros = len(df)
    
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    log_progress(f"Arquivo {nome_arquivo} salvo:")
    log_progress(f"- Registros: {num_registros:,}")
    log_progress(f"- Tamanho: {tamanho:.2f} MB")
    log_progress(f"- Tempo: {duration} segundos")

if __name__ == "__main__":
    start_time = time.time()
    log_progress("Iniciando geração de dados...")
    
    try:
        log_progress("Gerando dados de produtos...")
        df_produtos = gerar_produtos()
        
        log_progress("Gerando dados de clientes...")
        df_clientes = gerar_clientes()
        
        log_progress("Gerando dados de campanhas...")
        df_campanhas = gerar_campanhas()
        
        log_progress("Gerando métricas de campanhas...")
        df_metricas_campanhas = gerar_metricas_campanhas(df_campanhas)
        
        log_progress("Gerando dados de criativos...")
        df_criativos = gerar_criativos(df_campanhas)
        
        log_progress("Gerando métricas de criativos...")
        df_metricas_criativos = gerar_metricas_criativos(df_criativos, df_metricas_campanhas)
        
        log_progress("Gerando dados de vendas...")
        df_vendas, df_itens_venda, df_carrinhos = gerar_vendas(df_produtos, df_clientes)
        
        log_progress("Gerando dados de navegação...")
        df_navegacao = gerar_navegacao(df_clientes, df_produtos)
        
        # Salvando arquivos
        log_progress("Iniciando salvamento dos arquivos...")
        print("Salvando arquivos...")
        salvar_dataframe(df_produtos, 'produtos.csv', ordem_colunas)
        salvar_dataframe(df_clientes, 'clientes.csv', ordem_colunas)
        salvar_dataframe(df_vendas, 'vendas.csv', ordem_colunas)
        salvar_dataframe(df_itens_venda, 'itens_venda.csv', ordem_colunas)
        salvar_dataframe(df_carrinhos, 'carrinhos_abandonados.csv', ordem_colunas)
        salvar_dataframe(df_navegacao, 'navegacao.csv', ordem_colunas)
        salvar_dataframe(df_campanhas, 'campanhas.csv', ordem_colunas)
        salvar_dataframe(df_metricas_campanhas, 'metricas_campanhas.csv', ordem_colunas)
        salvar_dataframe(df_criativos, 'criativos.csv', ordem_colunas)
        salvar_dataframe(df_metricas_criativos, 'metricas_criativos.csv', ordem_colunas)

        print("Processo finalizado!")
        
        end_time = time.time()
        total_duration = round(end_time - start_time, 2)
        log_progress(f"Processo finalizado com sucesso em {total_duration} segundos!")
        
    except Exception as e:
        log_progress(f"ERRO: {str(e)}")
        raise