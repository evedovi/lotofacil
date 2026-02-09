from itertools import combinations
from csv import writer
from os import path
from pathlib import Path

#BASE_DIR = Path(__name__).resolve().parent  # pasta de scrapping_resultados.py
#o#utdir = BASE_DIR / 'lotofacil/'
#outdir = outdir / 'combinacoes/'
#outdir.mkdir(parents=True, exist_ok=True)   # não recria, só garante que exista

BASE_DIR = Path(__file__).resolve().parents[1]  # sobe 1 nível a partir de processamento/
BASE_DIR = BASE_DIR  # c:\Users\Vedovi\lotofacil\lotofacil
outdir = BASE_DIR  / 'combinacoes/'

# Cabeçalho do arquivo
CABECALHO = ['seq', 'n1', 'n2', 'n3', 'n4', 'n5',
			 'n6', 'n7', 'n8', 'n9', 'n10', 'n11',
			 'n12', 'n13', 'n14', 'n15']

# Lista com as 25 dezenas da Lotofácil
DEZENAS = [i for i in range(1, 26)]

# Diretório
DIR =  outdir / 'combinacoes.csv'

# Quantidade de dezenas
TM = 15


def criar_combinacoes_csv(dr=DIR, cb=CABECALHO, dz=DEZENAS, tm=TM):
	"""
	Cria um arquivo CSV com todos as combinações possíveis da Lotofácil. 
	
	:param dr: Diretório aonde será salvo o arquivo (default: {DIR})
	:param cb: Cabeçalho do arquivo CSV (default: {CABECALHO})
	:param dz: Dezenas da Lotofácil (default: {DEZENAS})
	:param tm: Quantidade de dezenas para a combinação (default: {15})
	"""

	if not path.exists(dr):
		with open(dr, 'w', newline='') as arquivo:
			add = writer(arquivo, delimiter=';')

			add.writerow(cb)
			indice = 1

			for combinacao in combinations(dz, tm):
				linha = list(combinacao)
				linha.insert(0, indice)
				
				add.writerow(linha)

				indice += 1



def criar_combinacoes(dz=DEZENAS, tm=TM):
	"""
	Cria uma lista com todos as combinações possíveis da Lotofácil de acordo
	com a quantidade de dezenas para a combinação. 
	
	:param dz: Dezenas da Lotofácil (default: {DEZENAS})
	:param tm: Quantidade de dezenas para a combinação (default: {15})
	"""

	combinacoes = list()

	for combinacao in combinations(dz, tm):
		combinacoes.append(list(combinacao))

	return combinacoes


if __name__ == '__main__':	
	criar_combinacoes_csv()
