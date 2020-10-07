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
print(df_bradesco)
hist_bradesco = df_bradesco.iloc[:,[2]]
print(type(hist_bradesco))

'''
Passos a seguir:
[1] Pegar a string json de cada linha da coluna historicoTaxas do dataframe
[2] Ler a linha json pd.read_json(linha) e tranformar num dataframe de 4 colunas e 1 linha
[3] Juntar todos os dataframes num df só (possivelmente já fazer isso linha a linha logo apos a leitura)
[4] Juntar o df historico com o principal
[5] Apagar a coluna historicoTaxas do df principal
'''