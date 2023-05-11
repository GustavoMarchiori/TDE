#Importando a biblioteca pandas para a manipulação e análise de dados.
import pandas as pd
import locale
import glob
import os

locale.setlocale(locale.LC_NUMERIC, 'pt_BR.utf8')

#caminho_pasta = "./Produção_Combustivel"
caminho_pasta2 = "C:/Users/Gabriel/Documents/GitHub/TDE/Preços_Combustivel/Mensal_Brasil/preco_gasolina_2006_2022.csv" #botar caminho automatico

precos_gasolina = {'2006': None, '2007': None, '2008': None, '2009': None, '2010': None, '2011': None, '2012': None, '2013': None, 
                   '2014': None,'2015': None, '2016': None, '2017': None, '2018': None,'2019': None,'2020': None,'2021': None, '2022': None }


df = pd.read_csv(caminho_pasta2, header = 0, delimiter = ',')
df = df['PRECO MÉDIO REVENDA'].dropna().astype(float)

df = df.to_frame()

sum = 0
cont = 0
ano = 2006

for index, row in df.iterrows():
    sum += row['PRECO MÉDIO REVENDA'].astype(float)
    cont+=1
    if ano != 2020:
        if cont==12:
            cont = 0
            precos_gasolina[str(ano)]=round(sum/12, 3)
            ano+=1
            sum = 0
    else:
        if cont==11:
            cont = 0
            precos_gasolina[str(ano)]=round(sum/12, 3)
            ano+=1
            sum = 0
        




print(precos_gasolina)







'''
lista_producao_mar = glob.glob(os.path.join(caminho_pasta,'producao_mar', '*.csv'))
lista_producao_terra = glob.glob(os.path.join(caminho_pasta,'producao_terra', '*.csv'))

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
    x.append(int(ano))
    y.append(producao_mar_anos[ano] + producao_terra_anos[ano])

plt.plot(x, y)

plt.title('Producao de Petroleo (bbl/ano)')
plt.xlabel('Ano')
plt.ylabel('Producao (bbl)')

plt.show()'''
