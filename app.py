import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor






# função para carregar o dataset
@st.cache
# aqui estou carregando o dataset que foi trabalhando durante as três aulas do curso
def get_data():
    return pd.read_csv("https://gist.githubusercontent.com/MagdaSousa/56765cb4d791ab878ccba9b9ca10996a/raw/ca87e08b7f0fad192dc9645d6273a79bd3a2ffb4/data.csv")


# função para treinar o modelo
def train_model():
    # aqui estou treinando o modelo com a classe RandomForestRegressor, que dos tipos de ferramentas testadas nas aulas, foi a que trouxe o valor
    # de predição mais acertivo
    data = get_data()
    x = data.drop("MEDV",axis=1)
    y = data["MEDV"]
    rf_regressor = RandomForestRegressor(n_estimators=200, max_depth=7, max_features=3)
    rf_regressor.fit(x, y)
    return rf_regressor

# criando um dataframe
#chamando a função para criar o dataframe
data = get_data()

# treinando o modelo
#chamando a função para fazer o treinamento do modelo, a partir dos dados obtidos no dataset
model = train_model()

# título
st.title("Data App - Prevendo Valores de Imóveis")

# subtítulo
st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learning para o problema de predição de valores de imóveis de Boston.")

# verificando o dataset
st.subheader("Selecionando apenas um pequeno conjunto de atributos do dataset para visualizar")

# atributos para serem exibidos por padrão
defaultcols = ["RM","PTRATIO","LSTAT","MEDV"]


# defindo atributos a partir do multiselect
cols = st.multiselect("Atributos", data.columns.tolist(), default=defaultcols)

# exibindo os top 10 registro do dataframe
st.dataframe(data[cols].head(10))


st.subheader("Distribuição de imóveis por preço")

# definindo a faixa de valores
faixa_valores = st.slider("Faixa de preço", float(data.MEDV.min()), 150., (10.0, 100.0))

# filtrando os dados
dados = data[data['MEDV'].between(left=faixa_valores[0],right=faixa_valores[1])]

# plot a distribuição dos dados
f = px.histogram(dados, x="MEDV", nbins=100, title="Distribuição de Preços")
f.update_xaxes(title="valor médio de casas ocupadas pelos proprietários em US $ 1000")
f.update_yaxes(title="Total Imóveis")
st.plotly_chart(f)




st.sidebar.subheader("Defina os atributos do imóvel para predição")

# mapeando dados do usuário para cada atributo
crim = st.sidebar.number_input("Taxa de Criminalidade", value=data.CRIM.mean())
indus = st.sidebar.number_input("Proporção de Hectares de Negócio", value=data.CRIM.mean())
chas = st.sidebar.selectbox("Faz limite com o rio?",("Sim","Não"))

# transformando o dado de entrada em valor binário
chas = 1 if chas == "Sim" else 0



nox = st.sidebar.number_input("Concentração de óxido nítrico", value=data.NOX.mean())

rm = st.sidebar.number_input("Número de Quartos", value=1)

ptratio = st.sidebar.number_input("Índice de alunos para professores",value=data.PTRATIO.mean())

lstat = st.sidebar.number_input("Porcentagem de status baixo",value=data.LSTAT.mean())

# inserindo um botão na tela
btn_predict = st.sidebar.button("Realizar Predição")

# verifica se o botão foi acionado
if btn_predict:
    result = model.predict([[crim,indus,chas,nox,rm,ptratio,lstat]])
    st.subheader("O valor previsto para o imóvel é:")
    result = "US $ "+str(round(result[0]*10,3))
    st.write(result)