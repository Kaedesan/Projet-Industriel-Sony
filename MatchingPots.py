import cv2
import numpy as np

lower_green = np.array([0,0, 42])  # valeur de vert supérieure
upper_green = np.array([90,164,198]) # valeur de vert inférieure


image = cv2.imread('alexandra14.jpg') # lecture de l'image

height, width, channels = image.shape # on récupère les dimensions de l'image

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # conversion de l'image en HSV

mask = cv2.inRange(img_hsv, lower_green, upper_green) # On créé un masque qui fixe les pixels qui ne nous intéresse pas en noir

res = cv2.bitwise_and(image,image, mask= mask) # On applique le masqu
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

# On utilise la détestion de Hough pour plus de précision
circles = cv2.HoughCircles(closing,cv2.HOUGH_GRADIENT,1,20,param1=60,param2=7,minRadius=15,maxRadius=18)
circles = np.uint16(np.around(circles))

nb_pots = 0;

for i in circles[0,:]:
		#draw the outer circle
		cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
		#draw the center of the circle
		cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
		#ajout de pots
		nb_pots = nb_pots+1

print(nb_pots)

cv2.waitKey(0)
