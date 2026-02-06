from processamento.possibilidades import obter_possibilidades
from processamento.resultados import resultados_ordenados
from processamento.reajustar_dados import obter_indices

from pandas import read_csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # sobe 1 nível a partir de processamento/
BASE_DIR = BASE_DIR  # c:\Users\Vedovi\lotofacil\lotofacil
outdir = BASE_DIR  / 'base/'
#outdir.mkdir(parents=True, exist_ok=True)  # não recria, só garante que exista

ARQUIVO = outdir / 'resultados.csv'


def dados_indice(atualizar_base_resultados=False):
	"""
	Cria um DataFrame com algumas informações dos concursos da Lotofácil.

	:param atualizar_base_resultados: True atualiza a base, do contrário, não.
	(default: {False})

	Campos do DataFrame:

	1 - Concursos
	2 - Índice dos concurso na lista de concursos possíveis
	3 - Data do sorteio
	4 - Quantidade de vencedores (15 dezenas) no concurso
	
	return: DataFrame com os dados
	"""

	if atualizar_base_resultados:
		# Atualiza o arquivo com todos os resultados dos sorteios já realizados
		from dados import scrapping_resultados	
	
	resultado_concurso = read_csv(ARQUIVO,
								  sep=';',
								  encoding='latin1')

	num_sorteados = resultado_concurso.iloc[:, 2:17]
	num_ordenados = num_sorteados.values

	for numeros in num_ordenados:
		numeros.sort()

	resultados = num_ordenados.tolist()
	possibilidades = obter_possibilidades()
	indices = obter_indices(possibilidades, resultados)

	dados = resultado_concurso[['Concurso', 'Data Sorteio', 'Ganhou']]
	
	dia = dados['Data Sorteio'].apply(lambda data: data[0:2])
	mes = dados['Data Sorteio'].apply(lambda data: data[3:5])
	ano = dados['Data Sorteio'].apply(lambda data: data[-4:])

	dados.insert(1, 'Indice', indices)
	dados.insert(len(dados.columns), column='Dia', value=dia)
	dados.insert(len(dados.columns), column='Mes', value=mes)
	dados.insert(len(dados.columns), column='Ano', value=ano)

	return dados 
