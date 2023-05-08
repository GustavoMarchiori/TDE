#Importando a biblioteca pandas para a manipulação e análise de dados.
import pandas as pd
import locale
import glob
import os

locale.setlocale(locale.LC_NUMERIC, 'pt_BR.utf8')

caminho_pasta = "C:/Users/valte/OneDrive/Documentos/MeusProjetos/TDE/Produção_Combustivel"

lista_producao_mar = glob.glob(caminho_pasta + '/producao_mar/*.csv')
lista_producao_terra = glob.glob(caminho_pasta + '/producao_terra/*.csv')

bases_de_dados = {'terra': {}, 'mar': {}}

for arquivo in lista_producao_terra:
    ano = os.path.splitext(os.path.basename(arquivo))[0].split('_')[0]
    dataframe = pd.read_csv(arquivo, usecols=['Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',', low_memory=False)
    dataframe = dataframe.dropna()
    dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(str).apply(locale.atof)
    if ano not in bases_de_dados['terra']: bases_de_dados['terra'][ano] = []
    bases_de_dados['terra'][ano].append(dataframe['Petróleo (bbl/dia)'])

for arquivo in lista_producao_mar:
    ano = os.path.splitext(os.path.basename(arquivo))[0].split('_')[0]
    dataframe = pd.read_csv(arquivo, usecols=['Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',', low_memory=False)
    dataframe = dataframe.dropna()
    dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(str).apply(locale.atof)
    if ano not in bases_de_dados['mar']: bases_de_dados['mar'][ano] = []
    bases_de_dados['mar'][ano].append(dataframe['Petróleo (bbl/dia)'])

producao_terra_anos = dict()
producao_terra_geral = 0

for ano, arquivos in bases_de_dados['terra'].items():
    soma = round(sum(pd.concat(arquivos)), 2)
    producao_terra_anos[ano] = soma
    producao_terra_geral+=soma

producao_mar_anos = dict()
producao_mar_geral = 0

for ano, arquivos in bases_de_dados['mar'].items():
    soma = round(sum(pd.concat(arquivos)), 2)
    producao_mar_anos[ano] = soma
    producao_mar_geral+=soma

producao_todos_os_anos = producao_terra_geral + producao_mar_geral
