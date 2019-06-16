#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import serial
import time
import sys
import picamera


# ==================== Initialisations ========================
#Changer le ttyUSB0 en USB1 si CNC pas reconnue
print('Veuillez entrer le port de la CNC (USB0 ou USB1)')
portcnc = raw_input()
#Connexion CNC
ser1 = serial.Serial('/dev/tty%s'%portcnc, 115200)

#Connexion Arduino
ser2 = serial.Serial('/dev/ttyUSB1',9600)
ser2.flushInput()

ser1.write('\r\n\r\n')
time.sleep(2)
ser1.flushInput()
ser1.write('g0 z-5 \n')
ser1.write("$H \n")
time.sleep(3) #delai permettant de s'assurer d'avoir un champ libre lors de la prise de vue

#Capture de la photo en 720*480
camera=picamera.PiCamera()
camera.resolution = (720,480)
camera.capture('Image1.jpg')

# ==================== Traitement de l'image ========================
lower_green = np.array([0,0, 42])  # valeur de vert supérieure
upper_green = np.array([90,164,198]) # valeur de vert inférieure

image = cv2.imread('Image1.jpg') # lecture de l'image
height, width, channels = image.shape # on récupère les dimensions de l'image

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # conversion de l'image en HSV

mask = cv2.inRange(img_hsv, lower_green, upper_green) # On créé un masque qui fixe les pixels qui ne nous intéresse pas en noir
res = cv2.bitwise_and(image,image, mask= mask) # On applique le masque
(h, s, v) = cv2.split(res)

imgtemp = cv2.GaussianBlur(res,(5,5),0) 
res_median = cv2.medianBlur(imgtemp,5) # On applique un filtre médian
img_bn = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # On récupère l'image initiale en noir et blanc

#On traces les contours de notre image où l'on a appliqué le masque
contours = cv2.Canny(res_median, 100, 2500, apertureSize=5)

# On binarise notre image en noir et blanc
for i in range(height):
    for j in range(width):
        if ((v[i][j] == 0) or (j<182) or (j>521) or (i<54) or (i>388)):
            img_bn[i][j]=0
        else :
            img_bn[i][j]=255


# On retire le bruit obtenu lors de l'application du masque
kernel = np.ones((5,5),np.uint8)
pre_closing = cv2.morphologyEx(img_bn, cv2.MORPH_CLOSE, kernel)
sec_closing = cv2.morphologyEx(pre_closing, cv2.MORPH_CLOSE, kernel)
closing = cv2.morphologyEx(sec_closing, cv2.MORPH_CLOSE, kernel)

#contours_bn = cv2.Canny(closing, 100, 2500, apertureSize=5) #On trace les contours


# On utilise la détection de Hough pour plus de précision
#Param2 de la Houghcircles a changer en fonction de la luminosité
circles = cv2.HoughCircles(closing,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=60,param2=8,minRadius=10,maxRadius=20)
circles = np.uint16(np.around(circles))

nb_pots = 0;
liste_pots = []
for i in circles[0,:]:
        #dessine le cercle extérieur
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
        #draw the center of the circle
        cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
        #ajout de pots à la liste
        nb_pots = nb_pots+1
        liste_pots.append(i[0])
        liste_pots.append(i[1])

cv2.imshow('Resultat du traitement',image)
print('Nombre de pots détectés = ',nb_pots)

#########################################Controle de l'image

cv2.waitKey(0)
cv2.destroyAllWindows = 0

print(liste_pots)
print((len(liste_pots)/2))

k=0

while( k <= (len(liste_pots)/2)):
    print(k)
    print('JE RENTRE')
    center_X = liste_pots[k]
    center_Y = liste_pots[k+1]
    OFFSET_X = 20
    OFFSET_Y = 200
    center_X_CNC = (-2.355 * center_X + 1228)//1 
    center_Y_CNC = (-2.385 * center_Y + 926.5)//1
    print('center_X', center_X)
    print('center_Y',center_Y)
    print('center_X_CNC', center_X_CNC)
    print('center_Y_CNC',center_Y_CNC)
    #Permet de s'assurer que la cnc ne tape pas dans le mur
    
    if(center_X_CNC > 0 and center_Y_CNC > 0 and center_X_CNC<800 and center_Y_CNC < 800):
        #On trace le chemin que doit suivre la CNC
        #On déplace la CNC a l'emplacement du centre avec l'offset nécessaire
        ser1.write('g0 x%s y%s \n'%(center_X_CNC - OFFSET_X,center_Y_CNC - OFFSET_Y))
        time.sleep(5)
        ser1.write('g0z-5 \n')
        #On positionne bien la pince pour effectuer la saisie
        center_offset = center_Y_CNC - 130
        ser1.write('g0 y%s \n'%(center_offset))
        time.sleep(7)
        #On envoie l'ordre de saisie à la pince
        ser2.write('F')
        
        time.sleep(5) #pause le temps de saisir notre pot
        #On remonte la CNC pour déplacer notre pot
        ser1.write('g0 z-25 \n')
        time.sleep(5)
        
        #On déplace notre pot a une position désirée
        ser1.write('g0 x%s y%s \n'%(k*50,0))
        time.sleep(5)
        #On pose notre pot
        ser1.write('g0 z0 \n')
        time.sleep(3)
        ser2.write('O')
        time.sleep(3) 
        #Retour à la position initiale pour effectuer la saisie suivante
        ser1.write('g0 z-60 \n')
        ser1.write('g0 x%s y%s \n'%(0,0))
        time.sleep(5)
    if(len(liste_pots) > 1) :
        k = k + 1




