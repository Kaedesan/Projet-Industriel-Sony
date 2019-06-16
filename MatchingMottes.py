#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import morphology, label

lower_green = np.array([0,48, 43])  # valeur de vert supérieure
upper_green = np.array([168,189,137]) # valeur de vert inférieure


image = cv2.imread('testMultiple.jpg') # lecture de l'image
image_rs=cv2.resize(image,(1080,720))

height, width, channels = image_rs.shape # on récupère les dimensions de l'image

img_hsv = cv2.cvtColor(image_rs, cv2.COLOR_BGR2HSV) # conversion de l'image en HSV


mask = cv2.inRange(img_hsv, lower_green, upper_green) # On créé un masque qui fixe les pixels qui ne nous intéresse pas en noir

res = cv2.bitwise_and(image_rs,image_rs, mask= mask) # On applique le masque
#cv2.imshow('Résultat masque',res) # Affichage de l'image après application du masque
(h, s, v) = cv2.split(res)

imgtemp = cv2.GaussianBlur(res,(5,5),0) 
res_median = cv2.medianBlur(imgtemp,5) # On applique un filtre médian
#cv2.imshow('Résultat lissage',res_median) # Affichage du résultat

img_bn = cv2.cvtColor(image_rs,cv2.COLOR_BGR2GRAY) # On récupère l'image initiale en noir et blanc


#cv2.imshow('Resultat contours',contours)

# On binarise notre image en noir et blanc
for i in range(height):
	for j in range(width):
		#if ((v[i][j] == 0) or (j<182) or (j>521) or (i<54) or (i>388)): # protection sur i et j pour les zones non atteignables par la CNC
		if (v[i][j] == 0):
			img_bn[i][j]=0
		else :
			img_bn[i][j]=255
        

# On applique une fermeture pour uniformiser les cibles et améliorer le résultat de la détection
kernel = np.ones((5,5),np.uint8)
pre_closing = cv2.morphologyEx(img_bn, cv2.MORPH_CLOSE, kernel)
sec_closing = cv2.morphologyEx(pre_closing, cv2.MORPH_CLOSE, kernel)
pre_closing = cv2.morphologyEx(sec_closing, cv2.MORPH_CLOSE, kernel)
sec_closing = cv2.morphologyEx(pre_closing, cv2.MORPH_CLOSE, kernel)
pre_closing = cv2.morphologyEx(sec_closing, cv2.MORPH_CLOSE, kernel)
sec_closing = cv2.morphologyEx(pre_closing, cv2.MORPH_CLOSE, kernel)
closing = cv2.morphologyEx(sec_closing, cv2.MORPH_CLOSE, kernel)


# Détection des différents corps sur l'image
lbl, nb_elem = label(closing)
# Size threshold.
min_size = 80 # pixels
box = []
for i in range(1, nb_elem + 1):
	py, px = np.nonzero(lbl == i)
	xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
	# Four corners and centroid.
	box.append([[(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (np.mean(px), np.mean(py))])

for b, centroid in box:
	b = np.uint16(np.around(b))
	phg, phd, pbd, pbg = b
	print(phg)
	if((pbd[0]-phg[0]>min_size) and (pbd[1]-phg[1]>min_size)): #Régler à la taille d'une motte
		cv2.rectangle(image_rs, (phg[0],phg[1]), (pbd[0],pbd[1]), (0,0,255), 2) 
		centroid = np.uint16(np.around(centroid))
		cv2.circle(image_rs,(centroid[0],centroid[1]),4,(0,0,255),-1) 



cv2.imshow('Resultat du traitement',image_rs)
cv2.waitKey(0)
cv2.destroyAllWindows()

