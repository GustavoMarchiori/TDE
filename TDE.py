#Importando a biblioteca pandas para a manipulação e análise de dados.
import pandas as pd

#Atribuindo os valores da coluna 'Petróleo (bbl/dia)' para um objeto DataFrame.
dataframe = pd.read_csv('C:/Users/valte/OneDrive/Documentos/MeusProjetos/TDE/Produção_Combustivel/2020/2020_producao_terra.csv', usecols=['Petróleo (bbl/dia)'], delimiter=';', decimal=',')

#Removendo todos os valores NaN (Not a Number) do nosso objeto DataFrame, para podermos executar futuras instruções necessárias.
dataframe = dataframe.dropna()

#Formatando nosso objeto DataFrame para remover dos valores todos os pontos e logo após transformar todas as vírgulas em pontos.
dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].apply(lambda x: x.replace(".", "").replace(",", "."))

#Transformando o tipo dos nossos valores dentro do objeto DataFrame (Series) para valores de ponto flutuante. 
dataframe['Petróleo (bbl/dia)'] = dataframe['Petróleo (bbl/dia)'].astype(float)

#Imprime a soma de toda a coluna presente no DataFrame com 2 valores de casa decimal.
print(f'Soma dos valores presentes na coluna Petróleo (bbl/dia): {sum(dataframe["Petróleo (bbl/dia)"]):.2f}')
