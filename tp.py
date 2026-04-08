from pilefile import Pile, File
from graphelib import Graphe

import turtle



laby = [[0, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 0]]


class Labyrinte:


    def __init__(self,lab,depart, arrivee):
        self.lab = lab
        def coord(s):       #transforme les coordonnés des objet en tuple
            s = s.strip().strip("()") # enleve les espaces + parenthese
            parties = s.split(",")
            if len(parties) != 2:
                raise ValueError("Format invalide")
            try:
                if self.lab[int(parties[0])][int(parties[1])] == 0:
                    return (int(parties[0].strip()), int(parties[1].strip()))
                else:
                    print("point de départ ou arrivée invalide")
                    return None
            except ValueError:
                raise ValueError("coordonner non entiere")

        self.depart = coord(depart)
        self.arrivee = coord(arrivee)


        self.objet=Graphe()
        lignes = len(self.lab)
        colonnes = len(self.lab[0])
        # ajout des voisins
        for y in range(lignes):
            for x in range(colonnes):

                if self.lab[y][x] == 0: #vérifie si le point actuelle n'est pas un mur
                    point = (y, x)

                    directions = [(y - 1, x),   #haut
                                  (y + 1, x),   #bas
                                  (y, x - 1),   #gauche
                                  (y, x + 1)]   #droite
                    for ny, nx in directions:

                        if 0 <= ny < lignes and 0 <= nx < colonnes:
                            if self.lab[ny][nx] == 0:       #si le point voisin est égal a 0 alors ce n'est
                                                            # pas un mur et donc on peut l'ajouter comme voisin
                                voisin = (ny, nx)
                                self.objet.ajouteArete(point, voisin)


    #dfs

    def parcours_profondeur_laby_rec(self, G,depart,arrivee):
        '''Parcours d'un graphe en longueur a  partir du sommet départ jusqu'au sommet arrivée'''

        if depart== None or arrivee == None:
            return None
        else:
            arrivee=G.sommet(arrivee)
            nomarrivée=arrivee._nom
            marque = set()  # ensemble des sommets deja visité
            chemin=[] # liste des sommet parcourue qui amène au sommet arrivée
            def parcours_aux(G, som):
                chemin.append(som) #ajoute le sommet parcouru à la liste

                if som._nom == nomarrivée : #la fonction vérifie si le point visité est l'arrivée

                    return True

                marque.add(som)
                for voisin in som.listeVoisins():

                    if voisin not in marque: #la fonction s'assure que le sommet n'est pas dans l'ensemble si non elle tourne en rond
                        if parcours_aux(G, voisin): #appelle recursif
                            return True
                chemin.pop() #si la fonction recule, elle enleve le point qu'elle avait parcourue
                return False

        if parcours_aux(G, G.sommet(depart)):
            print("Sommets visités :", [str(s._nom) for s in chemin])
            return chemin
        else:
            print('Aucun chemin.')
            return None

    #bfs
    def parcours_largeur_laby(self, G, depart, arrivee):
        '''Parcours d'un graphe en largeur a  partir du sommet départ jusqu'au sommet arrivée'''
        if depart == None or arrivee == None:
            return None
        else:
            marque = set()
            chemin=[] #chemin des point parcouru
            parent={} # dictionnaire permettant de savoir l'origine de chaque point parcourue
            parent[depart] = None #le point de départ n'a pas d'origine
            depart=G.sommet(depart)
            arrivee=G.sommet(arrivee)
            nom_arrivee = arrivee._nom
            f = File()
            f.enfile(depart) #enfile le depart
            while not f.estvide(): #si file est vide la boucle s'arrete et on ne peut pas trouver de chemin
                s = f.defile()
                if s._nom == nom_arrivee: #la fonction vérifie si le point visité est l'arrivée

                    break

                if s not in marque:
                    marque.add(s)

                    for voisin in s.listeVoisins():
                        if voisin not in marque and voisin not in parent:#la fonction s'assure que le sommet n'est
                                                                        # pas dans l'ensemble sinon elle tourne en rond
                            f.enfile(voisin)
                            parent[voisin] = s
            if f.estvide():

                print("Aucun chemin trouvé")
                return None
            courant = arrivee
            while courant is not None:#ajoute les sommets parcourus en ordre inverse
                chemin.append(courant)
                courant = parent.get(courant) #remplace le point actuelle par son origine
            chemin.reverse()
            print("Sommets visités :", [str(s._nom) for s in chemin])
            return chemin



    def solutiondfs(self):
        return self.parcours_profondeur_laby_rec(self.objet,self.depart,self.arrivee)
    def solutionbfs(self):
        return self.parcours_largeur_laby(self.objet,self.depart,self.arrivee)

    def visualiser(self, chemin, titre="Solution Labyrinthe", couleur_chemin="blue"):
        """
        chemin : la liste des objets Sommet renvoyée par tes fonctions de solution
        """
        # On calcule la distance directement ici au lieu de la demander aux algos
        # La distance est le nombre de cases du chemin - 1 (les arêtes)
        if chemin ==None:
            return None
        else:
            distance = len(chemin) - 1 if chemin else 0

            # On récupère les dimensions depuis self.lab (puisque self.nb_lignes n'est pas défini dans le __init__)
            nb_lignes = len(self.lab)
            nb_cols = len(self.lab[0])
            TAILLE = 30

            ecran = turtle.Screen()
            ecran.setup(width=600, height=600)
            ecran.title(f"{titre} - Distance: {distance} arêtes")
            ecran.tracer(0)

            t = turtle.Turtle()
            t.hideturtle()

            # Calcul pour centrer parfaitement
            ox = -nb_cols * TAILLE / 2
            oy = nb_lignes * TAILLE / 2

            # Dessin de la grille
            for x in range(nb_lignes):
                for y in range(nb_cols):
                    px, py = ox + y * TAILLE, oy - x * TAILLE

                    # Choix de la couleur
                    if self.lab[x][y] == 1:
                        color = "black"
                    elif (x, y) == self.depart:
                        color = "green"
                    elif (x, y) == self.arrivee:
                        color = "red"
                    else:
                        color = "white"

                    t.penup()
                    t.goto(px, py)
                    t.pendown()
                    t.fillcolor(color)
                    t.begin_fill()
                    for _ in range(4):
                        t.forward(TAILLE)
                        t.right(90)
                    t.end_fill()

            ecran.update()

            # Dessin du chemin
            if chemin:
                ecran.tracer(1)
                t.penup()
                t.pensize(3)
                t.pencolor(couleur_chemin)

                for i, etape in enumerate(chemin):
                    # Tes algos retournent des objets "Sommet" de graphelib.
                    # L'attribut _nom contient déjà le tuple de coordonnées (x, y) ! Pas besoin de eval().
                    coord_tuple = etape._nom

                    # Aller au centre de la case
                    cx = ox + coord_tuple[1] * TAILLE + TAILLE / 2
                    cy = oy - coord_tuple[0] * TAILLE - TAILLE / 2
                    t.goto(cx, cy)
                    t.pendown()
                    if i == 0:
                        t.dot(10, "green")

                t.dot(10, "red")

            print(f"Visualisation terminée. Distance : {distance}")
            turtle.done()



c = Labyrinte(laby, '(0,0)', '(7,4)')
c.solutiondfs()
c.solutionbfs()
# On récupère juste le chemin
chemin_bfs = c.solutiondfs()

# On passe ce chemin directement à la visualisation
c.visualiser(chemin_bfs, titre="Solution DFS", couleur_chemin="blue")






from pilefile import Pile, File
from graphelib import Graphe

import turtle



laby = [[0, 0, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 1, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 0]]


class Labyrinte:


    def __init__(self,lab,depart, arrivee):
        self.lab = lab
        def coord(s):       #transforme les coordonnés des objet en tuple
            s = s.strip().strip("()") # enleve les espaces + parenthese
            parties = s.split(",")
            if len(parties) != 2:
                raise ValueError("Format invalide")
            try:
                if self.lab[int(parties[1])][int(parties[0])] == 0:
                    return (int(parties[1].strip()), int(parties[0].strip()))
                else:
                    print("point de départ ou arrivée invalide")
                    return None
            except ValueError:
                raise ValueError("coordonner non entiere")

        self.depart = coord(depart)
        self.arrivee = coord(arrivee)


        self.objet=Graphe()
        lignes = len(self.lab)
        colonnes = len(self.lab[0])
        # ajout des voisins
        for y in range(lignes):
            for x in range(colonnes):

                if self.lab[y][x] == 0: #vérifie si le point actuelle n'est pas un mur
                    point = (y, x)

                    directions = [(y - 1, x),   #haut
                                  (y + 1, x),   #bas
                                  (y, x - 1),   #gauche
                                  (y, x + 1)]   #droite
                    for ny, nx in directions:

                        if 0 <= ny < lignes and 0 <= nx < colonnes:
                            if self.lab[ny][nx] == 0:       #si le point voisin est égal a 0 alors ce n'est
                                                            # pas un mur et donc on peut l'ajouter comme voisin
                                voisin = (ny, nx)
                                self.objet.ajouteArete(point, voisin)


    #dfs

    def parcours_profondeur_laby_rec(self, G,depart,arrivee):
        '''Parcours d'un graphe en longueur a  partir du sommet départ jusqu'au sommet arrivée'''

        if depart== None or arrivee == None:
            return None
        else:
            arrivee=G.sommet(arrivee)
            nomarrivée=arrivee._nom
            marque = set()  # ensemble des sommets deja visité
            chemin=[] # liste des sommet parcourue qui amène au sommet arrivée
            def parcours_aux(G, som):
                chemin.append(som) #ajoute le sommet parcouru à la liste

                if som._nom == nomarrivée : #la fonction vérifie si le point visité est l'arrivée

                    return True

                marque.add(som)
                for voisin in som.listeVoisins():

                    if voisin not in marque: #la fonction s'assure que le sommet n'est pas dans l'ensemble si non elle tourne en rond
                        if parcours_aux(G, voisin): #appelle recursif
                            return True
                chemin.pop() #si la fonction recule, elle enleve le point qu'elle avait parcourue
                return False

        if parcours_aux(G, G.sommet(depart)):
            print("Sommets visités :", [str((s._nom[1],s._nom[0])) for s in chemin])
            return chemin
        else:
            print('Aucun chemin.')
            return None

    #bfs
    def parcours_largeur_laby(self, G, depart, arrivee):
        '''Parcours d'un graphe en largeur a  partir du sommet départ jusqu'au sommet arrivée'''
        if depart == None or arrivee == None:
            return None
        else:
            marque = set()
            chemin=[] #chemin des point parcouru
            parent={} # dictionnaire permettant de savoir l'origine de chaque point parcourue
            parent[depart] = None #le point de départ n'a pas d'origine
            depart=G.sommet(depart)
            arrivee=G.sommet(arrivee)
            nom_arrivee = arrivee._nom
            f = File()
            f.enfile(depart) #enfile le depart
            while not f.estvide(): #si file est vide la boucle s'arrete et on ne peut pas trouver de chemin
                s = f.defile()
                if s._nom == nom_arrivee: #la fonction vérifie si le point visité est l'arrivée

                    break

                if s not in marque:
                    marque.add(s)

                    for voisin in s.listeVoisins():
                        if voisin not in marque and voisin not in parent:#la fonction s'assure que le sommet n'est
                                                                        # pas dans l'ensemble sinon elle tourne en rond
                            f.enfile(voisin)
                            parent[voisin] = s
            if f.estvide():

                print("Aucun chemin trouvé")
                return None
            courant = arrivee
            while courant is not None:#ajoute les sommets parcourus en ordre inverse
                chemin.append(courant)
                courant = parent.get(courant) #remplace le point actuelle par son origine
            chemin.reverse()
            print("Sommets visités :", [str((s._nom[1],s._nom[0]))for s in chemin])
            return chemin



    def solutiondfs(self):
        return self.parcours_profondeur_laby_rec(self.objet,self.depart,self.arrivee)
    def solutionbfs(self):
        return self.parcours_largeur_laby(self.objet,self.depart,self.arrivee)

    def visualiser(self, chemin, titre="Solution Labyrinthe", couleur_chemin="blue"):
        """
        chemin : la liste des objets Sommet renvoyée par tes fonctions de solution
        """
        # On calcule la distance directement ici au lieu de la demander aux algos
        # La distance est le nombre de cases du chemin - 1 (les arêtes)
        if chemin ==None:
            return None
        else:
            distance = len(chemin) - 1 if chemin else 0

            # On récupère les dimensions depuis self.lab (puisque self.nb_lignes n'est pas défini dans le __init__)
            nb_lignes = len(self.lab)
            nb_cols = len(self.lab[0])
            TAILLE = 30

            ecran = turtle.Screen()
            ecran.setup(width=600, height=600)
            ecran.title(f"{titre} - Distance: {distance} arêtes")
            ecran.tracer(0)

            t = turtle.Turtle()
            t.hideturtle()

            # Calcul pour centrer parfaitement
            ox = -nb_cols * TAILLE / 2
            oy = nb_lignes * TAILLE / 2

            # Dessin de la grille
            for x in range(nb_lignes):
                for y in range(nb_cols):
                    px, py = ox + y * TAILLE, oy - x * TAILLE

                    # Choix de la couleur
                    if self.lab[x][y] == 1:
                        color = "black"
                    elif (x, y) == self.depart:
                        color = "green"
                    elif (x, y) == self.arrivee:
                        color = "red"
                    else:
                        color = "white"

                    t.penup()
                    t.goto(px, py)
                    t.pendown()
                    t.fillcolor(color)
                    t.begin_fill()
                    for _ in range(4):
                        t.forward(TAILLE)
                        t.right(90)
                    t.end_fill()

            ecran.update()

            # Dessin du chemin
            if chemin:
                ecran.tracer(1)
                t.penup()
                t.pensize(3)
                t.pencolor(couleur_chemin)

                for i, etape in enumerate(chemin):
                    # Tes algos retournent des objets "Sommet" de graphelib.
                    # L'attribut _nom contient déjà le tuple de coordonnées (x, y) ! Pas besoin de eval().
                    coord_tuple = etape._nom

                    # Aller au centre de la case
                    cx = ox + coord_tuple[1] * TAILLE + TAILLE / 2
                    cy = oy - coord_tuple[0] * TAILLE - TAILLE / 2
                    t.goto(cx, cy)
                    t.pendown()
                    if i == 0:
                        t.dot(10, "green")

                t.dot(10, "red")

            print(f"Visualisation terminée. Distance : {distance}")
            turtle.done()



c = Labyrinte(laby, '(1,0)', '(4,7)')
c.solutiondfs()
c.solutionbfs()
# On récupère juste le chemin
chemin_bfs = c.solutionbfs()

# On passe ce chemin directement à la visualisation
c.visualiser(chemin_bfs, titre="Solution DFS", couleur_chemin="blue")
