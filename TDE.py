import pandas as pd
import glob

path = 'C:/Users/valte/OneDrive/Documentos/dreaming/Python/arquivos'
doze_arquivos = glob.glob(path+'/*.csv')

li = []
for filename in doze_arquivos:
    df = pd.read_csv(filename, usecols=['Petróleo (bbl/dia)'], delimiter=';', index_col=None, header=0, decimal=',')
    li.append(df)
concatenated_df = pd.concat(li, axis=0, ignore_index=True)

concatenated_df['Petróleo (bbl/dia)'] = concatenated_df['Petróleo (bbl/dia)'].apply(lambda x: x.replace(".", "").replace(",", "."))
concatenated_df['Petróleo (bbl/dia)'] = concatenated_df['Petróleo (bbl/dia)'].astype(float)

print(sum(concatenated_df['Petróleo (bbl/dia)']))
