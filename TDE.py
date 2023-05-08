#Importando a biblioteca pandas para a manipulação e análise de dados.
import pandas as pd
import glob


#Definindo o caminho para a pasta onde estão localizados seus arquivos CSV:
caminho_pasta = "C:/Users/valte/OneDrive/Documentos/MeusProjetos/TDE/Produção_Combustivel/teste"

#Criando uma lista vazia para armazenar os DataFrames que serão criados a partir de cada arquivo CSV dentro da pasta:
lista_producao = glob.glob(caminho_pasta + '/*.csv')

#loop para ler cada arquivo CSV na pasta e adicionar seu DataFrame resultante à lista de DataFrames:
petroleo = []
# os.listdir() retorna uma lista com o nome de todos os arquivos e diretórios na pasta especificada.
for nome_arquivo in lista_producao:
  #if nome_arquivo.endswith('.csv') é para garantir que apenas arquivos CSV sejam lidos
    
      #os.path.join() é usada para combinar o caminho da pasta e o nome do arquivo em uma única string.
        #pd.read_csv() é usada para ler cada arquivo CSV e criar um DataFrame. 
        dataframe = pd.read_csv(nome_arquivo, usecols=['Petróleo (bbl/dia)'], header=0, delimiter=';', decimal=',')
        print(dataframe)
        '''lista_producao.append(dataframe)


#juntando todos os DataFrames em um único DataFrame usando a função pd.concat():
producao = pd.concat(lista_producao,axis=0, join='inner', ignore_index=True)

#Formatando nosso objeto DataFrame para remover dos valores todos os pontos e logo após transformar todas as vírgulas em pontos.
producao['Petróleo (bbl/dia)'] = producao['Petróleo (bbl/dia)'].apply(lambda x: x.replace(".", "").replace(",", "."))

#Transformando o tipo dos nossos valores dentro do objeto DataFrame (Series) para valores de ponto flutuante. 
producao['Petróleo (bbl/dia)'] = producao['Petróleo (bbl/dia)'].astype(float)

#Imprime a soma de toda a coluna presente no DataFrame com 2 valores de casa decimal.
print(f'Soma dos valores presentes na coluna Petróleo (bbl/dia): {sum(producao["Petróleo (bbl/dia)"]):.2f}')'''
