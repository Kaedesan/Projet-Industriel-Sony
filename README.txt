##########################################################################################
######################################	      ############################################			
###################################### README ############################################
######################################        ############################################
##########################################################################################

Ce README a pour objectif de décrire le fonctionnent du système de préhension de pots et de mottes automatisés pour
le robot ROMI développé par le laboratoire de recherche SONY CSL, représenté par COLLIAUX David.

******************************
* Contacts des étudiants :   *
* rob4.sonycsl@gmail.com     *
******************************

/!\ ATTENTION /!\ : Avant l'utilisation de notre code, il est nécessaire de recalibrer la CNC. En effet, cette dernière
présente parfois des problèmes d'initialisation : il est préférable de s'assurer qu'elle possèdera le comportement
adéquat lors de l'utilisation.

###################################### Recalibrage de la CNC   #############################################	

	*Se connecter à la CNC par le port serial, et établir une communication en 115200.
	*Déverouiller la CNC (commande '$X') , puis lancer un Homing de la CNC (commande '$H')
	*S'assurer que la commande 'g0z0' ne déplace pas la CNC selon z
	*S'assurer que la commande 'g0z2' permet un déplacement vers le bas du bras
	*S'assurer que la commande 'g0z-25' permet un déplacement vers le haut
	*Relancer un Homing depuis la commande ('$H')

La CNC est prête à être utilisée avec notre programme.

###################################### Recalibrage des couleurs #############################################
En cas de changement de milieu, il se peut que notre algorithme ne détecte plus le vert de la même façon (changement
des nuances de vert du à la luminosité). Il est alors nécessaire de recalibrer les couleurs.

	*Lancer le programme SetupColor.py
	*Régler les barres afin de détecter le vert du centre des pots
	*Changer les valeurs de low_green et upper_green dans le programme main.py avec les nouvelles valeurs

###################################### Détection et saisie de pots ###########################################
Le programme suivant permet d'effectuer la détection et la saisie de multiples pots de forme circulaire dont 
	
	*Brancher la pince sur le port USB de la Raspberry
	*Lancer le programme main.py à l'aide Python2
	*Attendre que l'initialisation de la CNC se fasse.
	/!\ ATTENTION /!\ : Ne rien placer sous la CNC pendant la prise de vue.
	*L'algorithme renvoie alors une image des pots détectés et le nombre de pots
	*Une fois le contrôle visuel effectué, appuyer sur une touche pour lancer le cycle.


###################################### Problème avec l'Arduino #################################################
En cas de problème avec l'arduino, il est possible de téléverser à nouveau le code dans la pince.

	*Téléverser le code