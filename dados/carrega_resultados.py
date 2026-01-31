import pandas as pd
import ssl
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
outdir = BASE_DIR / 'lotofacil' / 'base'
outdir.mkdir(parents=True, exist_ok=True)

# endpoint “online” usado pelo site (último concurso)
URL_API = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil"

ssl._create_default_https_context = ssl._create_unverified_context

def baixar_todos_resultados():
    # 1) lê o XLS consolidado (como você já faz)
    url_xls = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados/download?modalidade=Lotof%C3%A1cil"
    base = pd.read_excel(url_xls)

    # 2) pega JSON do último concurso pelo mesmo backend do botão
    resp = requests.get(URL_API, verify=False)
    resp.raise_for_status()
    j = resp.json()

    # monta um DataFrame “1 linha” com o último concurso
    ultimo = pd.DataFrame([{
        "Concurso": j["numero"],
        "Data Sorteio": j["dataApuracao"],
        "Bola1": j["listaDezenas"][0],
        "Bola2": j["listaDezenas"][1],
        "Bola3": j["listaDezenas"][2],
        "Bola4": j["listaDezenas"][3],
        "Bola5": j["listaDezenas"][4],
        "Bola6": j["listaDezenas"][5],
        "Bola7": j["listaDezenas"][6],
        "Bola8": j["listaDezenas"][7],
        "Bola9": j["listaDezenas"][8],
        "Bola10": j["listaDezenas"][9],
        "Bola11": j["listaDezenas"][10],
        "Bola12": j["listaDezenas"][11],
        "Bola13": j["listaDezenas"][12],
        "Bola14": j["listaDezenas"][13],
        "Bola15": j["listaDezenas"][14],
        "Ganhadores_15_Números": j["listaRateioPremio"][0]["numeroDeGanhadores"]
    }])

    # 3) concatena: histórico + último (caso ainda não esteja no XLS)
    base = pd.concat([base, ultimo], ignore_index=True)

    # remove duplicados por Concurso
    base = base.drop_duplicates('Concurso')

    # renomeia colunas
    colunas = {
        'Bola1': 'B1', 'Bola2': 'B2', 'Bola3': 'B3', 'Bola4': 'B4', 'Bola5': 'B5',
        'Bola6': 'B6', 'Bola7': 'B7', 'Bola8': 'B8', 'Bola9': 'B9', 'Bola10': 'B10',
        'Bola11': 'B11', 'Bola12': 'B12', 'Bola13': 'B13', 'Bola14': 'B14', 'Bola15': 'B15',
        'Ganhadores_15_Números': 'Ganhou'
    }
    base.rename(columns=colunas, inplace=True)

    return base

if __name__ == '__main__':
    arquivo = outdir / 'resultados.csv'
    base = baixar_todos_resultados()
    base.to_csv(arquivo, sep=';', encoding='utf8', index=False)

    concurso = base['Concurso'].max()
    data = str(base[base['Concurso'] == concurso]['Data Sorteio'].iloc[0])

    print(f'\n\033[1;32mTODOS OS RESULTADOS DOS CONCURSOS DA LOTOFÁCIL FORAM BAIXADOS COM SUCESSO!\033[m')
    print(f'\n\n\033[1;36mÚltimo sorteio:\033[m {data}\n\033[1;36mConcurso:\033[m {concurso}')
    print(f'\n\n\033[1;35mArquivo salvo em:\033[m \033[1;33m{arquivo}\033[m')
