## 1. PRODUTOS

- **produto_id**: Identificador único do produto.
- **nome**: Nome do produto.
- **categoria**: Categoria do produto (ex: Camisetas, Calças, etc).
- **preco_base**: Preço base do produto antes de descontos/ajustes.
- **custo**: Custo de aquisição/produção.
- **colecao**: Coleção do produto (Verão, Outono, Inverno, Primavera).
- **e_atemporal**: Flag indicando se é um produto atemporal.
- **meses_venda**: Meses em que o produto é vendido.
- **data_inclusao**: Data em que o produto foi incluído no catálogo.

## 2. CLIENTES

- **cliente_id**: Identificador único do cliente.
- **data_cadastro**: Data de cadastro do cliente.
- **idade**: Idade do cliente.
- **genero**: Gênero (F, M, O).
- **estado_civil**: Estado civil do cliente.
- **estado**: Estado de residência.
- **faixa_renda**: Faixa de renda do cliente.
- **dispositivo_principal**: Dispositivo mais usado (Mobile, Desktop, Tablet).
- **canal_aquisicao**: Canal pelo qual o cliente chegou.
- **tem_filhos**: Flag indicando se tem filhos.
- **frequencia_compras**: Classificação de frequência (Baixa, Média, Alta).

## 3. VENDAS

- **venda_id**: Identificador único da venda.
- **cliente_id**: ID do cliente que realizou a compra.
- **data_venda**: Data e hora da venda.
- **valor_total**: Valor total da venda.
- **desconto**: Valor do desconto aplicado.
- **valor_final**: Valor final após descontos.
- **metodo_pagamento**: Método de pagamento utilizado.
- **parcelas**: Número de parcelas.
- **status**: Status da venda (Aprovado, Cancelado, etc).

## 4. ITENS_VENDA

- **venda_id**: ID da venda.
- **produto_id**: ID do produto.
- **quantidade**: Quantidade comprada.
- **valor_unitario**: Valor unitário do produto.
- **valor_total**: Valor total do item.
- **margem**: Margem de lucro do item.

## 5. CARRINHOS_ABANDONADOS

- **carrinho_id**: Identificador único do carrinho.
- **cliente_id**: ID do cliente.
- **data_abandono**: Data e hora do abandono.
- **valor_total**: Valor total do carrinho.
- **num_itens**: Número de itens.
- **dispositivo**: Dispositivo usado.
- **razao_abandono**: Motivo do abandono.
- **itens**: JSON com detalhes dos itens.

## 6. NAVEGACAO

- **navegacao_id**: Identificador único da navegação.
- **cliente_id**: ID do cliente.
- **produto_id**: ID do produto visualizado.
- **data_sessao**: Data e hora da sessão.
- **tempo_visualizacao**: Tempo de visualização em segundos.
- **adicionou_carrinho**: Flag se adicionou ao carrinho.
- **dispositivo**: Dispositivo usado.
- **origem_trafego**: Origem do tráfego.
- **horario**: Hora do dia.
- **dia_semana**: Dia da semana.

## 7. CAMPANHAS

- **campanha_id**: Identificador único da campanha.
- **nome**: Nome da campanha.
- **plataforma**: Plataforma de veiculação.
- **tipo_midia**: Tipo de mídia.
- **objetivo**: Objetivo da campanha.
- **data_inicio**: Data de início.
- **data_fim**: Data de fim.
- **status**: Status da campanha.
- **budget_planejado**: Orçamento planejado.
- **segmentacao**: JSON com detalhes da segmentação.

## 8. METRICAS_CAMPANHAS

- **metrica_id**: Identificador único da métrica.
- **campanha_id**: ID da campanha.
- **data_metrica**: Data da métrica.
- **impressoes**: Número de impressões.
- **cliques**: Número de cliques.
- **ctr**: Taxa de cliques (Click Through Rate).
- **cpc**: Custo por clique.
- **cpm**: Custo por mil impressões.
- **custo_total**: Custo total.
- **conversoes**: Número de conversões.
- **valor_conversoes**: Valor das conversões.
- **roas**: Retorno sobre investimento em ads.
- **bounce_rate**: Taxa de rejeição.
- **visualizacoes_pagina**: Número de visualizações.

## 9. CRIATIVOS

- **criativo_id**: Identificador único do criativo.
- **campanha_id**: ID da campanha.
- **tipo**: Tipo do criativo.
- **formato**: Formato do criativo.
- **nome**: Nome do criativo.
- **status**: Status do criativo.
- **data_criacao**: Data de criação.

## 10. METRICAS_CRIATIVOS

- **metrica_id**: Identificador único da métrica.
- **criativo_id**: ID do criativo.
- **data_metrica**: Data da métrica.
- **impressoes**: Número de impressões.
- **cliques**: Número de cliques.
- **ctr**: Taxa de cliques.
- **custo**: Custo do criativo.
- **conversoes**: Número de conversões.
