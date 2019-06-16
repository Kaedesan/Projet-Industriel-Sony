##########################################################################################
######################################	      ############################################			
###################################### README ############################################
######################################        ############################################
##########################################################################################

Ce README a pour objectif de d�crire le fonctionnent du syst�me de pr�hension de pots et de mottes automatis�s pour
le robot ROMI d�velopp� par le laboratoire de recherche SONY CSL, repr�sent� par COLLIAUX David.

******************************
* Contacts des �tudiants :   *
* rob4.sonycsl@gmail.com     *
******************************

/!\ ATTENTION /!\ : Avant l'utilisation de notre code, il est n�cessaire de recalibrer la CNC. En effet, cette derni�re
pr�sente parfois des probl�mes d'initialisation : il est pr�f�rable de s'assurer qu'elle poss�dera le comportement
ad�quat lors de l'utilisation.

###################################### Recalibrage de la CNC   #############################################	

	*Se connecter � la CNC par le port serial, et �tablir une communication en 115200.
	*D�verouiller la CNC (commande '$X') , puis lancer un Homing de la CNC (commande '$H')
	*S'assurer que la commande 'g0z0' ne d�place pas la CNC selon z
	*S'assurer que la commande 'g0z2' permet un d�placement vers le bas du bras
	*S'assurer que la commande 'g0z-25' permet un d�placement vers le haut
	*Relancer un Homing depuis la commande ('$H')

La CNC est pr�te � �tre utilis�e avec notre programme.

###################################### Recalibrage des couleurs #############################################
En cas de changement de milieu, il se peut que notre algorithme ne d�tecte plus le vert de la m�me fa�on (changement
des nuances de vert du � la luminosit�). Il est alors n�cessaire de recalibrer les couleurs.

	*Lancer le programme SetupColor.py
	*R�gler les barres afin de d�tecter le vert du centre des pots
	*Changer les valeurs de low_green et upper_green dans le programme main.py avec les nouvelles valeurs

###################################### D�tection et saisie de pots ###########################################
Le programme suivant permet d'effectuer la d�tection et la saisie de multiples pots de forme circulaire dont 
	
	*Brancher la pince sur le port USB de la Raspberry
	*Lancer le programme main.py � l'aide Python2
	*Attendre que l'initialisation de la CNC se fasse.
	/!\ ATTENTION /!\ : Ne rien placer sous la CNC pendant la prise de vue.
	*L'algorithme renvoie alors une image des pots d�tect�s et le nombre de pots
	*Une fois le contr�le visuel effectu�, appuyer sur une touche pour lancer le cycle.


###################################### Probl�me avec l'Arduino #################################################
En cas de probl�me avec l'arduino, il est possible de t�l�verser � nouveau le code dans la pince.

	*T�l�verser le code