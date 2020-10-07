import json
import requests
import pandas as pd


#source_caixa = requests.get("https://api.caixa.gov.br:8443/dadosabertos/taxasCartoes/1.2.0/itens")
source_bradesco = "https://proxy.api.prebanco.com.br/bradesco/dadosabertos/taxasCartoes/itens"
source_itau = requests.get("https://api.itau.com.br/dadosabertos/taxasCartoes/taxas/itens")
source_nubank = requests.get("https://dadosabertos.nubank.com.br/taxasCartoes/itens")

#data_caixa = json.loads(source_caixa.text)
#data_bradesco = json.loads(source_bradesco.text)
data_itau = json.loads(source_itau.text)
data_nubank = json.loads(source_nubank.text)

#print(data_bradesco)
df_bradesco = pd.read_json(source_bradesco)
print(df_bradesco.dtypes)
hist_bradesco = df_bradesco.iloc[:,[2]]
print(hist_bradesco)
