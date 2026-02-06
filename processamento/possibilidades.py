from pandas import read_csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # sobe 1 nível a partir de processamento/
BASE_DIR = BASE_DIR  # c:\Users\Vedovi\lotofacil\lotofacil
outdir = BASE_DIR  / 'base/'
#outdir.mkdir(parents=True, exist_ok=True)   # não recria, só garante que exista

ARQUIVO = outdir / 'combinacoes.csv'


def obter_possibilidades(arq=ARQUIVO):
	"""
	Cria uma lista com todas as combinações possíveis da lotofácil
		
	:param arq: Arquivo CSV com as combinações
	
	:return: Uma lista com todas as combinações 
	"""

	df = read_csv(arq, sep=';', encoding='utf-8')
	
	df.drop(columns=['seq'], inplace=True)
	possibilidades = df.values

	return possibilidades.tolist()
