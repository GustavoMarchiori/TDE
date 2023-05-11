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

print(precos_gasolina)

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

print(producao_terra_geral, producao_mar_geral, producao_todos_os_anos)

#Gerar gráficos
import matplotlib.pyplot as plt
import numpy as np

x1 = list()
y1 = list()
y2 = list()

# Construindo os dados para o primeiro gráfico (Produção de Petróleo)
for ano in bases_de_dados['mar'].keys():
    x1.append(int(ano))
    y1.append(producao_mar_anos[ano] + producao_terra_anos[ano])

# Construindo os dados para o segundo gráfico (Preço médio da Gasolina)
for valor in precos_gasolina.values():
    y2.append(valor)

# Criação da figura e dos eixos
fig, (ax1, ax2) = plt.subplots(2)

# Plotagem do primeiro gráfico
ax1.plot(x1, y1, label='Gráfico 1')
ax1.set_title('Producao de Petroleo (bbl/ano)')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Producao (bbl)')
ax1.legend()

# Plotagem do segundo gráfico
ax2.plot(x1, y2, label='Gráfico 2')
ax2.set_title('Preço médio da Gasolina por ano (R$/l)')
ax2.set_xlabel('Ano')
ax2.set_ylabel('Preço')
ax2.legend()

# Exibição dos gráficos
plt.tight_layout()  # Ajusta o espaçamento entre os subplots
plt.show()

#Fazer terceiro gráfico