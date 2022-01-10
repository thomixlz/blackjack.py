"""
=== Règles : ===

Après avoir reçu deux cartes de départ, le joueur tire des cartes pour s’approcher de la valeur 21 sans la dépasser. Il est possible de tirer 0 cartes.
Le but du joueur est de battre le croupier en obtenant un total de points supérieur à celui-ci ou en voyant ce dernier dépasser 21.

Le croupier est un bot qui tir automatiquement des cartes tant qu'il ne dépasse pas 17. 

=== Mise : ===

Votre solde de départ est de 1000€ votre but et d'atteindre le maximum.

Votre mise est doublé une fois la manche remporté. 
Votre mise est perdu une fois la manche remporté par le croupier.

Si votre solde atteint 0€ il sera automatiquement remis à 1000€

=== Infos : ===

Dans ce blackjack l'AS vos 1 on ne peut pas split l'AS, c'est vraiment incompréhensible dans la console ausinon.

Bonne chance.

======================================================================================================================
======================================================================================================================
======================================================================================================================
======================================================================================================================

Notes :

Le jeu n'est pas complet et sera compléter prochainement, il manquera à ce projet quelques ajouts :


- Faire le jeu avec PyGames l'affichage est horrible à gerer avec la console pour un jeu de cartes et les autres fonctionnalité serait horrible à mettre en place ici.

- Mise Ajout =
   * Ajout side bet gauche (21+3) (prend en compte la carte retourner du croupier + les 2 du joueurs en début de partie pour esperer un gain x fois la mise si la combinaison fait 24)
   * Ajout side bet droite (anypair) nimporte quel pair pour le joueur rapporte *3 de la mise si pas meme couleur |*5 si meme couleur 
   * Ajout de la fonctionnalité "Double x2" (permet au joueur de doubler sa mise après ses 2 premières cartes mais ne peut pas HIT par la suite)

- Le split en cas d'AS (si As et joueur 'split' alors les cartes sont divisés en 2 zones de jeu et de calcul) (voir règles exact du split)


"""

CROUGE = '\033[91m'
CJAUNE = "\033[33m"
CVERT = "\033[32m"
CBLEU = "\033[34m"
CGRIS = "\033[90m"
CVIOLET = "\033[94m"


CEND = '\033[0m'

#############################################################
#################   OUTILS DE BASE         ##################
#############################################################

import random
import os
from itertools import product



formeDesCartes = ['Coeur', 'Carreau', 'Pique', 'Trèfle']
nomDesCartes = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
valeurDesCartes = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,'9': 9, '10': 10, 'Valet': 11, 'Dame': 12, 'Roi': 13, 'As': 1}

maPartieDeBlackJackEtat = True
maPartieDeBlackJackRestart = False

numeroCarte = 3

solde = 1000




#############################################################
#################     MES FONCTIONS       ###################
#############################################################


# Fonction : Création de mon deck de carte avec 52*6 cartes

def creationDesDecks(liste_formesDesCartes,liste_nomDesCartes):
    monDeck = []
    for suite, rank in product(liste_formesDesCartes,liste_nomDesCartes):
         monDeck.append((rank,suite))
    return monDeck


monDeckRandom = creationDesDecks(formeDesCartes,nomDesCartes)*6 #BlackJack = 6 jeux de cartes


# Fonction : Mélange les decks de cartes et renvoie 1 cartes 

def tir(monDeckRandom):
    random.shuffle(monDeckRandom) #Les 6 decks sont mélangés aléatoirement
    f1, s1 = random.choice(monDeckRandom)
    return f1, s1

maCarteRandom = tir(monDeckRandom)

#Fonction : Calcul la value de chaque cartes#

def tir_value(maCarteRandom,dic_valeurDesCartes): 
        return dic_valeurDesCartes.get(maCarteRandom[0])
            
            

maValeurDeCarte = tir_value(maCarteRandom,valeurDesCartes)


# Fonction : [Question] TIRER UNE CARTE ou RESTER SUR SA POSITION      




def tirOuResteJoueur(monDeckRandom,totalDebutJoueur):  

    global maPartieDeBlackJackEtat 
    global totalJoueur
    global totalCroupier
    global numeroCarte       #Variable devient celle à l'exterieur de ma fonction (variable principal)

    while maPartieDeBlackJackEtat == True:
    
        maQuestion = input(CJAUNE + "Tirer une autre carte HIT(tir) ? ou rester STAY(reste) ? Entrer 'h' (HIT) ou 's' (STAY): \n" +CEND)
        if maQuestion.lower() == 'h':

            maNewCarte = tir(monDeckRandom)  #tir une carte aléatoire
            print(CBLEU + "~~~~~ Main personnel actuel ~~~~~ \n" +CEND) #me l'affiche
            print(CVIOLET + "[ Carte",numeroCarte,"] =", maNewCarte[0], "de", maNewCarte[1], "!" + CEND) #me l'affiche

            totalJoueur += valeurDesCartes.get(maNewCarte[0]) #Calcul du nouveau total 
            print(CROUGE + "|| TOTAL ACTUEL =", totalJoueur, "||\n" +CEND)#me l'affiche

            numeroCarte += 1 

            if totalJoueur >=21:
                return False


        elif maQuestion.lower() == 's':
            print(CJAUNE + "\n[STAY] Vous avez décidé de ne pas prendre de carte suplémentaire" + CEND +  " (Le croupier HIT si son total est en dessous de 17 et retourne sa carte)\n")
            print(CROUGE + "|| VOTRE TOTAL FINAL =", totalJoueur, "||\n" +CEND)
            print(CROUGE + "|| TOTAL ACTUEL DU CROUPIER =", totalCroupier, "||\n" +CEND)
            return False

        else :  print(CROUGE + "Le croupier n'a pas compris la réponse" +CEND)
                      

# Fonction : [Affichage] AFFICHE LES DIFFERENTE POSSIBILITE DE FIN DE PARTIE

def leJoueurABust():
    print(CJAUNE + "Vous avez depassé 21 ! Vous avez perdu !" +CEND)


def leJoueurAGagner():
    print(CJAUNE + "Vous avez gagné !" +CEND)


def leCroupierABust():
    print(CJAUNE + "Le croupier a dépassé 21 ! C'est perdu pour lui !" +CEND)


def leCroupierAGagner():
    print(CJAUNE + "Le croupier a gagné !" +CEND)


#Fonction : [Affichage] AFFICHE LES CARTES DU DEBUTS DE GAMES


def ImprimeCarte(main,laCarte):
    i = len(main)
    print(CVIOLET + "[ Carte",i,"] =", laCarte[0], "de", laCarte[1], "!" +CEND)


#Fonction : Mise

def miseBJ(solde): 

    miseNombre = False

    while miseNombre == False:
        miseDuJoueur = input(CJAUNE + "Combien voulez miser dans cette partie ?" + CEND)
        try:
            mise = int(miseDuJoueur)
            if mise < 1:
                print(CROUGE + "Vous pouvez miser au minimum 1€ !" + CEND)
                miseNombre = False
            elif mise > solde:
                print(CROUGE + "Vous ne pouvez pas miser plus que votre solde !" + CEND)
                miseNombre = False
            else: 
                miseNombre = True
                return mise
        except ValueError:
            print(CROUGE + "Le croupier n'a pas compris la mise !" + CEND)
            miseNombre = False
        
 

#############################################################
#################   LE JEU DU BLACK JACK  ###################
#############################################################


    # PARTIE 1 = INITIALISATION DE LA PARTIE

while maPartieDeBlackJackEtat == True:
    print(CJAUNE +"\nNouvelle partie ! Le croupier est heureux de jouer avec vous Madame BENHAJJI !" + CEND)
    print(CVERT + "[SOLDE] = ", solde, "€\n" + CEND)
    print("=======================================================================\n")

    # MISE DU JOUEUR 

    mise = miseBJ(solde)

    print(CGRIS + "\nVotre mise est de", mise, "€ ! Votre gain potentiel est de", mise*2, "€ !\n" + CEND)

    print("=======================================================================\n")

    # Création des mains

    mainCroupier = []
    mainJoueur = []

    #### LE CROUPIER ####

    print(CBLEU + "~~~~~ Main de départ du groupier ~~~~~ \n" +CEND)

    #Tirage carte n*1 croupier     
    carte1Croupier = tir(monDeckRandom)
    mainCroupier.append(carte1Croupier)
    ImprimeCarte(mainCroupier,carte1Croupier)

    #Tirage carte n*2 croupier
    carte2Croupier = tir(monDeckRandom)
    mainCroupier.append(carte2Croupier)
    #ImprimeCarte(mainCroupier,carte2Croupier) invisible pour le joueur car ausinon c'est trop simple 
    print(CVIOLET + "[ Carte 2 ] = ??" + CEND)

    #Calcul du total des cartes du croupier 
    totalDebutCroupier = valeurDesCartes.get(carte1Croupier[0]) + valeurDesCartes.get(carte2Croupier[0])
    print(CROUGE + "|| TOTAL CROUPIER = ", totalDebutCroupier - valeurDesCartes.get(carte2Croupier[0]), "||\n" + CEND)


    #### LE JOUEUR ####

    print(CBLEU +"~~~~~ Main de départ personnel ~~~~~ \n" +CEND)

    #Tirage carte n*1 joueur     
    carte1Joueur = tir(monDeckRandom)
    mainJoueur.append(carte1Joueur)
    ImprimeCarte(mainJoueur,carte1Joueur)


    #Tirage carte n*2 joueur
    carte2Joueur = tir(monDeckRandom)
    mainJoueur.append(carte2Joueur)
    ImprimeCarte(mainJoueur,carte2Joueur)


    #Calcul du total des cartes du joueur 
    totalDebutJoueur = valeurDesCartes.get(carte1Joueur[0]) + valeurDesCartes.get(carte2Joueur[0]) 
    if totalDebutJoueur == 21:
        print(CROUGE + "|| VOTRE TOTAL = ", totalDebutJoueur," BLACKJACK ! ||\n" + CEND)
    else : print(CROUGE + "|| VOTRE TOTAL = ", totalDebutJoueur, "||\n" + CEND)


    #Calcul du total des joueur 
    totalJoueur= 0
    totalJoueur += totalDebutJoueur
    totalCroupier = 0
    totalCroupier += totalDebutCroupier

    #Demande au joueur si il veut tirer une carte ou non 
    hitOrStay = tirOuResteJoueur(monDeckRandom,totalDebutJoueur)


    #Si le joueur décide de rester alors la partie s'arrête et le calcul du résultat commencera
    if hitOrStay == False :
        maPartieDeBlackJackEtat=False    

    if maPartieDeBlackJackEtat == False:    

        ii = 3

        #Tant le croupier est en dessous de 17 et tant que le joueur c'est arrêter en dessous de 21 il devra tirer.
        while totalJoueur <= 21 and totalCroupier <= 17 and totalJoueur > totalCroupier :
                maNewCarteCroupier = tir(monDeckRandom)  #tir une carte aléatoire
                print(CBLEU + "~~~~~ Main Croupier ~~~~~ \n" + CEND) #me l'affiche
                print(CVIOLET +"[ Carte",ii,"] =", maNewCarteCroupier[0], "de", maNewCarteCroupier[1], "!" + CEND) #me l'affiche

                totalCroupier += valeurDesCartes.get(maNewCarteCroupier[0]) #Calcul du nouveau total 
                print(CROUGE + "|| TOTAL DU CROUPIER = ", totalCroupier, "||\n" +CEND)#me l'affiche

                ii +=1
        print("=======================================================================\n")
        print (">>> RESULTAT <<<\n")   
        #Si le croupier dépasse 21 et que le joueur est en dessous de 21 alors joueur gagne (pas forcément ausinon il affiche plusieurs fois les même choses)
        if totalCroupier > 21:
            leCroupierABust()
            leJoueurAGagner()
            solde += mise
            maPartieDeBlackJackRestart = True
                        
        if totalJoueur > 21:
            leJoueurABust()
            leCroupierAGagner()
            solde -= mise
            maPartieDeBlackJackRestart = True

        if totalCroupier <= 21 and totalJoueur <=21:
            if totalCroupier > totalJoueur:
                leCroupierAGagner()
                solde -= mise
                maPartieDeBlackJackRestart = True
            elif totalJoueur < totalJoueur:
                leJoueurAGagner()
                solde += mise
                maPartieDeBlackJackRestart = True
            else : 
                print(CJAUNE + "Egalité, personne n'a gagné !" +CEND)
                maPartieDeBlackJackRestart = True


      
         #Demande pour continuer ou partir               
        if maPartieDeBlackJackRestart == True:  
            print(CVERT + "\n[SOLDE] = ", solde, "€\n" + CEND)
            if solde == 0:
                solde += 1000    
            newPartie = input(CJAUNE + "\nVoulez-vous rejouer ? Entrer 'o' (OUI) ou 'n' (NON) :\n" + CEND)
            if newPartie.lower() == 'o':
                maPartieDeBlackJackEtat = not maPartieDeBlackJackEtat
                maPartieDeBlackJackRestart = not maPartieDeBlackJackRestart

                clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                clearConsole()
            else:
                print(CJAUNE + "A bientôt ! <3"+ CEND)
            
    
