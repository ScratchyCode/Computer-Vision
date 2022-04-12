# Coded by Pietro Squilla
import os
import shutil
# Divide i file di una cartella in sottocartelle organizzate per estensione dei file
print("********************************************")
print("*                                          *")
print("*    RIPARTIZIONE FILE PER ESTENSIONE      *")
print("*                                          *")
print("*      Progetto Monitoraggi Faunisti       *")
print("* Parco Naturale Regionale Monti Lucretili *")
print("*             Anno 2021/2022               *")
print("*                                          *")
print("********************************************")

dirName = input("Nome cartella dati: ")

li = os.listdir(dirName)

for i in li:
    fileName, extension = os.path.splitext(i)
    
    extension = extension[1:]
    
    if extension == "":
        continue
    
    if os.path.exists(dirName + '/' + extension):
        shutil.move(dirName + '/' + i, dirName + '/' + extension + '/' + i)
    
    else:
        os.makedirs(dirName + '/' + extension)
        shutil.move(dirName + '/' + i, dirName + '/' + extension + '/' + i)

print("Fine.")
