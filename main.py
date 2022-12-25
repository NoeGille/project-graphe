from graphe import Graphe

dico = {1:[2, 4], 2:[1, 4], 3:[5],4:[1,2], 5:[]}

g = Graphe(15)
cycle = g.Ppvoisin()
cycle_opti = g.OptimisePpvoisin()
print(g.Ppvoisin())
print(g.OptimisePpvoisin())
print(g.Apminimum())