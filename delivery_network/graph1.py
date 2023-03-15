class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0


    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        """
        We create the nodes needed for the edge if they do not already exist.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        """
        Two values are added to our dictionary self.graph,
        keys being node1 and node2.
        """
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
        
    

    def get_path_with_power(self, src, dest, power):
        visited={nodes:False for nodes in self.nodes}
        path=[]

        """
        We use booleans in order not to have any 'infinite' loop.
        """
        def visite(nodes,path):
            visited[nodes]=True
            path.append(nodes)
            print(path)
            if nodes==dest:
                return path
            elif nodes!=dest:
                for neighbor in self.graph[nodes]:
                    power_c,neighbor_id=neighbor[1],neighbor[0]
                    if visited[neighbor_id]==False and power_c<=power:
                        return visite(neighbor_id,path)
                    elif visited[neighbor_id]== True and nodes==dest:
                        return path
            return None 
        
        t=visite(src,path)
        return t
    """
    Result of the test (tests/test_s1q3_node_reachable.py):
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK
    """

    def connected_components(self):
        liste=[]
        node_visited={nodes:False for nodes in self.nodes}

        """
        Another function is used to do a deep first search (dfs).
        """
        def dfs(nodes):
            composant=[nodes]
            for voisin in self.graph[nodes]:
                voisin=voisin[0]
                if not node_visited[voisin]:
                    node_visited[voisin]=True
                    composant=composant+dfs(voisin)
            return composant
        for node in self.nodes:
            if not node_visited[node]:
                liste.append(dfs(node))
        return liste


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component),
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))

    """
    Results of the test (tests/test_s1q2_connected_components.py):
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK

    For network.02.in:
    {frozenset({9}), frozenset({8}), frozenset({7}),
    frozenset({10}), frozenset({6}), frozenset({1, 2, 3, 4}), frozenset({5})}
    """

    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        L=[]
        N=[]
        for nodes in self.nodes :
            N.append(nodes)
            for city in self.graph[nodes]:
                if city[0] not in N:  # In order not to take the same power twice for the same edge
                   L.append(city[1])
        L.sort()
        i=0 
        while i<len(L) and self.get_path_with_power(src,dest,L[i])== None:
            i=i+1
        return L[i],self.get_path_with_power(src,dest,L[i])

    def get_path_and_power(self,src,dest,power):
        visited={nodes:False for nodes in self.nodes}
        path=[]
        nb_edges=len(self.nodes)-1
        e=0 #pour compter le nombre d'arêtes déja parcourues. 

        def visite(nodes,path):
            visited[nodes]=True
            path.append(nodes)
            print(path)
            while e < nb_edges+1:
                if nodes==dest:
                     return path
                elif nodes!=dest:
                    for neighbor in self.graph[nodes]:
                        power_c,neighbor_id=neighbor[1],neighbor[0]
                        if visited[neighbor_id]==False and power_c<=power:
                            e = e+1
                            return visite(neighbor_id,path)
                        elif visited[neighbor_id]== True and nodes==dest:
                            return path
                return None 
        t=visite(src,path)
        return t


def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4: # s1q4: Taking into account the distance if it exists.
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g

"""
Result for s1q1 (tests/test_s1q1_graph_loading.py):
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

Result for s1q4:
The graph has 10 nodes and 4 edges.
1-->[(4, 11, 6), (2, 4, 89)]
2-->[(3, 4, 3), (1, 4, 89)]
3-->[(2, 4, 3), (4, 4, 2)]
4-->[(3, 4, 2), (1, 11, 6)]
5-->[]
6-->[]
7-->[]
8-->[]
9-->[]
10-->[]
"""

def find(nodes, link): #on veut trouver grâce à cette fonction dans quel graphe le noeud est.
        #si deux noeuds ont le même link alors ils sont dans le même graphe
        if link[nodes]==nodes: 
            return nodes
        return find(link[nodes],link)
     

def union(nodes_1,nodes_2,link,rank):
    root1=find(nodes_1,link)
    root2=find(nodes_2,link)
    if rank[root1]>rank[root2]: #on ajoute root2 au graphe contenant root1, rank sert juste à définir un ordre 
        link[root2]=root1
    elif rank[root1]<rank[root2]: #on ajoute root1 au graphe contenant root2 
        link[root1]=root2 
    else :
        link[root2]=root1
        rank[root1]+=1


def krustal(g):
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
    liste_nodes=list(range(1,n+1))
    min_tree={nodes:[] for nodes in liste_nodes}
    e=0
    i=0
    edges=[]
    rank={nodes:0 for nodes in liste_nodes}
    link={nodes:nodes for nodes in liste_nodes} # At the beginning, each node is in a graph of which it is the only component. 
        
    for nodes in liste_nodes : # We create a list that contains the edges i.e., a list composed of sub-lists
        # where each sub-list contains both vertex and the minimal power associated.
        for neighbor in g[nodes]:
            edges.append([nodes,neighbor[0],neighbor[1]])

    edges_sorted=sorted(edges, key=lambda item: item[2])

    while e < len(liste_nodes) - 1 and i<len(edges_sorted): # It is known that there are no more than "number of nodes - 1" edges in a tree.
        n_1,n_2,p_m = edges_sorted[i] 
        i = i + 1
        x = find(n_1, link)
        y = find(n_2, link)

        if x != y:
            e = e + 1
            min_tree[n_1].append([n_2,p_m]) # If both nodes are not part of the same connected graph, then we add the edge that links them.
            union(x, y, link, rank)
        
    return min_tree

"""
We find the time needed thanks to time.perf_counter()
"""
import time

def estimated_time(filename):
    with open(filename, "r") as file:
        n = map(int, file.readline())
        start=time.perf_counter()
        for i in range(20):
            src,dest,power=list(map(int, file.readline().split()))
            g.min_power(scr,dest)
        end=timz.perf_counter()
    return ((end-start)/10)*len(T)