import mincemeat
import glob
import csv

text_files = glob.glob('/home/weto/workspace_puc/bigdata/exerc2/join/*')

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source = dict((file_name, file_contents(file_name))for file_name in text_files)

def mapfn(k,v):
    print 'map' + k
    for line in v.splitlines():
        if k == "/home/weto/workspace_puc/bigdata/exerc2/join/2.2-vendas.csv":
            yield line.split(';')[0], 'vendas' + ':' + line.split(';')[5]                
        if k == "/home/weto/workspace_puc/bigdata/exerc2/join/2.2-filiais.csv":
            yield line.split(';')[0], 'filiais' + ':' + line.split(';')[1]                

def reducefn(k,v):
    print 'reduce ' + k
    total = 0
    for index, item in enumerate(v):
        if item.split(":")[0] == "vendas":
            total = int(item.split(":")[1]) + total
        if item.split(":")[0] == "filiais":
            NomeFilial = item.split(":")[1]
    L = list()
    L.append(NomeFilial + " , " + str(total))
    return L

s = mincemeat.Server()
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")

w = csv.writer(open("RESULT.csv","w"))
for k, v in results.items():
    w.writerow([k,v])
