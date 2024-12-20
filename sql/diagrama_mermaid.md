``` mermaid
erDiagram
    CLIENTES ||--o{ VENDAS : realiza
    CLIENTES ||--o{ CARRINHOS_ABANDONADOS : tem
    CLIENTES ||--o{ NAVEGACAO : gera
    PRODUTOS ||--o{ ITENS_VENDA : contem
    PRODUTOS ||--o{ NAVEGACAO : visualizado_em
    VENDAS ||--|{ ITENS_VENDA : possui
    CAMPANHAS ||--o{ VENDAS : origina
    CAMPANHAS ||--o{ CARRINHOS_ABANDONADOS : origem_de
    CAMPANHAS ||--o{ NAVEGACAO : fonte_de
    CAMPANHAS ||--|{ METRICAS_CAMPANHAS : tem
    CAMPANHAS ||--|{ CRIATIVOS : possui
    CRIATIVOS ||--|{ METRICAS_CRIATIVOS : tem

    CLIENTES {
        int cliente_id PK
        datetime data_cadastro
        int idade
        string genero
        string estado_civil
        string estado
        string faixa_renda
        string dispositivo_principal
        string canal_aquisicao
        boolean tem_filhos
        string frequencia_compras
    }

    PRODUTOS {
        int produto_id PK
        string nome
        string categoria
        decimal preco_base
        decimal custo
        string colecao
        boolean e_atemporal
        string meses_venda
        datetime data_inclusao
    }

    VENDAS {
        int venda_id PK
        int cliente_id FK
        datetime data_venda
        decimal valor_total
        decimal desconto
        decimal valor_final
        string metodo_pagamento
        int parcelas
        string status
        int campanha_id FK
    }

    ITENS_VENDA {
        int venda_id FK
        int produto_id FK
        int quantidade
        decimal valor_unitario
        decimal valor_total
        decimal margem
    }

    CARRINHOS_ABANDONADOS {
        int carrinho_id PK
        int cliente_id FK
        datetime data_abandono
        decimal valor_total
        int num_itens
        string dispositivo
        string razao_abandono
        json itens
        int campanha_id FK
    }

    NAVEGACAO {
        int navegacao_id PK
        int cliente_id FK
        int produto_id FK
        datetime data_sessao
        int tempo_visualizacao
        boolean adicionou_carrinho
        string dispositivo
        string origem_trafego
        int horario
        string dia_semana
        int campanha_id FK
    }

    CAMPANHAS {
        int campanha_id PK
        string nome
        string plataforma
        string tipo_midia
        string objetivo
        datetime data_inicio
        datetime data_fim
        string status
        decimal budget_planejado
        json segmentacao
    }

    METRICAS_CAMPANHAS {
        int metrica_id PK
        int campanha_id FK
        date data_metrica
        int impressoes
        int cliques
        decimal ctr
        decimal cpc
        decimal cpm
        decimal custo_total
        int conversoes
        decimal valor_conversoes
        decimal roas
        decimal bounce_rate
        int visualizacoes_pagina
    }

    CRIATIVOS {
        int criativo_id PK
        int campanha_id FK
        string tipo
        string formato
        string nome
        string status
        datetime data_criacao
    }

    METRICAS_CRIATIVOS {
        int metrica_id PK
        int criativo_id FK
        date data_metrica
        int impressoes
        int cliques
        decimal ctr
        decimal custo
        int conversoes
    }

```
