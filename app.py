"""
Dashboard de Análise de Salários na Área de Dados

Este módulo implementa um dashboard interativo para análise de dados salariais
na área de tecnologia utilizando Streamlit e Plotly.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List, Optional

# ============================================================================
# CONSTANTES
# ============================================================================

URL_DADOS = "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv"

COLUNAS_TRADUZIDAS = {
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'usd',
    'salary_in_usd': 'salario_usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remota',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
}

TRADUCAO_SENIORIDADE = {
    'EN': 'junior',
    'MI': 'Pleno',
    'SE': 'Senior',
    'EX': 'executivo'
}

TRADUCAO_CONTRATO = {
    'FT': 'Tempo Integral',
    'PT': 'Meio Período',
    'CT': 'Contrato',
    'FL': 'Freelancer'
}

TRADUCAO_TAMANHO_EMPRESA = {
    'S': 'Pequena',
    'M': 'Média',
    'L': 'Grande'
}

TRADUCAO_REMOTA = {
    0: 'Presencial',
    50: 'Híbrido',
    100: 'Remoto'
}

CARGO_DATA_SCIENTIST = 'Cientista de Dados'
NUMERO_BINS_HISTOGRAMA = 30
TOP_CARGOS_LIMITE = 10
HOLE_PIZZA = 0.5

# ============================================================================
# FUNÇÕES DE PROCESSAMENTO DE DADOS
# ============================================================================


@st.cache_data
def carregar_dados(url: str) -> pd.DataFrame:
    """
    Carrega os dados do CSV a partir de uma URL.
    
    Args:
        url: URL do arquivo CSV com os dados
        
    Returns:
        DataFrame com os dados carregados
        
    Raises:
        Exception: Se houver erro ao carregar os dados
    """
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.stop()


def traduzir_colunas(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Traduz os nomes das colunas do DataFrame para português.
    
    Args:
        dataframe: DataFrame original com colunas em inglês
        
    Returns:
        DataFrame com colunas traduzidas
    """
    return dataframe.rename(columns=COLUNAS_TRADUZIDAS)


def traduzir_cargos_comuns(cargo: str) -> str:
    """
    Traduz os cargos mais comuns para português.
    
    Args:
        cargo: Nome do cargo em inglês
        
    Returns:
        Nome do cargo traduzido ou original se não houver tradução
    """
    traducao_cargos = {
        'Data Scientist': 'Cientista de Dados',
        'Data Engineer': 'Engenheiro de Dados',
        'Data Analyst': 'Analista de Dados',
        'Machine Learning Engineer': 'Engenheiro de Machine Learning',
        'Research Scientist': 'Cientista de Pesquisa',
        'Data Science Manager': 'Gerente de Ciência de Dados',
        'Data Architect': 'Arquiteto de Dados',
        'Analytics Engineer': 'Engenheiro de Analytics',
        'Business Intelligence Developer': 'Desenvolvedor de Business Intelligence',
        'Data Science Consultant': 'Consultor de Ciência de Dados',
        'Head of Data': 'Diretor de Dados',
        'Principal Data Scientist': 'Cientista de Dados Principal',
        'ML Engineer': 'Engenheiro de ML',
        'Applied Scientist': 'Cientista Aplicado',
        'Research Team Lead': 'Líder de Equipe de Pesquisa',
        'Analytics Engineering Manager': 'Gerente de Engenharia de Analytics',
        'Data Science Tech Lead': 'Líder Técnico de Ciência de Dados',
        'Applied AI ML Lead': 'Líder de IA e ML Aplicados',
        'Head of Applied AI': 'Diretor de IA Aplicada',
        'Head of Machine Learning': 'Diretor de Machine Learning',
        'Machine Learning Performance Engineer': 'Engenheiro de Performance de ML',
        'Director of Product Management': 'Diretor de Gestão de Produtos',
        'Engineering Manager': 'Gerente de Engenharia',
        'AWS Data Architect': 'Arquiteto de Dados AWS'
    }
    
    return traducao_cargos.get(cargo, cargo)


def traduzir_valores(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Traduz os valores das colunas categóricas para português.
    
    Args:
        dataframe: DataFrame com colunas já traduzidas
        
    Returns:
        DataFrame com valores traduzidos
    """
    df_traduzido = dataframe.copy()
    
    df_traduzido['senioridade'] = df_traduzido['senioridade'].replace(TRADUCAO_SENIORIDADE)
    df_traduzido['contrato'] = df_traduzido['contrato'].replace(TRADUCAO_CONTRATO)
    df_traduzido['tamanho_empresa'] = df_traduzido['tamanho_empresa'].replace(TRADUCAO_TAMANHO_EMPRESA)
    df_traduzido['remota'] = df_traduzido['remota'].replace(TRADUCAO_REMOTA)
    df_traduzido['cargo'] = df_traduzido['cargo'].apply(traduzir_cargos_comuns)
    
    return df_traduzido


def processar_dados(url: str) -> pd.DataFrame:
    """
    Processa os dados: carrega, traduz colunas e valores, remove nulos e converte tipos.
    
    Args:
        url: URL do arquivo CSV
        
    Returns:
        DataFrame processado e limpo
    """
    df = carregar_dados(url)
    df = traduzir_colunas(df)
    df = traduzir_valores(df)
    df = df.dropna()
    
    # Converter ano para inteiro
    df['ano'] = df['ano'].astype('int64')
    
    return df


def filtrar_dataframe(
    dataframe: pd.DataFrame,
    anos: List,
    senioridades: List,
    contratos: List,
    tamanhos_empresa: List,
    cargos: List = None
) -> pd.DataFrame:
    """
    Filtra o DataFrame com base nos critérios selecionados.
    
    Args:
        dataframe: DataFrame a ser filtrado
        anos: Lista de anos selecionados
        senioridades: Lista de senioridades selecionadas
        contratos: Lista de tipos de contrato selecionados
        tamanhos_empresa: Lista de tamanhos de empresa selecionados
        cargos: Lista de cargos selecionados (opcional)
        
    Returns:
        DataFrame filtrado
    """
    filtrado = dataframe[
        (dataframe['ano'].isin(anos)) &
        (dataframe['senioridade'].isin(senioridades)) &
        (dataframe['contrato'].isin(contratos)) &
        (dataframe['tamanho_empresa'].isin(tamanhos_empresa))
    ]
    
    # Aplicar filtro de cargos se fornecido
    if cargos and len(cargos) > 0:
        filtrado = filtrado[filtrado['cargo'].isin(cargos)]
    
    return filtrado


# ============================================================================
# FUNÇÕES DE CÁLCULO DE MÉTRICAS
# ============================================================================


def calcular_metricas(dataframe: pd.DataFrame, dataframe_completo: pd.DataFrame) -> Dict:
    """
    Calcula as métricas principais do dashboard com análises estatísticas robustas.
    
    Args:
        dataframe: DataFrame filtrado
        dataframe_completo: DataFrame completo para comparações
        
    Returns:
        Dicionário com as métricas calculadas
    """
    if dataframe.empty:
        return {
            'salario_medio': 0,
            'salario_mediano': 0,
            'salario_minimo': 0,
            'salario_maximo': 0,
            'desvio_padrao': 0,
            'percentil_25': 0,
            'percentil_75': 0,
            'total_registros': 0,
            'cargo_mais_frequente': "",
            'variacao_ano_anterior': 0,
            'numero_cargos_unicos': 0
        }
    
    salarios = dataframe['salario_usd']
    
    # Calcular variação ano a ano se houver múltiplos anos
    variacao = 0
    if len(dataframe['ano'].unique()) > 1:
        anos_ordenados = sorted(dataframe['ano'].unique())
        if len(anos_ordenados) >= 2:
            ano_atual = anos_ordenados[-1]
            ano_anterior = anos_ordenados[-2]
            
            media_atual = dataframe[dataframe['ano'] == ano_atual]['salario_usd'].mean()
            media_anterior = dataframe[dataframe['ano'] == ano_anterior]['salario_usd'].mean()
            
            if media_anterior > 0:
                variacao = ((media_atual - media_anterior) / media_anterior) * 100
    
    return {
        'salario_medio': salarios.mean(),
        'salario_mediano': salarios.median(),
        'salario_minimo': salarios.min(),
        'salario_maximo': salarios.max(),
        'desvio_padrao': salarios.std(),
        'percentil_25': salarios.quantile(0.25),
        'percentil_75': salarios.quantile(0.75),
        'total_registros': dataframe.shape[0],
        'cargo_mais_frequente': dataframe['cargo'].mode()[0] if not dataframe['cargo'].mode().empty else "",
        'variacao_ano_anterior': variacao,
        'numero_cargos_unicos': dataframe['cargo'].nunique()
    }


# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================


def criar_grafico_top_cargos(dataframe: pd.DataFrame) -> Optional[px.bar]:
    """
    Cria gráfico de barras horizontal com os top 10 cargos por salário médio.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio
    """
    if dataframe.empty:
        return None
    
    top_cargos = (
        dataframe
        .groupby('cargo')['salario_usd']
        .mean()
        .nlargest(TOP_CARGOS_LIMITE)
        .sort_values(ascending=True)
        .reset_index()
    )
    
    grafico = px.bar(
        top_cargos,
        x='salario_usd',
        y='cargo',
        orientation='h',
        title="Top 10 cargos por salário médio",
        labels={'salario_usd': 'Média salarial anual (USD)', 'cargo': 'Cargo'}
    )
    grafico.update_layout(
        title_x=0.1,
        xaxis_title='Média salarial anual (USD)',
        yaxis_title='',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return grafico


def criar_grafico_distribuicao_salarios(dataframe: pd.DataFrame) -> Optional[px.histogram]:
    """
    Cria histograma da distribuição de salários.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio
    """
    if dataframe.empty:
        return None
    
    grafico = px.histogram(
        dataframe,
        x='salario_usd',
        nbins=NUMERO_BINS_HISTOGRAMA,
        title="Distribuição de salários anuais",
        labels={'salario_usd': 'Faixa salarial (USD)', 'count': 'Frequência'}
    )
    grafico.update_layout(
        title_x=0.1,
        xaxis_title='Faixa salarial (USD)',
        yaxis_title='Frequência'
    )
    
    return grafico


def criar_grafico_tipos_trabalho(dataframe: pd.DataFrame) -> Optional[px.pie]:
    """
    Cria gráfico de pizza com a proporção dos tipos de trabalho.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio
    """
    if dataframe.empty:
        return None
    
    remoto_contagem = dataframe['remota'].value_counts().reset_index()
    remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
    
    grafico = px.pie(
        remoto_contagem,
        names='tipo_trabalho',
        values='quantidade',
        title='Proporção dos tipos de trabalho',
        hole=HOLE_PIZZA
    )
    grafico.update_traces(textinfo='percent+label')
    grafico.update_layout(title_x=0.1)
    
    return grafico


def criar_grafico_salario_por_pais(dataframe: pd.DataFrame) -> Optional[px.choropleth]:
    """
    Cria mapa coroplético com salário médio de Data Scientists por país.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio ou não houver dados
    """
    if dataframe.empty:
        return None
    
    df_data_scientist = dataframe[dataframe['cargo'] == CARGO_DATA_SCIENTIST]
    
    if df_data_scientist.empty:
        return None
    
    media_por_pais = (
        df_data_scientist
        .groupby('residencia')['salario_usd']
        .mean()
        .reset_index()
    )
    
    grafico = px.choropleth(
        media_por_pais,
        locations='residencia',
        color='salario_usd',
        color_continuous_scale='rdylgn',
        title='Salário médio de Cientista de Dados por país',
        labels={
            'salario_usd': 'Salário médio (USD)',
            'residencia': 'País'
        }
    )
    grafico.update_layout(
        title_x=0.1,
        coloraxis_colorbar_title='Salário médio (USD)'
    )
    
    return grafico


def criar_grafico_boxplot_senioridade(dataframe: pd.DataFrame) -> Optional[px.box]:
    """
    Cria box plot comparando salários por nível de senioridade.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio
    """
    if dataframe.empty:
        return None
    
    # Ordenar senioridade de forma lógica
    ordem_senioridade = ['junior', 'Pleno', 'Senior', 'executivo']
    dataframe_ordenado = dataframe.copy()
    dataframe_ordenado['senioridade'] = pd.Categorical(
        dataframe_ordenado['senioridade'],
        categories=ordem_senioridade,
        ordered=True
    )
    dataframe_ordenado = dataframe_ordenado.sort_values('senioridade')
    
    grafico = px.box(
        dataframe_ordenado,
        x='senioridade',
        y='salario_usd',
        title='Distribuição de Salários por Senioridade',
        labels={
            'salario_usd': 'Salário anual (USD)',
            'senioridade': 'Nível de Senioridade'
        },
        color='senioridade',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    grafico.update_layout(
        title_x=0.1,
        showlegend=False,
        xaxis_title='Nível de Senioridade',
        yaxis_title='Salário anual (USD)'
    )
    
    return grafico


def criar_grafico_tendencia_temporal(dataframe: pd.DataFrame) -> Optional[px.line]:
    """
    Cria gráfico de linha mostrando a tendência de salários ao longo dos anos.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio
    """
    if dataframe.empty or len(dataframe['ano'].unique()) < 2:
        return None
    
    tendencia = (
        dataframe
        .groupby('ano')['salario_usd']
        .agg(['mean', 'median', 'count'])
        .reset_index()
    )
    tendencia.columns = ['ano', 'media', 'mediana', 'contagem']
    
    grafico = px.line(
        tendencia,
        x='ano',
        y=['media', 'mediana'],
        title='Evolução Temporal dos Salários',
        labels={
            'ano': 'Ano',
            'value': 'Salário anual (USD)',
            'variable': 'Métrica'
        },
        markers=True
    )
    grafico.update_layout(
        title_x=0.1,
        xaxis_title='Ano',
        yaxis_title='Salário anual (USD)',
        legend=dict(
            title='Tipo',
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    grafico.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )
    
    # Renomear legendas
    grafico.data[0].name = 'Média'
    grafico.data[1].name = 'Mediana'
    
    return grafico


def criar_grafico_salario_por_tipo_trabalho(dataframe: pd.DataFrame) -> Optional[px.bar]:
    """
    Cria gráfico de barras comparando salários médios por tipo de trabalho.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Gráfico Plotly ou None se o DataFrame estiver vazio
    """
    if dataframe.empty:
        return None
    
    salario_por_tipo = (
        dataframe
        .groupby('remota')['salario_usd']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    salario_por_tipo.columns = ['tipo_trabalho', 'salario_medio']
    
    grafico = px.bar(
        salario_por_tipo,
        x='tipo_trabalho',
        y='salario_medio',
        title='Salário Médio por Tipo de Trabalho',
        labels={
            'salario_medio': 'Salário médio anual (USD)',
            'tipo_trabalho': 'Tipo de Trabalho'
        },
        color='salario_medio',
        color_continuous_scale='Blues'
    )
    grafico.update_layout(
        title_x=0.1,
        xaxis_title='Tipo de Trabalho',
        yaxis_title='Salário médio anual (USD)',
        showlegend=False
    )
    
    return grafico


def gerar_insights(dataframe: pd.DataFrame, metricas: Dict) -> List[str]:
    """
    Gera insights automáticos baseados nos dados.
    
    Args:
        dataframe: DataFrame filtrado
        metricas: Dicionário com métricas calculadas
        
    Returns:
        Lista de insights em formato de texto
    """
    insights = []
    
    if dataframe.empty:
        return ["⚠️ Nenhum dado disponível para gerar insights."]
    
    # Insight sobre variação temporal
    if metricas['variacao_ano_anterior'] != 0:
        if metricas['variacao_ano_anterior'] > 0:
            insights.append(
                f"📈 **Crescimento Positivo**: Os salários aumentaram "
                f"{metricas['variacao_ano_anterior']:.1f}% em relação ao ano anterior."
            )
        else:
            insights.append(
                f"📉 **Redução**: Os salários diminuíram "
                f"{abs(metricas['variacao_ano_anterior']):.1f}% em relação ao ano anterior."
            )
    
    # Insight sobre distribuição
    coeficiente_variacao = (metricas['desvio_padrao'] / metricas['salario_medio']) * 100 if metricas['salario_medio'] > 0 else 0
    if coeficiente_variacao > 50:
        insights.append(
            f"📊 **Alta Variabilidade**: Os salários apresentam alta dispersão "
            f"(CV: {coeficiente_variacao:.1f}%), indicando grande diferença entre os valores."
        )
    
    # Insight sobre mediana vs média
    diferenca_mediana_media = abs(metricas['salario_medio'] - metricas['salario_mediano'])
    if diferenca_mediana_media > metricas['salario_medio'] * 0.1:
        if metricas['salario_medio'] > metricas['salario_mediano']:
            insights.append(
                "💰 **Distribuição Assimétrica**: A média é significativamente maior que a mediana, "
                "indicando presença de salários muito altos que elevam a média."
            )
    
    # Insight sobre tipo de trabalho
    if 'remota' in dataframe.columns:
        salario_remoto = dataframe[dataframe['remota'] == 'Remoto']['salario_usd'].mean()
        salario_presencial = dataframe[dataframe['remota'] == 'Presencial']['salario_usd'].mean()
        if salario_remoto > 0 and salario_presencial > 0:
            diferenca = ((salario_remoto - salario_presencial) / salario_presencial) * 100
            if abs(diferenca) > 5:
                if diferenca > 0:
                    insights.append(
                        f"🏠 **Trabalho Remoto**: Profissionais remotos ganham em média "
                        f"{diferenca:.1f}% mais que profissionais presenciais."
                    )
                else:
                    insights.append(
                        f"🏢 **Trabalho Presencial**: Profissionais presenciais ganham em média "
                        f"{abs(diferenca):.1f}% mais que profissionais remotos."
                    )
    
    # Insight sobre senioridade
    if 'senioridade' in dataframe.columns:
        salario_por_senioridade = dataframe.groupby('senioridade')['salario_usd'].mean().sort_values(ascending=False)
        if len(salario_por_senioridade) > 1:
            maior = salario_por_senioridade.index[0]
            menor = salario_por_senioridade.index[-1]
            diferenca = ((salario_por_senioridade[maior] - salario_por_senioridade[menor]) / 
                        salario_por_senioridade[menor]) * 100
            insights.append(
                f"🎯 **Gap de Senioridade**: Profissionais {maior} ganham em média "
                f"{diferenca:.1f}% mais que profissionais {menor}."
            )
    
    if not insights:
        insights.append("💡 Analise os gráficos abaixo para obter mais insights sobre os dados.")
    
    return insights


# ============================================================================
# FUNÇÕES DE INTERFACE
# ============================================================================


def criar_barra_lateral_filtros(dataframe: pd.DataFrame) -> Dict:
    """
    Cria a barra lateral com os filtros interativos.
    
    Args:
        dataframe: DataFrame com os dados
        
    Returns:
        Dicionário com os valores selecionados nos filtros
    """
    st.sidebar.header("🔍 Filtros")
    
    anos_disponiveis = sorted(dataframe['ano'].unique())
    anos_selecionados = st.sidebar.multiselect(
        "Ano",
        anos_disponiveis,
        default=anos_disponiveis
    )
    
    senioridades_disponiveis = sorted(dataframe['senioridade'].unique())
    senioridades_selecionadas = st.sidebar.multiselect(
        "Senioridade",
        senioridades_disponiveis,
        default=senioridades_disponiveis
    )
    
    contratos_disponiveis = sorted(dataframe['contrato'].unique())
    contratos_selecionados = st.sidebar.multiselect(
        "Tipo de Contrato",
        contratos_disponiveis,
        default=contratos_disponiveis
    )
    
    tamanhos_disponiveis = sorted(dataframe['tamanho_empresa'].unique())
    tamanhos_selecionados = st.sidebar.multiselect(
        "Tamanho da Empresa",
        tamanhos_disponiveis,
        default=tamanhos_disponiveis
    )
    
    # Filtro opcional por cargo
    cargos_disponiveis = sorted(dataframe['cargo'].unique())
    cargos_selecionados = st.sidebar.multiselect(
        "Cargo (opcional)",
        cargos_disponiveis,
        default=[]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💡 Dica:** Use os filtros para refinar sua análise")
    
    return {
        'anos': anos_selecionados,
        'senioridades': senioridades_selecionadas,
        'contratos': contratos_selecionados,
        'tamanhos_empresa': tamanhos_selecionados,
        'cargos': cargos_selecionados
    }


def exibir_metricas(metricas: Dict) -> None:
    """
    Exibe as métricas principais do dashboard com layout melhorado.
    
    Args:
        metricas: Dicionário com as métricas calculadas
    """
    st.subheader("📊 Métricas Principais")
    
    # Primeira linha - Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Salário Médio",
            f"${metricas['salario_medio']:,.0f}",
            delta=f"Mediana: ${metricas['salario_mediano']:,.0f}" if metricas['salario_mediano'] > 0 else None
        )
    
    with col2:
        variacao_texto = f"{metricas['variacao_ano_anterior']:+.1f}%"
        st.metric(
            "Salário Mediano",
            f"${metricas['salario_mediano']:,.0f}",
            delta=variacao_texto if metricas['variacao_ano_anterior'] != 0 else None
        )
    
    with col3:
        st.metric(
            "Faixa Salarial",
            f"${metricas['salario_minimo']:,.0f} - ${metricas['salario_maximo']:,.0f}",
            delta=f"P25-P75: ${metricas['percentil_25']:,.0f} - ${metricas['percentil_75']:,.0f}"
        )
    
    with col4:
        st.metric(
            "Total de Registros",
            f"{metricas['total_registros']:,}",
            delta=f"{metricas['numero_cargos_unicos']} cargos únicos"
        )
    
    # Segunda linha - Estatísticas adicionais
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Desvio Padrão", f"${metricas['desvio_padrao']:,.0f}")
    
    with col6:
        st.metric("Percentil 25", f"${metricas['percentil_25']:,.0f}")
    
    with col7:
        st.metric("Percentil 75", f"${metricas['percentil_75']:,.0f}")
    
    with col8:
        cargo_freq = metricas['cargo_mais_frequente'][:30] + "..." if len(metricas['cargo_mais_frequente']) > 30 else metricas['cargo_mais_frequente']
        st.metric("Cargo Mais Frequente", cargo_freq)


def exibir_insights(insights: List[str]) -> None:
    """
    Exibe os insights gerados automaticamente.
    
    Args:
        insights: Lista de insights em formato de texto
    """
    st.subheader("💡 Insights Automáticos")
    for insight in insights:
        st.markdown(f"- {insight}")
    st.markdown("---")


def exibir_graficos(dataframe: pd.DataFrame, aba: str = "Visão Geral") -> None:
    """
    Exibe todos os gráficos do dashboard organizados por abas.
    
    Args:
        dataframe: DataFrame filtrado
        aba: Nome da aba atual
    """
    if aba == "Visão Geral":
        # Primeira linha de gráficos
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            grafico_cargos = criar_grafico_top_cargos(dataframe)
            if grafico_cargos:
                st.plotly_chart(grafico_cargos, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de cargos.")
        
        with col_graf2:
            grafico_hist = criar_grafico_distribuicao_salarios(dataframe)
            if grafico_hist:
                st.plotly_chart(grafico_hist, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de distribuição.")
        
        # Segunda linha de gráficos
        col_graf3, col_graf4 = st.columns(2)
        
        with col_graf3:
            grafico_remoto = criar_grafico_tipos_trabalho(dataframe)
            if grafico_remoto:
                st.plotly_chart(grafico_remoto, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")
        
        with col_graf4:
            grafico_paises = criar_grafico_salario_por_pais(dataframe)
            if grafico_paises:
                st.plotly_chart(grafico_paises, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de países.")
    
    elif aba == "Análises Comparativas":
        # Gráfico de tendência temporal
        grafico_tendencia = criar_grafico_tendencia_temporal(dataframe)
        if grafico_tendencia:
            st.plotly_chart(grafico_tendencia, use_container_width=True)
        else:
            st.info("Selecione múltiplos anos nos filtros para visualizar a tendência temporal.")
        
        st.markdown("---")
        
        # Box plot por senioridade
        col1, col2 = st.columns(2)
        
        with col1:
            grafico_box = criar_grafico_boxplot_senioridade(dataframe)
            if grafico_box:
                st.plotly_chart(grafico_box, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de box plot.")
        
        with col2:
            grafico_tipo_trabalho = criar_grafico_salario_por_tipo_trabalho(dataframe)
            if grafico_tipo_trabalho:
                st.plotly_chart(grafico_tipo_trabalho, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no gráfico de tipo de trabalho.")


def exibir_tabela_dados(dataframe: pd.DataFrame) -> None:
    """
    Exibe a tabela com os dados detalhados.
    
    Args:
        dataframe: DataFrame filtrado
    """
    st.subheader("Dados Detalhados")
    st.dataframe(dataframe)


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================


def main() -> None:
    """
    Função principal que orquestra a execução do dashboard.
    """
    # Configuração da página
    st.set_page_config(
        page_title="Análise de Dados de Salários em Tecnologia",
        layout="wide",
        page_icon="📊"
    )
    
    # Processamento dos dados
    df = processar_dados(URL_DADOS)
    
    # Criação dos filtros
    filtros = criar_barra_lateral_filtros(df)
    
    # Filtragem dos dados
    df_filtrado = filtrar_dataframe(
        df,
        filtros['anos'],
        filtros['senioridades'],
        filtros['contratos'],
        filtros['tamanhos_empresa'],
        filtros['cargos']
    )
    
    # Cabeçalho principal
    st.title("📊 Dashboard de Análise de Salários na Área de Dados")
    st.markdown(
        "Explore os dados salariais na área de dados nos últimos anos. "
        "Utilize os filtros à esquerda para refinar sua análise."
    )
    
    # Verificar se há dados filtrados
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados. Por favor, ajuste os filtros.")
        return
    
    # Exibição das métricas
    metricas = calcular_metricas(df_filtrado, df)
    exibir_metricas(metricas)
    
    st.markdown("---")
    
    # Exibir insights
    insights = gerar_insights(df_filtrado, metricas)
    exibir_insights(insights)
    
    # Organizar visualizações em tabs
    tab1, tab2, tab3 = st.tabs(["📈 Visão Geral", "🔍 Análises Comparativas", "📋 Dados Detalhados"])
    
    with tab1:
        st.header("Visão Geral dos Dados")
        exibir_graficos(df_filtrado, "Visão Geral")
    
    with tab2:
        st.header("Análises Comparativas e Tendências")
        exibir_graficos(df_filtrado, "Análises Comparativas")
    
    with tab3:
        st.header("Dados Detalhados")
        exibir_tabela_dados(df_filtrado)
        
        # Estatísticas descritivas
        st.subheader("📊 Estatísticas Descritivas")
        if not df_filtrado.empty:
            st.dataframe(
                df_filtrado['salario_usd'].describe().apply(lambda x: f"${x:,.2f}" if isinstance(x, (int, float)) else x),
                use_container_width=True
            )


if __name__ == "__main__":
    main()
