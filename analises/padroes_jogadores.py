import pandas as pd

def frequencia_dezenas(apostas_df: pd.DataFrame) -> pd.Series:
    cont = {d: 0 for d in range(1, 26)}
    for dezenas in apostas_df["Dezenas"]:
        for d in dezenas:
            cont[d] += 1
    return pd.Series(cont).sort_index()