# Coded by Pietro Squilla
import os
import cv2
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # da scegliere tra {'0', '1', '2'}
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.nasnet import preprocess_input
from keras.applications.nasnet import decode_predictions
from keras.applications.nasnet import NASNetLarge
from keras.models import load_model

def cropper(img,mosaico,frameSize):
    # esegue il mosaico di image dividendola in n*m crop, dove mosaico = (n,m)
    W,H = frameSize
    n,m = mosaico
    w,h = (int(W/n),int(H/m)) # dimensioni dei singoli crop
    
    # inizializzo la lista dei crop
    crops = []
    
    # esegue i crop
    for j in range(m):
        for i in range(n):
            crops.append(img[j*h:(j+1)*h,i*w:(i+1)*w])
    
    return crops



def analisiFrame(model,img,mosaico,frameSize):
    # valore (valutato poi booleanamente) da ritornare per conteggio riscontri
    contatore = 0
    
    # numero di crop
    numCrop = mosaico[0]*mosaico[1]
    
    # tupla che definisce il numero di righe e colonne per creare il mosaico
    listacrop = cropper(img,mosaico,frameSize)
    
    # rescaling dei crop al target_size della rete neurale -> NasNetLarge
    dim = (331,331)
    crops = []
    for i in range(numCrop):
        crops.append(cv2.resize(listacrop[i],dim,interpolation=cv2.INTER_CUBIC))
    
    # preprocessing
    for i in range(numCrop):
        crops[i] = preprocess_input(crops[i])
    
    # creo il batch dei crop per la parallelizzazione su gpu
    batch = np.array(crops)
    
    # running
    batchprob = model.predict(batch)
    
    # probabilità -> label
    batchlabel = decode_predictions(batchprob)
    
    # label più probabili di ogni crop
    for i in range(numCrop):
        label = batchlabel[i][0]
        animale = label[1]
        percentuale = label[2]*100
        print("Crop %d: %s (%.2f%%)" %(i+1,animale,percentuale),flush=True)


if(__name__ == "__main__"):
    filename = input("Inserisci il nome della foto: ")
    
    # matrice mosaico
    print("Scegli la tipologia di mosaico da applicare:")
    print("     8 riquadri -> (primo piano)")
    print("    18 riquadri -> (animali lontani)")
    print("    32 riquadri -> (animali piccoli)")
    print("   144 riquadri -> (sperimentale)")
    
    numMosaico = int(input("Numero riquadri: "))
    if(numMosaico == 8):
        mosaico = (4,2)
    elif(numMosaico == 18):
        mosaico = (6,3)
    elif(numMosaico == 32):
        mosaico = (8,4)
    elif(numMosaico == 144):
        mosaico = (16,9)
    else:
        print("\n*** Errore! ***")
        print("Numero di riquadri non supportata.")
        print("Uscita...")
        quit()
    
    try:
        image = cv2.imread(filename)
        height,width = image.shape[:2]
        frameSize = (width,height)
    except:
        print("Errore nel caricamento dell'immagine.")
        quit()
    
    # carico la cnn
    print("Caricamento rete neurale...")
    model = NASNetLarge(weights='imagenet')
    
    # predict su tutte le classi in output
    print("Running...")
    
    analisiFrame(model,image,mosaico,frameSize)

