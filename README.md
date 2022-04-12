# Descrizione
Software basati su metodi di intelligenza artificiale per i monitoraggi faunistici della fauna selvatica, sviluppati per il Parco Regionale dei Monti Lucretili.

# Installazione e setup:
Per installare tutto il necessario:
1) assicurarsi di avere una connessione internet
2) installare l'interprete python (versione 3.10);
3) conclusa l'installazione, eseguire lo script 'installaLib.py' per installare tutte le librerie e moduli necessari;


# Contenuto:
Il software utile è:

1) frame.py       salva i singoli frame di un video passato in input dentro alla cartella 'frame'
                  per poter ispezionare un video fotoframma dopo fotogramma (nel caso di riprese veloci);

2) timing.py:     per fototrappole, rinomina i file video di una cartella con data e ora dell'ultima modifica,
                  chiedendo inoltre informazioni sulla fototrappola da cui derivano i video per una più semplice gestione dei database;

3) extSort.py:    legge il contenuto di una directory ricorsivamente e separa i file al suo interno
                  per estensione, salvandoli in sottocartelle rinominate con l'estensione dei file;

4) videoScan.py:  analizza i video di una directory con una rete neurale filtrando tutto ciò che non è fauna;
                  i formati video supportati sono: .avi, .mov, .mp4;

5) fotoScan.py:   analizza una foto con la stessa rete neurale di 'videoScan.py' applicando gli stessi mosaici;
                  restituisce in output i label più probabili per ogni crop del mosaico su tutte le uscite della rete;


# Uso:
Per usare i software sarà sufficiente copiarli a fianco delle directory che contengono i dati,
cioè nella stessa working directory, seguendo poi le istruzioni dei singoli programmi.
