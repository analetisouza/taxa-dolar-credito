import json
import requests
from pprint import pprint
import pandas as pd
from flatten_json import flatten


#source_caixa = requests.get("https://api.caixa.gov.br:8443/dadosabertos/taxasCartoes/1.2.0/itens")
source_bradesco = "https://proxy.api.prebanco.com.br/bradesco/dadosabertos/taxasCartoes/itens"
source_itau = requests.get("https://api.itau.com.br/dadosabertos/taxasCartoes/taxas/itens")
source_nubank = "https://dadosabertos.nubank.com.br/taxasCartoes/itens"

#data_caixa = json.loads(source_caixa.text)
#data_bradesco = json.loads(source_bradesco.text)
data_itau = json.loads(source_itau.text)
#data_nubank = json.loads(source_nubank.text)

#print(data_bradesco)

df_bradesco = pd.read_json(source_bradesco)
hist_bradesco = df_bradesco.iloc[:,[2]]
print(type(hist_bradesco))

'''
Passos a seguir:
*** DONE *** [1] Pegar a string json de cada linha da coluna historicoTaxas do dataframe
*** DONE *** [2] Ler a linha json pd.read_json(linha) e tranformar num dataframe de 4 colunas e 1 linha
*** DONE *** [3] Juntar todos os dataframes num df só (possivelmente já fazer isso linha a linha logo apos a leitura)
*** DONE *** [4] Juntar o df historico com o principal
*** DONE *** [5] Apagar as colunas emissorCnpj, historicoTaxas e taxaDivulgacaoDataHora do df principal
'''

df_historico = pd.DataFrame()

for linha in range(hist_bradesco.size):
    df_linha = pd.DataFrame(hist_bradesco.at[linha,'historicoTaxas'], index = [0])
    df_historico = pd.concat([df_historico, df_linha], ignore_index = True)

df_bradesco = pd.concat([df_bradesco, df_historico], axis = 1)
df_bradesco = df_bradesco.drop(columns = ['emissorCnpj', 'historicoTaxas', 'taxaDivulgacaoDataHora'])
print(df_bradesco)