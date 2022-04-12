# Coded by Pietro Squilla
import os
import cv2

# nome file video
nome_file = input("Inserisci nome file dati: ")

vidcap = cv2.VideoCapture(nome_file)

count = 1
success = True

#os.mkdir("frame" + '_' + nome_file)
#os.chdir("frame" + '_' + nome_file)
os.mkdir("frame")
os.chdir("frame")

try:
    while success:
        success,image = vidcap.read()
        cv2.imwrite("frame%d.jpg" %count,image)    # salva il frame in jpg
        print("frame%d.jpg" %count,flush=True)
        count += 1
    quit()
except:
    quit()

