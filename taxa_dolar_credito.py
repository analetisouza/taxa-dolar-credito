import pandas as pd
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
    df_source = pd.read_json(source)
    print(df_source)
    hist_source = df_source.iloc[:,[2]]

    df_historico = pd.DataFrame()

    for linha in range(hist_source.size):
        df_linha = pd.DataFrame(hist_source.at[linha,'historicoTaxas'], index = [0])
        df_historico = pd.concat([df_historico, df_linha], ignore_index = True)

    df_source = pd.concat([df_source, df_historico], axis = 1)
    df_source = df_source.drop(columns = ['emissorCnpj', 'historicoTaxas', 'taxaDivulgacaoDataHora'])
    return df_source

'''
df_bradesco = prepara_dataframe(source_bradesco)
df_caixa = prepara_dataframe(source_caixa)
df_itau = prepara_dataframe(source_itau)
df_nubank = prepara_dataframe(source_nubank)
'''