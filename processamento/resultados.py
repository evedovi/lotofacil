from dados.dados import carregar_dados

def resultados_ordenados(base_dados):
    """
    Estrutura os resultados em ordem crescente.
    :param base_dados: DataFrame da base de dados.
    :return: lista com todos os resultados da lotofácil em ordem crescente.
    """
    dados = base_dados.copy()
    num_sorteados = dados.iloc[:, 2:17]          # colunas dos números

    resultados = []
    for _, linha in num_sorteados.iterrows():
        numeros = sorted(linha.tolist())         # cria lista mutável e ordena
        resultados.append(numeros)

    return resultados
