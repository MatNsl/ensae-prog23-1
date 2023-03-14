from graph1 import Graph, graph_from_file, find, union, krustal


data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)
print(krustal("input/network.00.in"))
