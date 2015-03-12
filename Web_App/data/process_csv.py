f = open('size_new_twenty_50_50_10e_test15k_items.csv').read().split(',')
f = [name for name in f if name]
d = {}

for i, line in enumerate(f):
	name = line.split('/')[-1]
	d[name] = i

print d.keys()[:10]