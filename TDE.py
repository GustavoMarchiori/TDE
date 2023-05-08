#Importando a biblioteca pandas para a manipulação e análise de dados.
import pandas as pd
import locale
import glob
import os

locale.setlocale(locale.LC_NUMERIC, 'pt_BR.utf8')

caminho_pasta = "C:/Users/Gabriel/Documents/GitHub/TDE/Produção_Combustivel"

lista_producao_mar = glob.glob(caminho_pasta + '/producao_mar/*.csv')
lista_producao_terra = glob.glob(caminho_pasta + '/producao_terra/*.csv')

bases_de_dados = {'terra': {}, 'mar': {}}

for arquivo in lista_producao_terra:
    ano = os.path.splitext(os.path.basename(arquivo))[0].split('_')[0]
    dataframe = pd.read_csv(arquivo, usecols=['Estado', 'Período', 'Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',', low_memory=False)
    dataframe = dataframe.dropna()
    dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(str).apply(locale.atof)
    if ano not in bases_de_dados['terra']: bases_de_dados['terra'][ano] = []
    bases_de_dados['terra'][ano].append(dataframe)

for arquivo in lista_producao_mar:
    ano = os.path.splitext(os.path.basename(arquivo))[0].split('_')[0]
    dataframe = pd.read_csv(arquivo, usecols=['Estado', 'Período', 'Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',', low_memory=False)
    dataframe = dataframe.dropna()
    dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(str).apply(locale.atof)
    if ano not in bases_de_dados['mar']: bases_de_dados['mar'][ano] = []
    bases_de_dados['mar'][ano].append(dataframe)

producao_terra_anos = dict()
producao_terra_geral = 0

for ano, arquivos in bases_de_dados['terra'].items():
    concat = pd.concat(arquivos)
    soma = round(sum(concat['Petróleo (bbl/dia)']), 3)
    producao_terra_anos[ano] = soma
    producao_terra_geral+=soma
producao_terra_geral = round(producao_terra_geral, 3)

producao_mar_anos = dict()
producao_mar_geral = 0

for ano, arquivos in bases_de_dados['mar'].items():
    concat = pd.concat(arquivos)
    soma = round(sum(concat['Petróleo (bbl/dia)']), 3)
    producao_mar_anos[ano] = soma
    producao_mar_geral+=soma
producao_mar_geral = round(producao_mar_geral, 3)

producao_todos_os_anos = producao_terra_geral + producao_mar_geral

print(producao_terra_geral, producao_mar_geral, producao_todos_os_anos)

import matplotlib.pyplot as plt

x = []
y = []

for ano in bases_de_dados['mar'].keys():
    x.append(ano)
    y.append(producao_mar_anos[ano] + producao_terra_anos[ano])
plt.plot(x, y)

plt.title('Producao de Petroleo (bbl/ano)')
plt.xlabel('Ano')
plt.ylabel('Producao (bbl)')

plt.show()
