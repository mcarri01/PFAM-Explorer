from flask import Flask
from flask import Flask, request, render_template
import json
import subprocess
import numpy as np
import re
import networkx as nx
from networkx.readwrite import json_graph


app = Flask(__name__)
matpat = '>(.+)\n([^>]+)'
content = open("seqidentmatrices.fasta").read()
fam2prot = json.load(open('fam2prot.json'))
families = {}
for m in re.findall(matpat, content):
    header = m[0].rstrip().split()
    famname = header[0]
    matrix = m[1].split('\n')[0:-1]
    matrix = [[float(entry) for entry in row.strip().split(' ')] for row in matrix]
    matrix = np.matrix(matrix)
    G = nx.from_numpy_matrix(matrix)
    mapping = dict(zip(G.nodes(), fam2prot[famname]))
    G.remove_edges_from([(i,i) for i in G.nodes()])
    G = nx.relabel_nodes(G,mapping)
    graphdata = json_graph.node_link_data(G)
    families[famname] = graphdata

@app.route('/')
def index():
    data = subprocess.check_output("python matparse.py < seqidentmatrices.fasta 0", shell=True).strip("\n")
    return render_template('index.html', data=data)

@app.route("/threshold", methods=['POST'])
def getThreshold():
    thresholdList = "".join(request.form['data'].split()).replace(',', ' ')
    print(thresholdList)
    data = subprocess.check_output("python matparse.py < seqidentmatrices.fasta %s" % thresholdList, shell=True)
    return json.dumps(data)

@app.route("/graph/<string:family>/<int:slider>")
def getGraph(family, slider):
    title = '<a href="http://pfam.xfam.org/family/'+family+'">'+family+'</a>'
    return render_template('graph.html', slider=slider, title=title, data=json.dumps(families[family]))

if __name__ == "__main__":
    app.run()
