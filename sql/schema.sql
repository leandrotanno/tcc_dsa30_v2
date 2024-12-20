-- Criação das tabelas principais
CREATE TABLE clientes (
    cliente_id INTEGER PRIMARY KEY,
    data_cadastro TIMESTAMP NOT NULL,
    idade INTEGER NOT NULL,
    genero VARCHAR(1) NOT NULL,
    estado_civil VARCHAR(20) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    faixa_renda VARCHAR(20) NOT NULL,
    dispositivo_principal VARCHAR(20) NOT NULL,
    canal_aquisicao VARCHAR(50) NOT NULL,
    tem_filhos BOOLEAN NOT NULL,
    frequencia_compras VARCHAR(10) NOT NULL,
    CONSTRAINT check_idade CHECK (idade >= 18)
);

CREATE TABLE produtos (
    produto_id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco_base DECIMAL(10,2) NOT NULL,
    custo DECIMAL(10,2) NOT NULL,
    colecao VARCHAR(20) NOT NULL,
    e_atemporal BOOLEAN NOT NULL,
    meses_venda TEXT NOT NULL,
    data_inclusao TIMESTAMP NOT NULL,
    CONSTRAINT check_preco_base CHECK (preco_base > 0),
    CONSTRAINT check_custo CHECK (custo > 0)
);

CREATE TABLE vendas (
    venda_id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    data_venda TIMESTAMP NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    desconto DECIMAL(10,2) NOT NULL DEFAULT 0,
    valor_final DECIMAL(10,2) NOT NULL,
    metodo_pagamento VARCHAR(50) NOT NULL,
    parcelas INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    estacao VARCHAR(20) NOT NULL,
    campanha_origem_id INTEGER,
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    CONSTRAINT check_valor CHECK (valor_total >= 0),
    CONSTRAINT check_desconto CHECK (desconto >= 0),
    CONSTRAINT check_valor_final CHECK (valor_final >= 0),
    CONSTRAINT check_parcelas CHECK (parcelas > 0)
);

CREATE TABLE itens_venda (
    venda_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    margem DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (venda_id, produto_id),
    CONSTRAINT fk_venda FOREIGN KEY (venda_id) REFERENCES vendas(venda_id),
    CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES produtos(produto_id),
    CONSTRAINT check_quantidade CHECK (quantidade > 0),
    CONSTRAINT check_valor_unitario CHECK (valor_unitario >= 0),
    CONSTRAINT check_valor_total CHECK (valor_total >= 0)
);

CREATE TABLE carrinhos_abandonados (
    carrinho_id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    data_abandono TIMESTAMP NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    num_itens INTEGER NOT NULL,
    dispositivo VARCHAR(20) NOT NULL,
    razao_abandono VARCHAR(50) NOT NULL,
    itens JSONB NOT NULL,
    campanha_origem_id INTEGER,
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    CONSTRAINT check_num_itens CHECK (num_itens > 0),
    CONSTRAINT check_valor CHECK (valor_total >= 0)
);

CREATE TABLE navegacao (
    navegacao_id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    data_sessao TIMESTAMP NOT NULL,
    tempo_visualizacao INTEGER NOT NULL,
    adicionou_carrinho BOOLEAN NOT NULL,
    dispositivo VARCHAR(20) NOT NULL,
    origem_trafego VARCHAR(50) NOT NULL,
    horario INTEGER NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    campanha_origem_id INTEGER,
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES produtos(produto_id),
    CONSTRAINT check_tempo CHECK (tempo_visualizacao >= 0),
    CONSTRAINT check_horario CHECK (horario >= 0 AND horario < 24)
);

-- Tabelas de Mídia
CREATE TABLE campanhas (
    campanha_id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    plataforma VARCHAR(50) NOT NULL,
    tipo_midia VARCHAR(50) NOT NULL,
    objetivo VARCHAR(50) NOT NULL,
    data_inicio TIMESTAMP NOT NULL,
    data_fim TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    budget_planejado DECIMAL(10,2) NOT NULL,
    segmentacao JSONB NOT NULL
);

CREATE TABLE metricas_campanhas (
    metrica_id SERIAL PRIMARY KEY,
    campanha_id INTEGER NOT NULL,
    data_metrica DATE NOT NULL,
    impressoes INTEGER NOT NULL,
    cliques INTEGER NOT NULL,
    ctr DECIMAL(5,4) NOT NULL,
    cpc DECIMAL(10,2) NOT NULL,
    cpm DECIMAL(10,2) NOT NULL,
    custo_total DECIMAL(10,2) NOT NULL,
    conversoes INTEGER NOT NULL,
    valor_conversoes DECIMAL(10,2) NOT NULL,
    roas DECIMAL(10,2) NOT NULL,
    bounce_rate DECIMAL(5,2),
    visualizacoes_pagina INTEGER,
    CONSTRAINT fk_campanha FOREIGN KEY (campanha_id) REFERENCES campanhas(campanha_id),
    CONSTRAINT check_metricas CHECK (impressoes >= 0 AND cliques >= 0 AND ctr >= 0)
);

CREATE TABLE criativos (
    criativo_id INTEGER PRIMARY KEY,
    campanha_id INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    formato VARCHAR(50) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    data_criacao TIMESTAMP NOT NULL,
    CONSTRAINT fk_campanha FOREIGN KEY (campanha_id) REFERENCES campanhas(campanha_id)
);

CREATE TABLE metricas_criativos (
    metrica_id SERIAL PRIMARY KEY,
    criativo_id INTEGER NOT NULL,
    data_metrica DATE NOT NULL,
    impressoes INTEGER NOT NULL,
    cliques INTEGER NOT NULL,
    ctr DECIMAL(5,4) NOT NULL,
    custo DECIMAL(10,2) NOT NULL,
    conversoes INTEGER NOT NULL,
    CONSTRAINT fk_criativo FOREIGN KEY (criativo_id) REFERENCES criativos(criativo_id)
);

-- Índices
CREATE INDEX idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX idx_vendas_data ON vendas(data_venda);
CREATE INDEX idx_itens_venda_produto ON itens_venda(produto_id);
CREATE INDEX idx_navegacao_cliente ON navegacao(cliente_id);
CREATE INDEX idx_navegacao_produto ON navegacao(produto_id);
CREATE INDEX idx_navegacao_data ON navegacao(data_sessao);
CREATE INDEX idx_carrinhos_cliente ON carrinhos_abandonados(cliente_id);
CREATE INDEX idx_carrinhos_data ON carrinhos_abandonados(data_abandono);
CREATE INDEX idx_produtos_categoria ON produtos(categoria);
CREATE INDEX idx_produtos_colecao ON produtos(colecao);
CREATE INDEX idx_clientes_estado ON clientes(estado);
CREATE INDEX idx_clientes_estado_civil ON clientes(estado_civil);

-- Índices de mídia
CREATE INDEX idx_campanhas_data ON campanhas(data_inicio, data_fim);
CREATE INDEX idx_campanhas_plataforma ON campanhas(plataforma);
CREATE INDEX idx_metricas_campanhas_data ON metricas_campanhas(data_metrica);
CREATE INDEX idx_metricas_campanhas_campanha ON metricas_campanhas(campanha_id);
CREATE INDEX idx_criativos_campanha ON criativos(campanha_id);
CREATE INDEX idx_metricas_criativos_data ON metricas_criativos(data_metrica);