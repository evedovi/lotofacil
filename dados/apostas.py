import pandas as pd

def simular_apostas_exemplo():
    return pd.DataFrame([
        {"Concurso": 3200, "Aposta_ID": 1, "Jogador_ID": 101,
         "Dezenas": [1, 3, 5, 7, 9, 10, 11, 13, 15, 17, 18, 20, 22, 24, 25]},
        {"Concurso": 3200, "Aposta_ID": 2, "Jogador_ID": 102,
         "Dezenas": [2, 4, 6, 8, 10, 11, 12, 14, 16, 18, 19, 21, 23, 24, 25]},
    ])