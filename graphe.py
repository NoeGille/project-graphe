# Importations des bibliothèques
import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt
from copy import deepcopy

from enum import Enum

class Couleur(Enum):
    '''Enumération des couleurs qui représente l'état d'exploration d'un sommet pour
    le parcours en profondeur'''
    BLANC = 0
    GRIS = 1
    NOIR = 2

class Graphe():
    '''## Un graphe non orienté, complet et valué modélisant le problème du voyageur de commerce'''

    # CONSTANTES

    DEFAULT_NB_SOMMET = 5

    # CONSTRUCTEUR

    def __init__(self, n = DEFAULT_NB_SOMMET):
        '''Crée un graphe de n sommets'''
        self.n = n
        self.matrice = np.zeros((n, n), dtype=int)
        self.x = rd.rand(n)
        self.y = rd.rand(n)
        self.D = np.zeros((n, n), dtype=float)
        # D[i,j] vaut la distance euclidienne entre i et j
        for i in range(n):
            for j in range(n):
                self.D[i, j] = np.sqrt((self.x[i] - self.x[j])**2 + (self.y[i] - self.y[j])**2)
        print("Création du graphe")
    # ALGORITHMES

    def Ppvoisin(self) -> np.ndarray:
        '''### Algorithme du plus proche voisin'''
        # On initialise les variables
        # On commence par le sommet 0
        sommet_courant = 0
        sommet_visite = np.zeros(self.n + 1, dtype=np.uint8)
        sommet_visite[0] = 0
        for i in range(1, self.n):
            dist_min = np.inf
            # On cherche le sommet le plus proche
            for j in range(self.n):
                if self.D[sommet_courant, j] < dist_min and j not in sommet_visite:
                    dist_min = self.D[sommet_courant, j]
                    # On met à jour le sommet le plus proche
                    sommet_visite[i] = j
            # On met à jour le sommet courant
            sommet_courant = sommet_visite[i]
        return sommet_visite + 1

    def OptimisePpvoisin(self) -> np.ndarray:
        '''Si deux arêtes se croisent, 
        on cherche un autre chemin qui les décroise. 
        Si ce chemin est plus court, on le prend'''
        cycle = self.Ppvoisin()
        for i in range(0, self.n - 2):
            a1 = (cycle[i], cycle[i + 1])
            # pour tout couple (i, j), i < j - 1
            # Cela évite de tester plusieurs fois le même croisement d'arêtes
            for j in range(i + 2, self.n):
                if not(cycle[j] in a1 or cycle[j + 1] in a1):
                    a2 = (cycle[j], cycle[j + 1])
                    if self.croisement(a1[0], a1[1], a2[0], a2[1]):
                        invert = cycle[j: i: -1]
                        cycle_decroise = np.concatenate((cycle[0 : i + 1], invert, cycle[j + 1 : self.n + 1]))
                        if self.D[cycle_decroise[:-1] - 1, cycle_decroise[1:] - 1].sum() < self.D[cycle[:-1] - 1, cycle[1:] - 1].sum():
                            cycle = cycle_decroise
        return cycle

    def croisement(self, s1: int, s2: int, s3: int, s4: int) -> bool:
        '''### Vérifie si les arêtes (s1, s2) et (s3, s4) se croisent'''
        return self.ccw(s1, s3, s4) != self.ccw(s2, s3, s4) and self.ccw(s1, s2, s3) != self.ccw(s1, s2, s4)
        
    def ccw(self, A,B,C):
        return (self.y[C - 1] - self.y[A - 1]) * (self.x[B - 1] - self.x[A - 1]) > (self.y[B - 1] - self.y[A - 1]) * (self.x[C - 1] - self.x[A - 1])
        
    def Apminimum(self) -> np.ndarray:
        '''### Arête de poids minimum'''
        

    def forme_un_circuit(self, sommet1: int, sommet2: int, G: dict) -> bool:
        '''### Vérifie si l'arête (sommet1, sommet2) forme un circuit dans le graphe G
        Cette méthode utilise l'algorithme d'exploration de graphes pour vérifier si
        sommet 2 est accessible à partir de sommet1'''
        frontiere = [sommet1]
        genere = [sommet1]
        for i in range(0, self.n):
            while len(frontiere) > 0:
                # On choisit toujours le premier sommet de la frontiere
                sommet_choisi = frontiere[0]
                frontiere = frontiere[1:]
                for successeur in G[sommet_choisi]:
                    if successeur == sommet2:
                        return True
                    if successeur not in genere:
                        genere.append(successeur)
                        frontiere.append(sommet_choisi)
        return False

    def Pvcprim(self) -> np.ndarray:
        '''### Utilise l'arbre couvrant de poids minimum pour trouver un cycle hamiltonien 
        de poids minimum'''
        pass

    def Branch_and_bound(self) -> np.ndarray:
        '''### Algorithme du branch and bound'''
        pass

    # COMMANDES

    def __affiche_plan(self) -> None:
        '''Affiche le plan du graphe représenté par un nuage de points et d'arêtes'''
        plt.scatter(self.x, self.y,)
        for i in range(self.n):
            plt.text(self.x[i], self.y[i], str(i + 1))
        # alpha est la matrice de valeur de transparence des liens
        alpha = np.where(self.D > 1., 1. / 3., self.D / 3)
        for i in range(self.n):
            for j in range(self.n):
                plt.plot([self.x[i], self.x[j]], [self.y[i], self.y[j]], color='blue', alpha=alpha[i,j])

    
    def dessiner(self, cycle = []):
        '''### Dessine le graphe en bleu et si il est donné en paramètre un cycle, le dessine en rouge'''
        self.__affiche_plan()
        for i in range(len(cycle) - 1):
            plt.plot([self.x[cycle[i] - 1], self.x[cycle[i + 1] - 1]], [self.y[cycle[i] - 1], self.y[cycle[i + 1] - 1]], color='red')
        plt.show()

    # EVENTUELLEMENT UTILE
    def __trouver_rapide(self, sommet: int) -> int:
        '''Trouve la racine du sommet dans le graphe G et fais la compression de chemin'''

        i = sommet

        # Recherche de la racine
        while self.pere[i] > 0:
            i = self.pere[i]
        res = i
        i = sommet

        # Compression de chemin
        while self.pere[i] > 0:
            j = i
            self.pere[j] = res
            i = self.pere[i]
        
        return res

    def __reunir_pondere(self, r1, r2):
        '''### Raccroche la racine de l'arbre de poids minimum à la racine de l'arbre de poids maximum'''
        if r1 != r2:
            if self.pere[r1] < self.pere[r2]:
                self.pere[r1] += self.pere[r2]
                self.pere[r2] = r1
            else:
                self.pere[r2] += self.pere[r1]
                self.pere[r1] = r2
                
if __name__ == '__main__':
    g = Graphe(5)
    print(g.Ppvoisin())
    g.Apminimum()