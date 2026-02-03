import pandas as pd
import ssl
from pathlib import Path
import requests

BASE_DIR = Path(__name__).resolve().parent  # pasta de scrapping_resultados.py
outdir = BASE_DIR / 'lotofacil/'
outdir = outdir / 'base'
outdir.mkdir(parents=True, exist_ok=True)   # não recria, só garante que exista

ssl._create_default_https_context = ssl._create_unverified_context

URL_XLS = "https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados/download?modalidade=Lotof%C3%A1cil"
URL_API_BASE = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil"

def ler_xls_consolidado():
    base = pd.read_excel(URL_XLS)
    base = base.drop_duplicates('Concurso')
    return base

def montar_df_concurso(json_obj):
    # monta DataFrame usando MESMOS nomes que existem no XLS
    return pd.DataFrame([{
        "Concurso": json_obj["numero"],
        "Data Sorteio": json_obj["dataApuracao"],
        "Bola1": json_obj["listaDezenas"][0],
        "Bola2": json_obj["listaDezenas"][1],
        "Bola3": json_obj["listaDezenas"][2],
        "Bola4": json_obj["listaDezenas"][3],
        "Bola5": json_obj["listaDezenas"][4],
        "Bola6": json_obj["listaDezenas"][5],
        "Bola7": json_obj["listaDezenas"][6],
        "Bola8": json_obj["listaDezenas"][7],
        "Bola9": json_obj["listaDezenas"][8],
        "Bola10": json_obj["listaDezenas"][9],
        "Bola11": json_obj["listaDezenas"][10],
        "Bola12": json_obj["listaDezenas"][11],
        "Bola13": json_obj["listaDezenas"][12],
        "Bola14": json_obj["listaDezenas"][13],
        "Bola15": json_obj["listaDezenas"][14],
        "Ganhadores_15_Números": json_obj["listaRateioPremio"][0]["numeroDeGanhadores"]
    }])

def baixar_concurso(numero=None):
    if numero is None:
        url = URL_API_BASE                  # último concurso
    else:
        url = f"{URL_API_BASE}/{numero}"    # concurso específico
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def baixar_todos_resultados():
    # 1) lê XLS consolidado (estrutura “oficial”)
    base = ler_xls_consolidado()

    # guarda a lista de colunas e ordem do XLS
    colunas_base = list(base.columns)

    # 2) pega último concurso existente no XLS
    ultimo_xls = int(base['Concurso'].max())

    # 3) pega último concurso disponível na API
    json_ultimo = baixar_concurso()
    ultimo_api = int(json_ultimo["numero"])

    dfs_extra = []

    # 4) se faltar algum concurso entre XLS e API, busca um a um
    if ultimo_api > ultimo_xls:
        for concurso in range(ultimo_xls + 1, ultimo_api + 1):
            j = baixar_concurso(concurso)
            df_c = montar_df_concurso(j)
            dfs_extra.append(df_c)

    # 5) concatena preservando exatamente as colunas do XLS
    if dfs_extra:
        df_extra = pd.concat(dfs_extra, ignore_index=True)

        # garante mesmas colunas: adiciona colunas faltantes como NaN
        for c in colunas_base:
            if c not in df_extra.columns:
                df_extra[c] = pd.NA

        # mantém apenas as colunas do XLS, na mesma ordem
        df_extra = df_extra[colunas_base]

        base = pd.concat([base, df_extra], ignore_index=True)

    # 6) remove duplicados (se por acaso o XLS já tiver algum desses concursos)
    base = base.drop_duplicates('Concurso')

    # 7) renomeia colunas para o layout final do CSV
    colunas_renome = {
        'Bola1': 'B1', 'Bola2': 'B2', 'Bola3': 'B3', 'Bola4': 'B4', 'Bola5': 'B5',
        'Bola6': 'B6', 'Bola7': 'B7', 'Bola8': 'B8', 'Bola9': 'B9', 'Bola10': 'B10',
        'Bola11': 'B11', 'Bola12': 'B12', 'Bola13': 'B13', 'Bola14': 'B14', 'Bola15': 'B15',
        'Ganhadores_15_Números': 'Ganhou'
    }
    base.rename(columns=colunas_renome, inplace=True)

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