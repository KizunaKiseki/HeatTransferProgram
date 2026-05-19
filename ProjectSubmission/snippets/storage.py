import pandas

ℕ1 = ['n0','n1']
ℕ2 = ['n0','n1','n2']


def read_mesh(file_name):
	# Types for all columns in short form
	types = {
		str:'name color',
		int:'id material n0 n1 n2',
		float:'x y T q ρ k Cₚ',
		}
	# Invert types dictionary for pandas format
	conv = {
		column:dtype
		for dtype,columns in types.items()
		for column in columns.split()
		}
	
	# Read all sheets in file as dataframes
	mesh = pandas.read_excel(file_name,None,converters=conv)
	return mesh


def write_mesh(mesh,file_name):
	with pandas.ExcelWriter(file_name) as excel:
		for (sheet,data) in mesh.items():
			data.to_excel(excel,sheet_name=sheet,index=False)


def print_mesh(mesh):
	for (k,(sheet,data)) in enumerate(mesh.items()):
		if k!=0:
			print()
		print(f'=== {sheet} ===')
		print(data)


def get_nodes(mesh):
	x = mesh['XY']['x'].values
	y = mesh['XY']['y'].values
	return x,y
