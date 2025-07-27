# import streamlit as st
# import mysql.connector
# import pandas as pd
# import google.generativeai as genai
# from mysql.connector import Error
# import matplotlib.pyplot as plt
# import seaborn as sns

# # -- Chave API --
# genai.configure(api_key="")

# # Modelo Gemini
# modelo = genai.GenerativeModel("gemini-1.5-flash")

# # -- Conexão com MySQL --
# @st.cache_resource
# def conectar_mysql():
#     try:
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='12345678',
#             database='database_projeto_tcs'
#         )
#         return conn
#     except Error as e:
#         st.error(f"Erro ao conectar: {e}")
#         return None

# # -- Gerar SQL --
# def gerar_sql(pergunta):
#     prompt = f"""
# Você é um assistente SQL especializado em MySQL. Com base na pergunta do usuário, gere uma consulta SQL válida.
# Use apenas as tabelas e colunas abaixo...

# IMPORTANTE: 
# - Para nomes de estados ou municípios, sempre normalize removendo acentos (ex: 'Paraná' -> 'Parana')
# - Use esta normalização em todas as cláusulas WHERE que envolvam nomes próprios

# Tabelas e campos disponíveis:

# - regiao (id, NO_REGIAO)
# - uf (id, NO_UF, regiao_id)
# - municipio (id, NO_MUNICIPIO, uf_id)
# - tipo_localizacao (id, TP_LOCALIZACAO, descricao)
# - escola (id, NO_ENTIDADE, DS_ENDERECO, municipio_id, tp_localizacao_id)
# - saneamento_basico (
#     escola_id, IN_AGUA_POTAVEL, IN_AGUA_INEXISTENTE, IN_AGUA_POCO_ARTESIANO,
#     IN_AGUA_REDE_PUBLICA, IN_ESGOTO_INEXISTENTE, IN_ENERGIA_INEXISTENTE,
#     IN_LIXO_SERVICO_COLETA, IN_ENERGIA_REDE_PUBLICA, IN_ESGOTO_REDE_PUBLICA
# )
# - infraestrutura (
#     escola_id, IN_PATIO_COBERTO, IN_BIBLIOTECA, IN_LABORATORIO_CIENCIAS,
#     IN_LABORATORIO_INFORMATICA, IN_QUADRA_ESPORTES, IN_PARQUE_INFANTIL,
#     IN_SALA_PROFESSOR, IN_COZINHA, IN_REFEITORIO, IN_ALMOXARIFADO,
#     IN_ALIMENTACAO, QT_TRANSP_PUBLICO
# )
# - corpo_docente (
#     escola_id, QT_PROF_BIBLIOTECARIO, QT_PROF_PEDAGOGIA, QT_PROF_SAUDE,
#     QT_PROF_PSICOLOGO, QT_PROF_ADMINISTRATIVOS, QT_PROF_SERVICOS_GERAIS,
#     QT_PROF_SEGURANCA, QT_PROF_GESTAO, QT_PROF_ASSIST_SOCIAL,
#     QT_PROF_NUTRICIONISTA
# )
# - matriculas (
#     escola_id, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, QT_MAT_EJA, QT_MAT_ESP,
#     QT_MAT_BAS_FEM, QT_MAT_BAS_MASC, QT_MAT_BAS_BRANCA, QT_MAT_BAS_PRETA,
#     QT_MAT_BAS_PARDA, QT_MAT_BAS_AMARELA, QT_MAT_BAS_INDIGENA
# )
# - materiais (
#     escola_id, IN_MATERIAL_PED_CIENTIFICO, IN_MATERIAL_PED_ARTISTICAS,
#     IN_MATERIAL_PED_DESPORTIVA, IN_INTERNET, QT_EQUIP_MULTIMIDIA
# )

# Regras:
# - Use sempre JOINs com as chaves estrangeiras corretas.
# - Priorize nomes exatos de colunas e tabelas.
# - Retorne apenas a consulta SQL. Não escreva mais nada.

# Pergunta do usuário:
# \"\"\"{pergunta}\"\"\"
# """
#     resposta = modelo.generate_content(prompt)
#     return resposta.text.strip("```sql").strip("```").strip()

# # Função para gerar visualização gráfica dos dados
# def gerar_visualizacao(df):
#     if df.empty:
#         st.warning("Nenhum dado para visualizar.")
#         return
    
#     st.subheader("📊 Visualização Gráfica")

#     if len(df.columns) == 1:
#         col = df.columns[0]
#         fig, ax = plt.subplots()
#         df[col].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
#         ax.set_ylabel("")
#         ax.set_title(f"Distribuição de {col}")
#         st.pyplot(fig)

#     elif len(df.columns) == 2:
#         col1, col2 = df.columns
#         fig, ax = plt.subplots(figsize=(10, 6))

#         if pd.api.types.is_numeric_dtype(df[col2]):
#             # Barplot se a segunda coluna é numérica
#             sns.barplot(x=col1, y=col2, data=df, ax=ax)
#             ax.set_title(f"{col2} por {col1}")
#             plt.xticks(rotation=45)
#         elif pd.api.types.is_numeric_dtype(df[col1]):
#             # Inverso também possível
#             sns.barplot(x=col2, y=col1, data=df, ax=ax)
#             ax.set_title(f"{col1} por {col2}")
#             plt.xticks(rotation=45)
#         else:
#             # Ambos categóricos: contagem
#             df.groupby([col1, col2]).size().unstack().plot(kind='bar', stacked=True, ax=ax)
#             ax.set_title(f"Distribuição de {col1} por {col2}")
#             plt.xticks(rotation=45)

#         plt.tight_layout()
#         st.pyplot(fig)

#     elif len(df.columns) == 3:
#         # Tentativa de gráfico de dispersão
#         numeric_cols = df.select_dtypes(include='number').columns
#         if len(numeric_cols) >= 2:
#             fig, ax = plt.subplots(figsize=(10, 6))
#             sns.scatterplot(x=numeric_cols[0], y=numeric_cols[1], data=df, ax=ax)
#             ax.set_title(f"{numeric_cols[1]} vs {numeric_cols[0]}")
#             st.pyplot(fig)

#     elif df.shape[0] < 30 and df.shape[1] < 10 and df.select_dtypes(include='number').shape[1] >= 2:
#         # Heatmap para dados pequenos com muitas colunas numéricas
#         fig, ax = plt.subplots(figsize=(10, 6))
#         sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
#         ax.set_title("Correlação entre Variáveis Numéricas")
#         st.pyplot(fig)

#     else:
#         st.info("Não foi possível gerar um gráfico apropriado automaticamente.")

# # -- APP STREAMLIT --
# st.set_page_config("Chatbot SQL com Gemini", layout="centered")
# st.title("🤖 Chatbot Inteligente com Gemini + MySQL")

# pergunta = st.text_input("Faça uma pergunta sobre os dados educacionais:")

# if pergunta:
#     with st.spinner("Consultando IA..."):
#         sql_query = gerar_sql(pergunta)
#         st.code(sql_query, language="sql")

#     try:
#         conn = conectar_mysql()
#         if conn:
#             df = pd.read_sql(sql_query, conn)
            
#             st.success("Resultado:")
#             st.dataframe(df)

#             # Adiciona opção para gerar gráfico
#             if not df.empty and st.checkbox("📊 Gerar gráfico com os dados"):
#                 gerar_visualizacao(df)

#             conn.close()
#     except Exception as e:
#         st.error(f"Erro na consulta: {e}")


# Chatbot com Gemini e Streamlit

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Pega a chave da variável de ambiente
api_key = os.getenv("GEMINI_API_KEY")

# -- CONFIGURAR CHAVE GEMINI --
genai.configure(api_key=api_key)

# Modelo Gemini
modelo = genai.GenerativeModel("gemini-1.5-flash")

# -- APP STREAMLIT --
st.set_page_config("Chatbot Geral com Gemini", layout="centered")
st.title("🤖 Chatbot Inteligente com Gemini")

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    with st.spinner("Pensando..."):
        resposta = modelo.generate_content(pergunta)
        st.markdown("### 🤖 Resposta:")
        st.write(resposta.text)