from dados.dados import dividir_dados
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score


def criar_modelo(
        base_dados,
        max_depth=None,
        n_estimators=200,
        learning_rate=0.1,
        min_samples_leaf=20
    ):
    """
    Cria um modelo de gradient boosting otimizado para dados tabulares.
    """

    x_treino, x_teste, y_treino, y_teste, atributos = dividir_dados(base_dados)

    modelo = HistGradientBoostingClassifier(
        max_depth=max_depth,
        max_iter=n_estimators,   # nº de árvores
        learning_rate=learning_rate,
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )

    modelo.fit(x_treino, y_treino)

    y_pred = modelo.predict(x_teste)
    pontuacao = accuracy_score(y_teste, y_pred)

    return modelo, pontuacao
