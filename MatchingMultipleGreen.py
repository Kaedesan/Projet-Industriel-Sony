import cv2
import numpy as np

lower_green = np.array([31,26,0])  # valeur de vert supérieure
upper_green = np.array([39,255,255]) # valeur de vert inférieure


image = cv2.imread('testMultiple.jpg') # lecture de l'image

height, width, channels = image.shape # on récupère les dimensions de l'image

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # conversion de l'image en HSV
(h, s, v) = cv2.split(img_hsv)

mask = cv2.inRange(img_hsv, lower_green, upper_green) # On créé un masque qui fixe les pixels qui ne nous intéresse pas en noir

res = cv2.bitwise_and(image,image, mask= mask) # On applique le masque
#cv2.imshow('Résultat masque',res) # Affichage de l'image après application du masque
(h, s, v) = cv2.split(res)

imgtemp = cv2.GaussianBlur(res,(5,5),0) 
res_median = cv2.medianBlur(imgtemp,5) # On applique un filtre médian
#cv2.imshow('Résultat lissage',res_median) # Affichage du résultat

img_bn = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # On récupère l'image initiale en noir et blanc

#On traces les contours de notre image où l'on a appliqué le masque
contours = cv2.Canny(res_median, 100, 2500, apertureSize=5)
#cv2.imshow('Resultat contours',contours)

# On binarise notre image en noir et blanc
for i in range(height):
	for j in range(width):
		if (v[i][j] == 0):
			img_bn[i][j]=0
		else :
			img_bn[i][j]=255
        
# On affiche les résultats
#cv2.imshow('Resultat binarisation',img_bn)


kernel = np.ones((5,5),np.uint8)
#erosion = cv2.erode(img_bn,kernel,iterations = 3)
#cv2.imshow('Resultat erosion',erosion)

#dilation = cv2.dilate(erosion,kernel,iterations = 6)
#cv2.imshow('Resultat dilatation',dilation)

closing = cv2.morphologyEx(img_bn, cv2.MORPH_CLOSE, kernel)
#cv2.imshow('Resultat closing',closing)

contours_bn = cv2.Canny(closing, 100, 2500, apertureSize=5) #On trace les contours
#cv2.imshow('Resultat contours à partir de image_bn',contours_bn)

#Calcul du centre par moyenne des points
cmptx =0
cmpty =0
cmptp =0
for i in range(height):
    for j in range(width):
        if (img_bn[i][j] != 0):
            cmptx = cmptx + j;
            cmpty = cmpty + i;
            cmptp = cmptp +1;


cmptx = cmptx // cmptp
cmpty = cmpty // cmptp
# On trace le cercle obtenu
cv2.circle(image,(cmptx,cmpty),2,(0,0,255),-1)
cv2.circle(image,(cmptx,cmpty),70,(0,0,255),2)

# On utilise la détestion de Hough pour plus de précision
circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,1,20,param1=60,param2=15,minRadius=0,maxRadius=100)
circles = np.uint16(np.around(circles))

nb_pots = 0;

for i in circles[0,:]:
	#if i[2] > 10: # 70 à remplacer par la taille d'un pot en pixel quand la caméra sera calibrée
		#draw the outer circle
		cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
		#draw the center of the circle
		cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
		nb_pots = nb_pots+1

cv2.imshow('Resultat du traitement',image)
print(nb_pots)

cv2.waitKey(0)
cv2.destroyAllWindows()
