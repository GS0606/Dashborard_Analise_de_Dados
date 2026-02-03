# 📊 Dashboard de Análise de Salários na Área de Dados

Dashboard interativo desenvolvido em Streamlit para análise exploratória de dados salariais na área de tecnologia e ciência de dados. O projeto permite visualizar e analisar informações sobre salários, cargos, níveis de experiência e outros fatores relevantes do mercado de trabalho em tecnologia.

## 🚀 Características

- **Interface Interativa**: Filtros dinâmicos para refinar análises
- **Visualizações Interativas**: Gráficos interativos usando Plotly
- **Métricas em Tempo Real**: KPIs atualizados conforme os filtros aplicados
- **Interface Completamente em Português**: Todos os textos, legendas, eixos e cargos traduzidos
- **Tradução Inteligente de Cargos**: Os cargos mais comuns são automaticamente traduzidos
- **Responsivo**: Layout adaptável para diferentes tamanhos de tela

## 📋 Funcionalidades

### Métricas Principais
- Salário médio anual em USD
- Salário máximo registrado
- Total de registros na base
- Cargo mais frequente

### Visualizações
1. **Top 10 Cargos por Salário Médio**: Gráfico de barras horizontal com cargos traduzidos
2. **Distribuição de Salários**: Histograma da distribuição salarial com eixos em português
3. **Proporção de Tipos de Trabalho**: Gráfico de pizza (Presencial, Híbrido, Remoto)
4. **Salário por País**: Mapa coroplético para Cientistas de Dados com legendas em português

### Filtros Disponíveis
- **Ano**: Filtro por ano de trabalho
- **Senioridade**: Junior, Pleno, Senior, Executivo
- **Tipo de Contrato**: Tempo Integral, Meio Período, Contrato, Freelancer
- **Tamanho da Empresa**: Pequena, Média, Grande

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web interativas
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Criação de gráficos interativos
- **NumPy**: Operações numéricas

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone o repositório** (ou baixe os arquivos):
   ```bash
   git clone <url-do-repositorio>
   cd Dashboard_Analise_de_Dados
   ```

2. **Crie um ambiente virtual** (recomendado):
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**:
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Como Executar

Após instalar as dependências, execute o seguinte comando:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão, geralmente em `http://localhost:8501`.

## 📁 Estrutura do Projeto

```
Dashboard_Analise_de_Dados/
│
├── app.py                 # Aplicação principal do dashboard
├── main.py                # Script de análise exploratória
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

## 🔧 Arquitetura do Código

O código foi desenvolvido seguindo princípios de **Clean Code**:

- **Separação de Responsabilidades**: Funções modulares e com responsabilidades únicas
- **Documentação**: Docstrings em todas as funções
- **Constantes**: Valores mágicos extraídos para constantes nomeadas
- **Type Hints**: Tipagem para melhor legibilidade e manutenção
- **Cache de Dados**: Uso de `@st.cache_data` para otimização de performance

### Estrutura Modular

- **Constantes**: Configurações e mapeamentos de tradução (colunas, valores, cargos)
- **Processamento de Dados**: Carregamento, tradução de colunas/valores/cargos e limpeza
- **Cálculo de Métricas**: Funções para cálculo de KPIs
- **Visualizações**: Funções para criação de gráficos com legendas em português
- **Interface**: Funções para construção da UI
- **Função Principal**: Orquestração do dashboard

### Funções de Tradução

O código inclui funções especializadas para tradução:
- `traduzir_colunas()`: Traduz nomes das colunas
- `traduzir_valores()`: Traduz valores categóricos (senioridade, contrato, etc.)
- `traduzir_cargos_comuns()`: Traduz os cargos mais frequentes no dataset

## 📊 Fonte de Dados

Os dados são carregados diretamente do repositório GitHub:
```
https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv
```

## 🎨 Personalização

### Traduções Implementadas

O dashboard possui tradução completa para português brasileiro:

#### Tradução de Colunas
- Todas as colunas do dataset são traduzidas automaticamente
- Exemplo: `work_year` → `ano`, `job_title` → `cargo`

#### Tradução de Valores Categóricos
- **Senioridade**: EN → junior, MI → Pleno, SE → Senior, EX → executivo
- **Tipo de Contrato**: FT → Tempo Integral, PT → Meio Período, CT → Contrato, FL → Freelancer
- **Tamanho da Empresa**: S → Pequena, M → Média, L → Grande
- **Modalidade de Trabalho**: 0 → Presencial, 50 → Híbrido, 100 → Remoto

#### Tradução de Cargos
Os cargos mais comuns são automaticamente traduzidos, incluindo:
- Data Scientist → Cientista de Dados
- Data Engineer → Engenheiro de Dados
- Data Analyst → Analista de Dados
- Machine Learning Engineer → Engenheiro de Machine Learning
- Research Team Lead → Líder de Equipe de Pesquisa
- Analytics Engineering Manager → Gerente de Engenharia de Analytics
- E muitos outros...

#### Tradução de Legendas dos Gráficos
- Todos os eixos dos gráficos estão em português
- Títulos e labels traduzidos
- Exemplo: "count" → "Frequência", "salary_in_usd" → "Salário (USD)"

### Modificar Traduções

As traduções podem ser ajustadas nas constantes no início do arquivo `app.py`:

```python
# Tradução de senioridade
TRADUCAO_SENIORIDADE = {
    'EN': 'junior',
    'MI': 'Pleno',
    'SE': 'Senior',
    'EX': 'executivo'
}

# Tradução de cargos (função traduzir_cargos_comuns)
traducao_cargos = {
    'Data Scientist': 'Cientista de Dados',
    'Data Engineer': 'Engenheiro de Dados',
    # Adicione mais traduções aqui
}
```

### Adicionar Novos Gráficos

Para adicionar novos gráficos, crie uma função seguindo o padrão:

```python
def criar_grafico_novo(dataframe: pd.DataFrame) -> Optional[px.Chart]:
    # Sua lógica aqui
    pass
```

E adicione a chamada na função `exibir_graficos()`.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## 👤 Autor

Desenvolvido como projeto de análise de dados e visualização.

## 🙏 Agradecimentos

- Dados fornecidos pelo repositório [data-jobs](https://github.com/guilhermeonrails/data-jobs)
- Comunidade Streamlit pelo excelente framework
- Comunidade Plotly pelas ferramentas de visualização

---

---

## 🌐 Internacionalização

O dashboard foi desenvolvido com foco na experiência do usuário brasileiro, oferecendo:

- ✅ **100% em Português**: Interface, filtros, métricas e gráficos
- ✅ **Cargos Traduzidos**: Os principais cargos do mercado são exibidos em português
- ✅ **Legendas Claras**: Todos os eixos e labels dos gráficos estão traduzidos
- ✅ **Fácil Extensão**: Sistema modular permite adicionar novas traduções facilmente

**Nota**: Este dashboard é uma ferramenta de análise exploratória. Os dados são atualizados conforme a fonte original. Cargos que não possuem tradução específica são mantidos em inglês para preservar a precisão dos dados.
