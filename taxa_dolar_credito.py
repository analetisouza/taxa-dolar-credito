import json
import requests
import pandas

source_bradesco = requests.get("https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$filter=CnpjInstituicao%20eq%20'60746948000112'&$format=json&$select=Api,CnpjInstituicao,NomeInstituicao,Recurso,URLDados")
source_caixa = requests.get("https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$filter=CnpjInstituicao%20eq%20'00360305000104'&$format=json&$select=Api,CnpjInstituicao,NomeInstituicao,Recurso,URLDados")
source_itau = requests.get("https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$filter=CnpjInstituicao%20eq%20'60701190000104'&$format=json&$select=Api,CnpjInstituicao,NomeInstituicao,Recurso,URLDados")
source_nubank = requests.get("https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$filter=CnpjInstituicao%20eq%20'18236120000158'&$format=json&$select=Api,CnpjInstituicao,NomeInstituicao,Recurso,URLDados")

api_bradesco = json.loads(source_bradesco.text)
api_caixa = json.loads(source_caixa.text)
api_itau = json.loads(source_itau.text)
api_nubank = json.loads(source_nubank.text)

print(api_caixa)

response_bradesco = requests.get(api_bradesco["URLDados"])

data_bradesco = json.loads(response_bradesco.text)
type(data_bradesco)
print(data_bradesco)