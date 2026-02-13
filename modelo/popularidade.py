import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


def linha_para_dezenas(row: pd.Series, col_prefix: str = "d") -> list[int]:
    """
    Converte uma linha com colunas d1, d2, ..., d15 em uma lista ordenada de dezenas.
    Ajuste o prefixo/nomes das colunas conforme o seu CSV de combinações.
    """
    cols_dezenas = [c for c in row.index if c.startswith(col_prefix)]
    dezenas = [int(row[c]) for c in cols_dezenas]
    return sorted(dezenas)


def extrair_features_dezenas(dezenas: list[int]) -> dict:
    """
    Extrai features simples de uma combinação de dezenas:
    - soma
    - quantidade de pares/ímpares
    - quantidade de sequências consecutivas
    """
    dezenas = sorted(dezenas)
    soma = sum(dezenas)
    pares = sum(1 for d in dezenas if d % 2 == 0)
    impares = len(dezenas) - pares
    sequencias = sum(
        1 for i in range(len(dezenas) - 1)
        if dezenas[i + 1] - dezenas[i] == 1
    )
    return {
        "soma": soma,
        "qtd_pares": pares,
        "qtd_impares": impares,
        "qtd_sequencias": sequencias,
    }


def score_popularidade_simulada(dezenas: list[int]) -> float:
    """
    Heurística de popularidade "teórica" de uma combinação.

    Ideia:
    - Mais sequências: jogadores gostam de padrões visíveis.
    - Soma baixa: tendência a números pequenos.
    - Combinações com todos pares/todos ímpares: menos comuns.
    - Pequeno ruído gaussiano para não ficar 100% determinístico.
    """
    f = extrair_features_dezenas(dezenas)
    score = 0.0

    # Sequências tornam a combinação mais "atraente"
    score += f["qtd_sequencias"] * 2.0

    # Soma baixa tende a ser mais escolhida
    if f["soma"] < 200:
        score += 3.0
    elif f["soma"] < 250:
        score += 1.0

    # Extremos de pares/ímpares (muito desequilibrado) penalizados
    if f["qtd_pares"] in (0, 1, 14, 15):
        score -= 2.0

    # Ruído pequeno para diferenciar combinações parecidas
    score += float(np.random.normal(0, 0.5))

    return score


def preparar_combinacoes(combinacoes_df: pd.DataFrame) -> pd.DataFrame:
    """
    A partir de um DataFrame de combinações (colunas d1..d15 ou similar),
    adiciona colunas:
    - Dezenas (lista)
    - features (soma, qtd_pares, qtd_impares, qtd_sequencias)
    - score_popularidade (simulado)
    """
    # Gera coluna Dezenas se ainda não existir
    if "Dezenas" not in combinacoes_df.columns:
        combinacoes_df = combinacoes_df.copy()
        combinacoes_df["Dezenas"] = combinacoes_df.apply(
            linha_para_dezenas, axis=1
        )

    feats = combinacoes_df["Dezenas"].apply(extrair_features_dezenas)
    feats_df = pd.DataFrame(list(feats))

    combinacoes_feats = pd.concat([combinacoes_df.reset_index(drop=True),
                                   feats_df.reset_index(drop=True)], axis=1)

    combinacoes_feats["score_popularidade"] = combinacoes_feats["Dezenas"].apply(
        score_popularidade_simulada
    )

    return combinacoes_feats


def treinar_modelo_popularidade(combinacoes_feats: pd.DataFrame):
    """
    Treina um modelo de regressão (HistGradientBoostingRegressor)
    para aprender o score de popularidade simulado.

    Retorna:
    - modelo treinado
    - R² em teste
    - colunas de features usadas (lista)
    """
    cols_features = ["soma", "qtd_pares", "qtd_impares", "qtd_sequencias"]

    X = combinacoes_feats[cols_features]
    y = combinacoes_feats["score_popularidade"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = HistGradientBoostingRegressor(random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    return modelo, r2, cols_features


def estimar_popularidade(modelo, dezenas: list[int], cols_features: list[str]) -> float:
    """
    Usa o modelo treinado para estimar a popularidade de uma combinação.
    """
    feats = extrair_features_dezenas(dezenas)
    X = pd.DataFrame([[feats[c] for c in cols_features]], columns=cols_features)
    return float(modelo.predict(X)[0])


def gerar_jogos_pouco_populares(
    modelo,
    cols_features: list[str],
    n_jogos: int = 10,
    n_amostras: int = 5000,
    seed: int | None = 42,
):
    """
    Gera n_jogos combinações candidatas com baixa popularidade estimada,
    escolhidas entre n_amostras combinações aleatórias.
    """
    rng = np.random.default_rng(seed)
    candidatos = []

    for _ in range(n_amostras):
        dezenas = sorted(rng.choice(range(1, 26), size=15, replace=False))
        score = estimar_popularidade(modelo, dezenas, cols_features)
        candidatos.append((score, dezenas))

    candidatos.sort(key=lambda x: x[0])  # menor score = menos popular
    return candidatos[:n_jogos]
