#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2
import os,sys, os.path
import numpy as np
import math

#filtro baixo
image_lower_hsv1 = np.array([76,54,78])
image_upper_hsv1 = np.array([96,255,255])
#filtro alto
image_lower_hsv2 = np.array([0,93,68])
image_upper_hsv2 = np.array([10,255,255])



def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada"""
    img = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask 

def mascara_or(mask1, mask2):

    """ retorna a mascara or"""
    mask = cv2.bitwise_or(mask1, mask2)
    return mask

def mascara_and(mask1, mask2):
     """ retorna a mascara and"""
     mask = cv2.bitwise_and(mask1, mask2)
     
     return mask

def desenha_cruz(img, cX,cY, size, color):
     """ faz a cruz no ponto cx cy"""
     cv2.line(img,(cX - size,cY),(cX + size,cY),color,3)
     cv2.line(img,(cX,cY - size),(cX, cY + size),color,3)    

def escreve_texto(img, text, x, y, color):
     """ faz a cruz no ponto cx cy"""
 
     font = cv2.FONT_HERSHEY_SIMPLEX
     origem = (x-33,y-30)
     cv2.putText(img, str(text), origem, font,0.4,color,1,cv2.LINE_AA)



def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """  
    mask_hsv1 = filtro_de_cor(img, image_lower_hsv1, image_upper_hsv1)
    mask_hsv2 = filtro_de_cor(img, image_lower_hsv2, image_upper_hsv2)
    
    mask_hsv = mascara_or(mask_hsv1, mask_hsv2)
    
    contornos, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB) 
    contornos_img = mask_rgb.copy()
    
    primeiroMaior = None
    maior_area = 0
    segundoMaior = None
    segundoMaior_area = 0
    for c in contornos:
        area = cv2.contourArea(c)
        if area > maior_area:
            segundoMaior_area = maior_area
            maior_area = area
            segundoMaior = primeiroMaior
            primeiroMaior = c
        elif area > segundoMaior_area:
            segundoMaior_area = area
            segundoMaior = c
    
    primeiroM = cv2.moments(primeiroMaior)
    segundoM = cv2.moments(segundoMaior)

    # Verifica se existe alguma para calcular, se sim calcula e exibe no display
    if primeiroM["m00"] != 0 and segundoM["m00"] != 0:
        pX = int(primeiroM["m10"] / primeiroM["m00"])
        pY = int(primeiroM["m01"] / primeiroM["m00"])
        sX = int(segundoM["m10"] / segundoM["m00"])
        sY = int(segundoM["m01"] / segundoM["m00"])
        
        cv2.drawContours(contornos_img, [primeiroMaior], -1, [255, 0, 0], 3)
        cv2.drawContours(contornos_img, [segundoMaior], -1, [255, 0, 0], 3)
       
        #faz a cruz no centro de massa
        desenha_cruz(contornos_img, pX,pY, 20, (0,0,255))
        desenha_cruz(contornos_img, sX,sY, 20, (0,0,255))

        
        # Para escrever vamos definir uma fonte 
        textoPrimeiro = pX, pY
        textoSegundo = sX, sY
 
        escreve_texto(contornos_img, textoPrimeiro, pX, pY, (0,0,255)) 
        escreve_texto(contornos_img, textoSegundo, sX, sY, (0,0,255)) 

        cv2.line(contornos_img,(pX,pY),(sX,sY),(0,0,255),3)

        rad = math.atan2(pY-sY, pX-sY)
        graus = round(math.degrees(rad))

        escreve_texto(contornos_img, str(graus)+' graus', sX+60, sY+35, (0,0,255)) 
            
    else:
    # se não existe nada para segmentar
        # Para escrever vamos definir uma fonte 
        textoPrimeiro = 'nao tem nada'
        escreve_texto(contornos_img, textoPrimeiro, 80, 60, (0,0,255))
    


    return contornos_img

cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)

#vc = cv2.VideoCapture("video.mp4") # para ler um video mp4 

#configura o tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada



    cv2.imshow("original", frame)
    cv2.imshow("preview", img)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
