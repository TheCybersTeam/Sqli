class banco():
	nome = None
	tabela = None

	def getBanco():
		global nome
		nome = "loja"


class tabela():
	nome = None
	colunas = None
	linhas = []

	def getTabela():
		global nome
		nome = "usuarios"

	def getColunas():
		global colunas
		colunas = ["id","usuario","senha"]

	def getDados(colunas):
		global linha
		linhas = [0:"id":"1","usuario":"joao","senha":"123"]
