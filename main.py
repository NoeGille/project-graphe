from graphe import Graphe

dico = {1:[2, 4], 2:[1, 4], 3:[5],4:[1,2], 5:[]}

g = Graphe(5)
print(g.Pvcprim())
g.dessiner()