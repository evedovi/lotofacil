from dados.dados import dividir_dados
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


def criar_modelo(
        base_dados,
        primeira_camada=30,
        segunda_camada=15,
        terceira_camada=15,
        saida=1,
        periodo=50,
        lote=15
    ):
    """
    Cria um modelo de rede neural (MLP) com até três camadas escondidas.
    """

    x_treino, x_teste, y_treino, y_teste, atributos = dividir_dados(base_dados)

    hidden = (primeira_camada, segunda_camada, terceira_camada)

    modelo = MLPClassifier(
        hidden_layer_sizes=hidden,
        activation="relu",
        max_iter=periodo,      # similar a epochs
        batch_size=lote,
        solver="adam",
        random_state=42
    )

    modelo.fit(x_treino, y_treino)

    y_pred = modelo.predict(x_teste)
    pontuacao = accuracy_score(y_teste, y_pred)

    return modelo, pontuacao

