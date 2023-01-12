# Importations des bibliothèques
import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt
from copy import deepcopy
from copy import copy
from couleur import Couleur
from tas import Tas

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

    # REQUETES

    def poids_cycle(self, cycle: np.ndarray) -> float:
        '''Renvoie le poids du cycle donné en paramètre'''
        poids = 0
        for i in range(len(cycle) - 1):
            poids += self.D[cycle[i] - 1, cycle[i + 1] - 1]
        return poids

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
        '''### Arête de poids minimum
        On sélectionne l'arête de poids minimum et on la supprime du graphe.
        On ajoute l'arête à la liste d'arêtes du cycle.
        On recommence jusqu'à obtenir n - 1 arêtes
        Une fois qu'on a n-1 arêtes, on crée un cycle à partir de ces arêtes'''
        
        temp_D = deepcopy(self.D)
        G = {}
        for i in range(1, self.n + 1):
            G[i] = []
        nb_arete = 0
        while  nb_arete < self.n - 1:
            # Recherche de l'arête de poids minimum
            min = np.inf
            min_index = (0, 0)
            for i in range(self.n):
                # Comme le graphe est complet et non orienté, la matrice D est symétrique
                # On ne parcourt donc que la partie triangulaire supérieure de la matrice
                for j in range(i + 1, self.n):
                    if temp_D[i, j] < min:
                        min = temp_D[i, j]
                        min_index = (i + 1, j + 1)
            if not self.forme_un_circuit(min_index[0], min_index[1], G):
                G[min_index[0]].append(min_index[1])
                G[min_index[1]].append(min_index[0])
                nb_arete += 1
            temp_D[min_index[0] - 1, min_index[1] - 1] = np.inf
        # On crée le cycle à partir de la liste d'arêtes
        sommet_courant = 0
        for key in G:
            if len(G[key]) == 1:
                sommet_courant = key
                break
        cycle = [sommet_courant]
        while len(cycle) < self.n:
            for s in G[sommet_courant]:
                if s not in cycle:
                    cycle.append(s)
                    sommet_courant = s
        cycle.append(cycle[0])
        return np.array(cycle)


    def forme_un_circuit(self, sommet1: int, sommet2: int, G: dict) -> bool:
        '''### Vérifie si l'arête (sommet1, sommet2) forme un circuit dans le graphe G
        G est représenté par une liste d'arêtes
        Cette méthode utilise l'algorithme d'exploration de graphes pour vérifier si
        sommet 2 est accessible à partir de sommet1'''
        frontiere = [sommet1]
        genere = [sommet1]
        if len(G[sommet1]) > 1 or len(G[sommet2]) > 1:
            return True
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
                        frontiere.append(successeur)              
        return False
    
    def Pvcprim(self) -> np.ndarray:
        '''### Utilise l'algorithme de Prim dans sa version efficace qui utilise un tas.
        On construit un arbre couvrant de poids minimum. On fait le parcours préfixe
        de l'arbre obtenu pour obtenir le cycle hamiltonien'''
        r = 1
        acm = []
        T = [r]
        # Le complémentaire de T dans S
        C_T = [i for i in range(1, self.n + 1) if i != r]
        # On fait pousser un acm à partir de la racine
        while len(T) != self.n:
            # Calcule du cocycle et de l'arête de poids minimum du cocycle
            tas = Tas() # Voir la classe Tas
            min = np.inf
            for sommet in T:
                for sommet_c in C_T:
                    tas.inserer((sommet, sommet_c), self.D[sommet - 1, sommet_c - 1])
            min = tas.racine()[0][1]
            # On ajoute l'arête de poids minimum à l'acm
            acm.append(tas.racine()[0],)
            # On ajoute le sommet pas dans T à l'arbre couvrant
            T.append(min)
            C_T.remove(min)
        res = [r]
        for a in acm:
            res.append(a[1])
        return res + [r]
    
    def Esdemisomme(self) -> np.ndarray:
        '''### Algorithme du branch and bound
        On regarde chaque solution possibles. On développe toujours
        la solution la plus prometteuses, c'est à dire, celle qui a la plus
        petite borne minorante.'''
        
        # Initialisation

        # Déterminer une borne minorante pour le poids du cycle hamiltonien
        # On utilise la matrice D pour calculer cette borne
        tas = Tas()
        # aretes_borne est la liste des poids des arêtes du cycle hamiltonien.
        # [p(1,x1), p(1,y1), p(2,x2), p(2,y2) ... p(n, xn), p(n, yn)]
        poids_aretes_borne = []
        # On construit un cycle hamiltonien à partir de la racine
        cycle = [1]
        temp_D = deepcopy(self.D)
        # On choisit les deux plus petites arêtes incidentes à chaque sommet : 
        for i in range(self.n):
            i_aretes = temp_D[i]
            i_aretes[i] = np.inf
            min1 = np.argmin(i_aretes)
            poids_aretes_borne.append(self.D[i, min1])
            i_aretes[min1] = np.inf
            poids_aretes_borne.append(self.D[i, np.argmin(i_aretes)])
        # On calcule la borne minorante
        borne = np.sum(poids_aretes_borne) / 2
        # On utilise un tas de priorité pour stocker les solutions et leur borne minorante.
        # On stocke également la liste des poids des arêtes du cycle hamiltonien pour
        # le calcul de la borne minorante.
        tas.inserer(([1], poids_aretes_borne), borne)

        # Boucle principal
        while len(cycle) < self.n:
            # On développe toujours la solution qui a la plus petite borne minorante,
            # c'est à dire la racine du tas.
            temp_racine_tas = tas.racine()[0][1]
            tas.supprimer()
            for i in range(self.n):
                if i + 1 not in cycle:
                    poids_aretes_borne = copy(temp_racine_tas)
                    poids_aretes_borne[(i + 1) * 2 - 1] = self.D[i, cycle[-1] - 1]
                    poids_aretes_borne[(cycle[-1] - 1) * 2 - 1] = self.D[cycle[-1] - 1, i]
                    # On calcule la nouvelle borne minorante
                    borne = np.sum(poids_aretes_borne) / 2
                    tas.inserer((cycle + [i + 1], poids_aretes_borne), borne)
            borne = tas.racine()[1]
            cycle = tas.racine()[0][0]
        return cycle + [1]

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
        plt.title("Poids du cycle : " + str(self.poids_cycle(cycle)))
        plt.show()

    def executer(self, i):
        '''### Exécute l'algorithme i'''
        dico = {1: self.Ppvoisin, 2: self.OptimisePpvoisin, 3: self.Apminimum, 4: self.Pvcprim, 5: self.Esdemisomme}
        return dico[i]()