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

source_bradesco = "https://proxy.api.prebanco.com.br/bradesco/dadosabertos/taxasCartoes/itens"
source_caixa = "https://api.caixa.gov.br:8443/dadosabertos/taxasCartoes/1.2.0/itens"
source_itau = "https://api.itau.com.br/dadosabertos/taxasCartoes/taxas/itens"
source_nubank = "https://dadosabertos.nubank.com.br/taxasCartoes/itens"
source_compra = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='06%2F08%2F2020'&@dataFinalCotacao='10%2F18%2F2020'&$top=10000&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"

inicio_analise =  pd.to_datetime("2020-10-05")
periodo_analise = 30
dias_excluidos = ["2020-10-04", "2020-10-03", "2020-09-27", "2020-09-26", "2020-09-20", "2020-09-19", 
                "2020-09-13", "2020-09-12", "2020-09-07", "2020-09-06", "2020-09-05", "2020-08-30", "2020-08-29"]

for i in range(len(dias_excluidos)):
    dias_excluidos[i] = pd.to_datetime(dias_excluidos[i])

'''
Passos a seguir:
*** DONE *** [1] Pegar a string json de cada linha da coluna historicoTaxas do dataframe
*** DONE *** [2] Ler a linha json pd.read_json(linha) e tranformar num dataframe de 4 colunas e 1 linha
*** DONE *** [3] Juntar todos os dataframes num df só (possivelmente já fazer isso linha a linha logo apos a leitura)
*** DONE *** [4] Juntar o df historico com o principal
*** DONE *** [5] Apagar as colunas emissorCnpj, historicoTaxas e taxaDivulgacaoDataHora do df principal
'''


def prepara_dataframe(source):

    df_linha = pd.DataFrame()

    if source == source_itau: 
        df_source = json.loads(requests.get(source_itau).text)
        df_source = pd.DataFrame(df_source[0])
        df_source = df_source.at[0, 'itens']
        df_emissor = pd.DataFrame(df_source['emissor'], index = [0])
        df_historico = pd.DataFrame(df_source['historicoTaxas'])

        for linha in range(df_historico.shape[0]):
            df_linha = pd.concat([df_linha, df_emissor], ignore_index = True)
            df_historico['taxaData'] = pd.to_datetime(df_historico['taxaData'])
            df_source = df_linha

        df_source = pd.concat([df_source, df_historico], axis = 1)
        df_source = df_source.drop(columns = ['emissorCnpj', 'taxaDivulgacaoDataHora'])

    elif source == source_compra:
        df_source = pd.read_json(source)
        hist_source = df_source.iloc[:,[1]]
        df_historico = pd.DataFrame()

        for linha in range(hist_source.shape[0]):
            df_linha = pd.DataFrame(hist_source.at[linha,'value'], index = [0])
            df_linha['dataHoraCotacao'] = pd.to_datetime(df_linha['dataHoraCotacao']).dt.date
            df_historico = pd.concat([df_historico, df_linha], ignore_index = True)
            df_source = df_historico

    else:
        df_source = pd.read_json(source)
        hist_source = df_source.iloc[:,[2]]
        df_historico = pd.DataFrame()

        for linha in range(hist_source.shape[0]):
            df_linha = pd.DataFrame(hist_source.at[linha,'historicoTaxas'], index = [0])
            df_linha['taxaData'] = pd.to_datetime(df_linha['taxaData'])
            df_historico = pd.concat([df_historico, df_linha], ignore_index = True)

        df_source = pd.concat([df_source, df_historico], axis = 1)
        df_source = df_source.drop(columns = ['emissorCnpj', 'historicoTaxas', 'taxaDivulgacaoDataHora'])
    return df_source


df_bradesco = prepara_dataframe(source_bradesco)
df_caixa = prepara_dataframe(source_caixa)
df_itau = prepara_dataframe(source_itau)
df_nubank = prepara_dataframe(source_nubank)
df_compra = prepara_dataframe(source_compra)

'''
Próximos passos:
*** DONE *** [1] Inverter a ordem do Bradesco
*** DONE *** [2] Remover os valores de débito do Bradesco
*** DONE *** [3] Alterar 'CREDITO' para 'Crédito" no df da Caixa
*** DONE *** [4] Alterar 'CAIXA ECONOMICA FEDERAL'
[5] Excluir os dias não úteis dos dfs do Itaú e Nubank
[6] Verificar se os dfs começam na mesma data
[7] Diminuir o dataset para os últimos 90, 60 ou 30 dias
'''
def altera_data_inicio(df, inicio):

    for linha in range(df.shape[0]):

        #if (df.loc[linha] == df.columns).all():
           # continue
        print(linha)
        print(inicio)
        linha_atual = df.at[linha, 'taxaData']
        print(type(linha))
        if linha_atual == inicio:
            return df
        else:
            df = df.drop(df.index[linha])

    return df

df_bradesco = df_bradesco.drop(df_bradesco.loc[df_bradesco['taxaTipoGasto'] == 'Débito à conta'].index)
df_bradesco = df_bradesco.iloc[::-1].reset_index(drop = True)
df_compra = df_compra.iloc[::-1].reset_index(drop = True)


df_caixa = df_caixa.replace({'CAIXA ECONOMICA FEDERAL' : 'Caixa Economica Federal', 'CREDITO' : 'Crédito'})

print(df_bradesco)
print(df_caixa)
print(df_itau)
print(df_nubank)
print(df_compra)


df_bradesco = altera_data_inicio(df_bradesco, inicio_analise)
print(df_bradesco)
df_caixa = altera_data_inicio(df_caixa, inicio_analise)
df_itau = altera_data_inicio(df_itau, inicio_analise)
df_nubank = altera_data_inicio(df_nubank, inicio_analise)
df_compra = altera_data_inicio(df_compra, inicio_analise)

print(df_bradesco)
print(df_caixa)
print(df_itau)
print(df_nubank)
print(df_compra)