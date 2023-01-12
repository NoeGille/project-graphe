from graphe import Graphe
import numpy as np
import matplotlib.pyplot as plt
import time

class App():
    '''###Application permettant de faire des statistiques sur les différents algos de la classe Graphe.
    Cette application contient une interface permettant d'intéragir avec les algorithmes dans un terminal de commande
    Cette interface permet de tester les algorithmes et d'afficher le graphe et le résultat de l'algorithme
    Cette interface permet aussi d'afficher des statistiques sur x exécution d'un algorithme.'''

    # CONSTANTES

    DEFAULT_NB_SOMMETS = 10
    DEFAULT_NB_ESSAIES = 10
    ALGO_NOM = {1: "Ppvoisin", 2: "OptimisePpvoisin", 3: "Apminimum", 4: "Pvcprim", 5: "Esdemisomme"}
    # Temps limite en secondes à partir duquel on considère que le temps d'exécution de l'algo n'est pas raisonnable
    TEMPS_MAX = 1
    # Nombre de sommets à ajouter à chaque itération pour le test du nombre de sommets croissant
    AJOUTE_SOMMET = 1

    # CONSTRUCTEUR

    def __init__(self):
        self.graphe = Graphe(self.DEFAULT_NB_SOMMETS)
        self.algo = 1
        self.nb_sommets = self.DEFAULT_NB_SOMMETS
        self.nb_essaies = self.DEFAULT_NB_ESSAIES
    
    # COMMANDES

    def run(self):
        '''Point de démarrage de l'application'''
        dico = {1: self.choisir_algo, 2: self.choisir_nb_sommets, 3: self.choisir_nb_essaies, 4: self.lancer_algo, 5: self.lancer_tous_algo, 6: self.test_nb_sommet_croissant, 7: self.quitter}
        print("Lancement de l'application")
        print("Ecrivez 7 pour quitter l'application depuis le menu principal ou ctrl+c dans le terminal.")
        print("Bienvenue dans l'application de test des algorithmes de recherche d'une solution au PVC.")
        print("Ecrivez le nombre correspondant à l'action que vous souhaitez effectuer.")
        while True:
            print("---------------------------------------------")
            print("Sélectionner un algorithme : ", self.ALGO_NOM[self.algo])
            print("Sélectionner un nombre de sommets : ", self.nb_sommets)
            print("Sélectionner un nombre d'essaies : ", self.nb_essaies)
            print("1) Choisir l'algorithme")
            print("2) Choisir le nombre de sommets")
            print("3) Choisir le nombre d'essaies")
            print("4) Lancer l'algorithme")
            print("5) Lancer tous les algorithmes")
            print("6) Test du temps d'exécution en fonction du nombre de sommets")
            print("7) Quitter")
            choix = int(input("Choix: "))
            if choix in dico.keys():
                dico[choix]()
            else:
                print("Choix invalide")
            
    
    def choisir_algo(self):
        print("1) Plus proche voisin")
        print("2) Plus proche voisin décroisé")
        print("3) Arête de poids minimum")
        print("4) Prim")
        print("5) Heuristique de la demi-somme")
        
        choix = int(input("Choix: "))
        if choix in self.ALGO_NOM.keys():
            self.algo = choix
            print("Algorithme choisi : ", self.ALGO_NOM[choix])
        else:
            print("Choix invalide")
        
    def choisir_nb_sommets(self):
        self.nb_sommets = int(input("Nombre de sommets: "))
        print("Nombre de sommets choisi : ", self.nb_sommets)
    
    def choisir_nb_essaies(self):
        self.nb_essaies = int(input("Nombre d'essaies: "))
        print("Nombre d'essaies choisi : ", self.nb_essaies)
    
    def lancer_algo(self):
        # Poids
        poids = []
        # Temps d'exécution
        temps = []
        
        for i in range(0, self.nb_essaies):
            self.graphe = Graphe(self.nb_sommets)
            start_time = time.time()
            cycle = self.graphe.executer(self.algo)
            temps.append(time.time() - start_time)
            poids.append(self.graphe.poids_cycle(cycle))

        print("Algorithme choisi : ", self.ALGO_NOM[self.algo])
        print("Poids moyen du cycle : ", np.array(poids).sum()/self.nb_essaies)
        print("Poids médian du cycle : ", np.median(poids))
        print("Temps moyen d'exécution : ", np.array(temps).sum()/self.nb_essaies)
        plt.hist(poids, bins = 50)
        plt.title("Performance de l'algorithme " + self.ALGO_NOM[self.algo] + " sur " + str(self.nb_essaies) + " essaies")
        plt.show()
    
    def lancer_tous_algo(self):
        graphes = [Graphe(self.nb_sommets) for i in range(0, self.nb_essaies)]
        for algo in range(1, 6):
            # Poids
            poids = []
            # Temps d'exécution
            temps = []
            for j in range(0, self.nb_essaies):
                self.graphe = graphes[j]
                start_time = time.time()
                cycle = self.graphe.executer(algo)
                temps.append(time.time() - start_time)
                poids.append(self.graphe.poids_cycle(cycle))
            print("Algorithme choisi : ", self.ALGO_NOM[algo])
            print("Poids moyen du cycle : ", np.array(poids).sum()/self.nb_essaies)
            print("Poids médian du cycle : ", np.median(poids))
            print("Temps moyen d'exécution : ", np.array(temps).sum()/self.nb_essaies)
            plt.hist(poids, bins = 50)
            plt.title("Performance de l'algorithme " + self.ALGO_NOM[algo] + " sur " + str(self.nb_essaies) + " essaies")
            plt.show()
    
    def test_nb_sommet_croissant(self):
        temps = 0
        old_nb_sommets = self.nb_sommets
        old_nb_essaies = self.nb_essaies
        self.nb_sommets = 1
        self.nb_essaies = 0
        
        print("Début des tests pour l'algo " + self.ALGO_NOM[self.algo])
        while temps < self.TEMPS_MAX:
            start_time = time.time()
            self.nb_sommets += self.AJOUTE_SOMMET
            Graphe(self.nb_sommets).executer(self.algo)
            temps = time.time() - start_time
            print("Temps d'exécution pour " + str(self.nb_sommets) + " : " + str(temps))
            
        print("Fin des tests pour l'algo " + self.ALGO_NOM[self.algo])
        print("Nombre de sommets max pour lequel le temps d'exécution est raisonable (inférieur à " + str(self.TEMPS_MAX) + " s): " + str(self.nb_sommets))
        self.nb_sommets = old_nb_sommets
        self.nb_essaies = old_nb_essaies

    def quitter(self):
        print("Fermeture de l'application")
        exit()

if __name__ == "__main__":
    app = App()
    app.run()