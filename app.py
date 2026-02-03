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

CARGO_DATA_SCIENTIST = 'Data Scientist'
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
    
    return df_traduzido


def processar_dados(url: str) -> pd.DataFrame:
    """
    Processa os dados: carrega, traduz colunas e valores, e remove nulos.
    
    Args:
        url: URL do arquivo CSV
        
    Returns:
        DataFrame processado e limpo
    """
    df = carregar_dados(url)
    df = traduzir_colunas(df)
    df = traduzir_valores(df)
    df = df.dropna()
    
    return df


def filtrar_dataframe(
    dataframe: pd.DataFrame,
    anos: List,
    senioridades: List,
    contratos: List,
    tamanhos_empresa: List
) -> pd.DataFrame:
    """
    Filtra o DataFrame com base nos critérios selecionados.
    
    Args:
        dataframe: DataFrame a ser filtrado
        anos: Lista de anos selecionados
        senioridades: Lista de senioridades selecionadas
        contratos: Lista de tipos de contrato selecionados
        tamanhos_empresa: Lista de tamanhos de empresa selecionados
        
    Returns:
        DataFrame filtrado
    """
    return dataframe[
        (dataframe['ano'].isin(anos)) &
        (dataframe['senioridade'].isin(senioridades)) &
        (dataframe['contrato'].isin(contratos)) &
        (dataframe['tamanho_empresa'].isin(tamanhos_empresa))
    ]


# ============================================================================
# FUNÇÕES DE CÁLCULO DE MÉTRICAS
# ============================================================================


def calcular_metricas(dataframe: pd.DataFrame) -> Dict:
    """
    Calcula as métricas principais do dashboard.
    
    Args:
        dataframe: DataFrame filtrado
        
    Returns:
        Dicionário com as métricas calculadas
    """
    if dataframe.empty:
        return {
            'salario_medio': 0,
            'salario_maximo': 0,
            'total_registros': 0,
            'cargo_mais_frequente': ""
        }
    
    return {
        'salario_medio': dataframe['salario_usd'].mean(),
        'salario_maximo': dataframe['salario_usd'].max(),
        'total_registros': dataframe.shape[0],
        'cargo_mais_frequente': dataframe['cargo'].mode()[0] if not dataframe['cargo'].mode().empty else ""
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
        labels={'salario_usd': 'Média salarial anual (USD)', 'cargo': ''}
    )
    grafico.update_layout(
        title_x=0.1,
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
        labels={'salario_usd': 'Faixa salarial (USD)', 'count': ''}
    )
    grafico.update_layout(title_x=0.1)
    
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
        labels={'salario_usd': 'Salário médio (USD)', 'residencia': 'País'}
    )
    grafico.update_layout(title_x=0.1)
    
    return grafico


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
    
    return {
        'anos': anos_selecionados,
        'senioridades': senioridades_selecionadas,
        'contratos': contratos_selecionados,
        'tamanhos_empresa': tamanhos_selecionados
    }


def exibir_metricas(metricas: Dict) -> None:
    """
    Exibe as métricas principais do dashboard.
    
    Args:
        metricas: Dicionário com as métricas calculadas
    """
    st.subheader("Métricas gerais (Salário anual em USD)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Salário médio", f"${metricas['salario_medio']:,.0f}")
    col2.metric("Salário máximo", f"${metricas['salario_maximo']:,.0f}")
    col3.metric("Total de registros", f"{metricas['total_registros']:,}")
    col4.metric("Cargo mais frequente", metricas['cargo_mais_frequente'])


def exibir_graficos(dataframe: pd.DataFrame) -> None:
    """
    Exibe todos os gráficos do dashboard.
    
    Args:
        dataframe: DataFrame filtrado
    """
    st.subheader("Gráficos")
    
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
        filtros['tamanhos_empresa']
    )
    
    # Cabeçalho principal
    st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
    st.markdown(
        "Explore os dados salariais na área de dados nos últimos anos. "
        "Utilize os filtros à esquerda para refinar sua análise."
    )
    
    # Exibição das métricas
    metricas = calcular_metricas(df_filtrado)
    exibir_metricas(metricas)
    
    st.markdown("---")
    
    # Exibição dos gráficos
    exibir_graficos(df_filtrado)
    
    # Exibição da tabela
    exibir_tabela_dados(df_filtrado)


if __name__ == "__main__":
    main()
