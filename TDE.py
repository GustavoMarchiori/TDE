# Gerar DataFrames
import pandas as pd
import locale
import glob
import os

locale.setlocale(locale.LC_NUMERIC, 'pt_BR.utf8')

# Obter informações sobre o preço

caminho_pasta_preco = './Preços_Combustivel'

precos_gasolina = dict()

# Lendo o arquivo CSV com os dados de preço da gasolina
df = pd.read_csv(os.path.join(caminho_pasta_preco, 'Mensal_Brasil/preco_gasolina_2006_2022.csv'), header = 0, delimiter = ',')

for index, row in df.iterrows():
    # Obtendo o ano a partir do campo 'MÊS' do DataFrame
    ano = '20' + row['MÊS'].split('-')[-1]
    if ano not in precos_gasolina:
        precos_gasolina[ano] = list()
    # Armazenando os preços médios de revenda por ano
    precos_gasolina[ano].append(row['PRECO MÉDIO REVENDA'])

# Calculando a média dos preços de revenda por ano
for ano, valores in precos_gasolina.items():
    precos_gasolina[ano] = round(sum(valores) / len(valores), 3)

# Obter informações sobre a produção
caminho_pasta_producao = './Produção_Combustivel'

bases_de_dados = {'terra': {}, 'mar': {}}

# Obtendo a lista de arquivos CSV de produção em terra e mar
lista_producao_mar = glob.glob(os.path.join(caminho_pasta_producao,'producao_mar', '*.csv'))
lista_producao_terra = glob.glob(os.path.join(caminho_pasta_producao,'producao_terra', '*.csv'))

for arquivo in lista_producao_terra:
    # Obtendo o ano a partir do nome do arquivo
    ano = os.path.splitext(os.path.basename(arquivo))[0].split('_')[0]
    dataframe = pd.read_csv(arquivo, usecols=['Estado', 'Período', 'Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',', low_memory=False)
    dataframe = dataframe.dropna()
    dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(str).apply(locale.atof)
    if ano not in bases_de_dados['terra']: bases_de_dados['terra'][ano] = []
    bases_de_dados['terra'][ano].append(dataframe)

for arquivo in lista_producao_mar:
    # Obtendo o ano a partir do nome do arquivo
    ano = os.path.splitext(os.path.basename(arquivo))[0].split('_')[0]
    dataframe = pd.read_csv(arquivo, usecols=['Estado', 'Período', 'Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',', low_memory=False)
    dataframe = dataframe.dropna()
    dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(str).apply(locale.atof)
    if ano not in bases_de_dados['mar']: bases_de_dados['mar'][ano] = []
    bases_de_dados['mar'][ano].append(dataframe)

producao_terra_anos = dict()
producao_mar_anos = dict()
producao_terra_geral = 0
producao_mar_geral = 0

# Calculando a produção de petróleo em terra por ano e a produção total em terra
for ano, arquivos in bases_de_dados['terra'].items():
    concat = pd.concat(arquivos)
    soma = round(sum(concat['Petróleo (bbl/dia)']), 3)
    producao_terra_anos[ano] = soma
    producao_terra_geral+=soma
producao_terra_geral = round(producao_terra_geral, 3)

# Calculando a produção de petróleo no mar por ano e a produção total no mar
for ano, arquivos in bases_de_dados['mar'].items():
    concat = pd.concat(arquivos)
    soma = round(sum(concat['Petróleo (bbl/dia)']), 3)
    producao_mar_anos[ano] = soma
    producao_mar_geral+=soma
producao_mar_geral = round(producao_mar_geral, 3)

producao_todos_os_anos = producao_terra_geral + producao_mar_geral

#Gerar gráficos
import matplotlib.pyplot as plt
import numpy as np

x1 = list(bases_de_dados['terra'].keys())
y1 = list()
y2 = list()

# Construindo os dados para o primeiro gráfico (Produção de Petróleo)
for ano in x1:
    y1.append(producao_terra_anos[ano] + producao_mar_anos[ano])

# Construindo os dados para o segundo gráfico (Preço médio da Gasolina)
for valor in precos_gasolina.values():
    y2.append(valor)


# Criação da figura e dos eixos
fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

# Plotagem do primeiro gráfico
ax1.plot(x1, y1, color='blue', marker='o')
ax1.set_title('Producao de Petróleo (bbl/ano) (Linha)')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Producao (bbl)')
ax1.tick_params(axis='x', rotation=90)

# Plotagem do segundo gráfico
ax2.plot(x1, y2, color='orange', marker='o')
ax2.set_title('Preço médio da Gasolina por ano (R$/L) (Linha)')
ax2.set_xlabel('Ano')
ax2.set_ylabel('Preço')
ax2.tick_params(axis='x', rotation=90)

# Ajustando o espaço entre os subplots
plt.tight_layout()

# Mostrando os dois primeiros graficos
plt.show()

#Transformando o tamanho da lista em uma variavel para mostrar um ano para cada indice
x = np.arange(len(x1))

#Terceiro e quarto grafico

fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))
# Plotagem do terceiro gráfico
ax1.bar(x, y1, color='blue')
ax1.set_title('Produção de Petróleo (bbl/ano) (Barra)')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Produção (bbl)')
ax1.set_xticks(x)
ax1.set_xticklabels(x1, rotation=90)

# Plotagem do quarto gráfico
ax2.bar(x, y2, color='orange')
ax2.set_title('Preço médio da Gasolina por ano (R$/L) (Barra)')
ax2.set_xlabel('Ano')
ax2.set_ylabel('Preço')
ax2.set_xticks(x)
ax2.set_xticklabels(x1, rotation=90)

# Ajustando o espaço entre os subplots
plt.tight_layout()

# Mostrando os graficos
plt.show()

# Plotagem do quinto gráfico
fig, ax1 = plt.subplots()
ax1.bar(x, y1, color='blue')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Producao de Petróleo (bbl/ano)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Criando um eixo-y secundário para o Preço médio da gasolina
ax2 = ax1.twinx()

# Plotando o preço médio da gasolina
ax2.plot(x, y2, color='orange', marker='o')
ax2.set_ylabel('Preço médio da Gasolina por ano (R$/L)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')
ax1.set_xticks(x)
ax1.set_xticklabels(x1, rotation=90)
plt.title('Produção de Petróleo x Preço médio da gasolina por ano')

# Mostrando o quinto gráfico
plt.tight_layout()
plt.show()
