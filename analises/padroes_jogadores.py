import pandas as pd
import numpy as np

def frequencia_dezenas(apostas_df: pd.DataFrame) -> pd.Series:
    cont = {d: 0 for d in range(1, 26)}
    for dezenas in apostas_df["Dezenas"]:
        for d in dezenas:
            cont[d] += 1
    return pd.Series(cont).sort_index()


def dezenas_para_one_hot(df):
    matriz = np.zeros((len(df), 25), dtype=int)
    for i, dezenas in enumerate(df["Dezenas"]):
        for d in dezenas:
            matriz[i, d-1] = 1
    colunas = [f"d{d}" for d in range(1, 26)]
    one_hot = pd.DataFrame(matriz, columns=colunas, index=df.index)
    return pd.concat([df, one_hot], axis=1)

def extrair_features_dezenas(dezenas):
    dezenas = sorted(dezenas)
    soma = sum(dezenas)
    pares = sum(1 for d in dezenas if d % 2 == 0)
    impares = 15 - pares
    sequencias = sum(
        1 for i in range(len(dezenas) - 1)
        if dezenas[i+1] - dezenas[i] == 1
    )
    return {
        "soma": soma,
        "qtd_pares": pares,
        "qtd_impares": impares,
        "qtd_sequencias": sequencias,
    }


