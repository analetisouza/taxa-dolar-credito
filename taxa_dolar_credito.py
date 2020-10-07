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

print(data_itau.keys)

flat_itau = (flatten(d) for d in data_itau)
df_itau = pd.DataFrame(flat_itau)

'''
#print(data_bradesco)

df_bradesco = pd.read_json(source_bradesco)
print(df_bradesco)
hist_bradesco = df_bradesco.iloc[:,[2]]
print(type(hist_bradesco))
hist_bradesco = hist_bradesco.to_dict()
hist_bradesco = json.JSONDecoder(hist_bradesco)
print(hist_bradesco)

#df_itau = pd.json_normalize(data_itau, max_level = 15)
#print(df_itau)
'''

df_nubank = pd.read_json(source_nubank)
print(df_itau)