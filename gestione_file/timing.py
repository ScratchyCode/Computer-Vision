# Coded by Pietro Squilla
# per Windows
import os
import platform
import time

print("********************************************")
print("*                                          *")
print("*         TIMING VIDEO FOTOTRAPPOLE        *")
print("*                                          *")
print("*      Progetto Monitoraggi Faunisti       *")
print("* Parco Naturale Regionale Monti Lucretili *")
print("*             Anno 2021/2022               *")
print("*                                          *")
print("********************************************")

# funzione per estrapolare data e ora dell'ultima modifica del file
def datatime(nomefile):
    stat = os.stat(nomefile)
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime

# dati generali
dirname = input("Nome cartella dati: ")
luogo = input("Località: ")
fototrappola = input("Codice fototrappola: ")
solare = int(input("Inserisci '1' per ora solare, '0' per ora legale: "))
if(solare != 0 and solare != 1):
    print(" Solo i valori '0' ed '1' sono consentiti!\n Uscita.")
    quit()

# lista dei video nella cartella
listavideo = os.listdir(dirname + "/")
listavideo.sort()
numerovideo = len(listavideo)

# cambio la dir operativa per consentire di trovare i file alla funzione
os.chdir(dirname + '/')

# estrapolo le informazioni da ogni video
for i in range(numerovideo):
    # escludo eventuali directory dalla lista dei video presenti
    if(os.path.exists(listavideo[i]) and os.path.isdir(listavideo[i])):
        print("*** Escludo '%s': è una directory.\n" %(listavideo[i]))
        continue
    
    print("Video %d..." %(i+1))
    epoch = datatime(listavideo[i])
    tupla = time.localtime(epoch)
    aa = int(tupla[0])
    mm = int(tupla[1])
    gg = int(tupla[2])
    ora = int(tupla[3])
    minuti = int(tupla[4])
    secondi = int(tupla[5])
    ora = ora - solare
    
    # anni
    aastring = str(aa)
    
    # mesi
    if(mm < 10):
        mmstring = '0' + str(mm)
    else:
        mmstring = str(mm)
    
    # giorni
    if(gg < 10):
        ggstring = '0' + str(gg)
    else:
        ggstring = str(gg)
    
    # ora
    if(ora < 10):
        orastring = '0' + str(ora)
    else:
        orastring = str(ora)
    
    # minuti
    if(minuti < 10):
        minutistring = '0' + str(minuti)
    else:
        minutistring = str(minuti)
    
    # secondi
    if(secondi < 10):
        secondistring = '0' + str(secondi)
    else:
        secondistring = str(secondi)
    
    # rinomino il video con le informazioni estratte
    estensione = os.path.splitext(listavideo[i])[1][1:]
    os.rename(listavideo[i],"%s.%s" %(luogo + ' ' + fototrappola + ' ' + ggstring + '-' + mmstring + '-' + aastring + ' ' + orastring + '_' + minutistring + '_' + secondistring,estensione))
    
    i += 1

print("\nFine.")
input("Premi INVIO per continuare...")

