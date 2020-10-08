import pandas as pd
import requests
import json
import ssl 

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

source_caixa = "https://api.caixa.gov.br:8443/dadosabertos/taxasCartoes/1.2.0/itens"
source_bradesco = "https://proxy.api.prebanco.com.br/bradesco/dadosabertos/taxasCartoes/itens"
source_itau = "https://api.itau.com.br/dadosabertos/taxasCartoes/taxas/itens"
source_nubank = "https://dadosabertos.nubank.com.br/taxasCartoes/itens"

'''
Passos a seguir:
*** DONE *** [1] Pegar a string json de cada linha da coluna historicoTaxas do dataframe
*** DONE *** [2] Ler a linha json pd.read_json(linha) e tranformar num dataframe de 4 colunas e 1 linha
*** DONE *** [3] Juntar todos os dataframes num df só (possivelmente já fazer isso linha a linha logo apos a leitura)
*** DONE *** [4] Juntar o df historico com o principal
*** DONE *** [5] Apagar as colunas emissorCnpj, historicoTaxas e taxaDivulgacaoDataHora do df principal
'''


def prepara_dataframe(source):

    if source == source_itau: 
        df_source = json.loads(requests.get(source_itau).text)
        df_source = pd.DataFrame(df_source[0])
        df_source = df_source.at[0, 'itens']
        df_emissor = pd.DataFrame(df_source['emissor'], index = [0])
        df_historico = pd.DataFrame(df_source['historicoTaxas'])

        df_linha = pd.DataFrame()

        for linha in range(df_historico.shape[0]):
            df_linha = pd.concat([df_linha, df_emissor], ignore_index = True)
            df_source = df_linha

        df_source = pd.concat([df_source, df_historico], axis = 1)
        df_source = df_source.drop(columns = ['emissorCnpj', 'taxaDivulgacaoDataHora'])

    else:
        df_source = pd.read_json(source)
        hist_source = df_source.iloc[:,[2]]

        df_historico = pd.DataFrame()

        for linha in range(hist_source.shape[0]):
            df_linha = pd.DataFrame(hist_source.at[linha,'historicoTaxas'], index = [0])
            df_historico = pd.concat([df_historico, df_linha], ignore_index = True)

        df_source = pd.concat([df_source, df_historico], axis = 1)
        df_source = df_source.drop(columns = ['emissorCnpj', 'historicoTaxas', 'taxaDivulgacaoDataHora'])
    return df_source


df_bradesco = prepara_dataframe(source_bradesco)
df_caixa = prepara_dataframe(source_caixa)
df_itau = prepara_dataframe(source_itau)
df_nubank = prepara_dataframe(source_nubank)

'''
Próximos passos:
*** DONE *** [1] Inverter a ordem do Bradesco
*** DONE *** [2] Remover os valores de débito do Bradesco
[3] Alterar 'CREDITO' para 'Crédito" no df da Caixa
[4] Alterar 'CAIXA ECONOMICA FEDERAL'
[5] Verificar se os dfs começam na mesma data
[6] Diminuir o dataset para os últimos 90, 60 ou 30 dias
'''

df_bradesco = df_bradesco.drop(df_bradesco.loc[df_bradesco['taxaTipoGasto'] == 'Débito à conta'].index)
df_bradesco = df_bradesco.iloc[::-1].reset_index(drop=True)

df_caixa = df_caixa.replace({'CAIXA ECONOMICA FEDERAL' : 'Caixa Economica Federal', 'CREDITO' : 'Crédito'})

print(df_bradesco)
print(df_caixa)
print(df_itau)
print(df_nubank)