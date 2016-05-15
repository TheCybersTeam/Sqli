class Db:
	name = None
	tables = []

	def setName(self, name):
		self.name = name

	def setTables(self, table):
		self.tables.append(table)

# Bancos
db = []

# Add novo banco
db.append(Db())
db[0].setName("Teste")

# Mostra bancos
for i in db:
	pass
	#print i.name

class Tb:
	name = None
	def setName(self,name):
		self.name = name

tb = Tb()
tb.setName("users")
db[0].setTables(tb)

for i in db:
	for j in i.tables:
		print j.name
