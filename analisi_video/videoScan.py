# Coded by Pietro Squilla
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # da scegliere tra {'0', '1', '2'}
import cv2
import numpy as np
from keras.applications.nasnet import preprocess_input
from keras.applications.nasnet import decode_predictions
from keras.applications.nasnet import NASNetLarge

def informazioni():
    print("\n")
    print("INFORMAZIONI GENERALI:")
    print("Questo programma analizza i video in una directory alla ricerca di fauna.")
    print("È stato concepito per snellire la classificazione di una grande mole di dati video;")
    print("i file vengono rinominati con un 'RISCONTRO' se essi hanno ripreso degli animali,")
    print("se sono vuoti o riprendono altro non subiscono alterazioni.\n")
    
    print("Per fare ciò è stata implementata una rete neurale addestrata sul dataset 'imageNet',")
    print("un insieme di 14 mln di immagini suddivise in 1000 classi di oggetti e animali comuni.")
    print("La rete usata dimostra un'accuratezza in fase di validazione dei risultati del 96%.")
    print("I risultati sono frutto di calcolo numerico sui pixel ed hanno una valenza statistica.")
    print("Non sostituiscono l'analisi umana ma possono discriminare dove l'occhio non vede;")
    print("la differenza è che viene eseguita un'analisi quantitativa e non qualitativa.")
    print("In questa versione del programma si discrimina solo tra video vuoti e con fauna;")
    print("potenzialmente questa rete può classificare le singole specie animali, necessita però")
    print("di un training specifico sulla fauna locale che si vuole monitorare.")
    print("\n")
    print("FUNZIONAMENTO:")
    print("Il funzionamento è il seguente:")
    print("1) si inserisce il nome della cartella che ha SOLO file video (risoluzione 1920x1080);")
    print("2) si inserisce il numero di frame da NON far processare alla rete neurale;")
    print("3) si inserisce il valore percentuale della confidenza desiderata per il riscontro;")
    print("4) si inserisce il tipo di mosaicizzazione di ogni frame dei video.\n")

    print("Il primo settaggio è stato programmato perchè l'elaborazione di ogni frame impiega:")
    print("circa 350ms se si sfrutta solo la CPU (caso di computer senza scheda video dedicata);")
    print("circa 20 ms se si sfrutta la GPU di una scheda video dedicata.")
    print("Lo skip dei frame in questo caso consente di ridurre i tempi di elaborazione.")
    print("Inoltre il software è stato testato con la mosaicizzazione su frame 1920x1080.")
    print("Potenzialmente non ci sono problemi ad estendere l'uso su qualsiasi risoluzione,")
    print("ma all'attuale versione non è stata testata come funzionalità, inibendone quindi l'uso.\n")

    print("Il secondo punto è stato programmato perchè i riscontri avvengono su base probabilistica.")
    print("Una confidenza alta (>70%) consente di essere sicuri della fauna classificata,")
    print("ma può creare riscontri che risultano essere falsi negativi,")
    print("cioè tenderà ad escludere la fauna che ha una percentuale bassa di riscontro")
    print("come per esempio per i video sgranati, notturni o che presentano fauna defilata.")
    print("Una confidenza bassa (<50%) porterà dei riscontri che risultano essere falsi positivi,")
    print("cioè tenderà a classificare i video vuoti come se riprendessero della fauna.")
    print("Questo perchè la rete neurale è affetta (come gli umani) al noto effetto per cui")
    print("'l'occhio vede ciò che vuole vedere', a causa degli strati convoluzionali della ANN.\n")

    print("Il terzo settaggio è stato programmato per dare la possibilità all'utente")
    print("di decidere che mosaicizzazione creare di ogni frame, in base all'inquadratura del video.")
    print("Creare un mosaico di crop per ogni frame è necessario ed utile ai nostri fini perchè:")
    print("    1) le reti neurali hanno ingressi limitati rispetto al numero di pixel da analizzare;")
    print("    2) si limita la quantità di oggetti che possono interferire nella classificazione;")
    print("    3) si limita la quantità di rumore statistico che non appartiene ai pattern ricercati;")
    print("I limiti alla profondità dell'analisi sono arbitrari;")
    print("dipendendo direttamente dalle dimensioni degli animali e dalla loro lontananza,")
    print("ma aumentando il numero di riquadri di crop aumenta anche il tempo di elaborazione.")
    print("Leggere i settaggi consigliati a proposito.")
    print("\n")
    print("SETTAGGI:")
    print("skip = 1  -> si analizzano tutti i frame dei video;")
    print("skip = 10 -> si analizza 1 frame ogni 10 (e cosi via);")
    print("si consideri che un video ha un FPS = 30 (quindi 30 frame sono 1s di video).\n")

    print("Un'analisi profonda, che riduce gli errori di classificazione, ha:")
    print("    skip = 1")
    print("    confidenza = 50.0")
    print("    riquadri = 18")
    #print("\n")
    print("Si consiglia di usare sempre questi settaggi per i monitoraggi faunistici,")
    print("perchè è preferibile controllare un video vuoto in più al 'perdere' i dati.")
    print("\n")
    print("NB: Eseguire il programma nella stessa directory della cartella con i video,")
    print("altrimenti fornire il percorso assoluto alla cartella che contiene i dati.")
    print("Formato video supportati: .avi, .mov, .mp4\n")
    
    return

listafauna = [
#_pesci
'tench,Tinca_tinca',
'goldfish,Carassius_auratus',
'great_white_shark,white_shark,man-eater,man-eating_shark,Carcharodon_carcharias',
'tiger_shark,Galeocerdo_cuvieri',
'hammerhead,hammerhead_shark',
'electric_ray,crampfish,numbfish,torpedo',
'stingray',

#_uccelli
'cock',
'hen',
'brambling,Fringilla_montifringilla',
'goldfinch,Carduelis_carduelis',
'house_finch,linnet,Carpodacus_mexicanus',
'junco,snowbird',
'indigo_bunting,indigo_finch,indigo_bird,Passerina_cyanea',
'robin,American_robin,Turdus_migratorius',
'bulbul',
'jay',
'magpie',
'chickadee',
'water_ouzel,dipper',
'bald_eagle,American_eagle,Haliaeetus_leucocephalus',
'vulture',
'great_grey_owl,great_gray_owl,Strix_nebulosa',

#_anfibi
'European_fire_salamander,Salamandra_salamandra',
'common_newt,Triturus_vulgaris',
'eft',
'spotted_salamander,Ambystoma_maculatum',
'axolotl,mud_puppy,Ambystoma_mexicanum',
'bullfrog,Rana_catesbeiana',
'tree_frog,tree-frog',
'tailed_frog,bell_toad,ribbed_toad,tailed_toad,Ascaphus_trui',

#_rettili
'banded_gecko',
'American_chameleon,anole,Anolis_carolinensis',
'whiptail,whiptail_lizard',
'agama',
'frilled_lizard,Chlamydosaurus_kingi',
'alligator_lizard',
'Gila_monster,Heloderma_suspectum',
'green_lizard,Lacerta_viridis',
'African_chameleon,Chamaeleo_chamaeleon',
'Komodo_dragon,Komodo_lizard,dragon_lizard,giant_lizard,Varanus_komodoensis',
'thunder_snake,worm_snake,Carphophis_amoenus',
'ringneck_snake,ring-necked_snake,ring_snake',
'hognose_snake,puff_adder,sand_viper',
'green_snake,grass_snake',
'king_snake,kingsnake',
'garter_snake,grass_snake',
'water_snake',
'vine_snake',
'night_snake,Hypsiglena_torquata',
'boa_constrictor,Constrictor_constrictor',
'rock_python,rock_snake,Python_sebae',
'Indian_cobra,Naja_naja',
'green_mamba',
'sea_snake',
'horned_viper,cerastes,sand_viper,horned_asp,Cerastes_cornutus',
'diamondback,diamondback_rattlesnake,Crotalus_adamanteus',
'sidewinder,horned_rattlesnake,Crotalus_cerastes',

#_altri
'black_grouse',
'ptarmigan',
'ruffed_grouse,partridge,Bonasa_umbellus',
'prairie_chicken,prairie_grouse,prairie_fowl',
'peacock',
'quail',
'partridge',
'African_grey,African_gray,Psittacus_erithacus',
'macaw',
'sulphur-crested_cockatoo,Kakatoe_galerita,Cacatua_galerita',
'lorikeet',
'coucal',
'bee_eater',
'hornbill',
'hummingbird',
'jacamar',
'toucan',
'red-breasted_merganser,Mergus_serrator',
'goose',
'black_swan,Cygnus_atratus',
'echidna,spiny_anteater,anteater',
'platypus,duckbill,duckbilled_platypus,duck-billed_platypus,Ornithorhynchus_anatinus',
'wallaby,brush_kangaroo',
'koala,koala_bear,kangaroo_bear,native_bear,Phascolarctos_cinereus',
'wombat',
'white_stork,Ciconia_ciconia',
'black_stork,Ciconia_nigra',
'spoonbill',
'flamingo',
'little_blue_heron,Egretta_caerulea',
'American_egret,great_white_heron,Egretta_albus',
'bittern',
'crane',
'limpkin,Aramus_pictus',
'European_gallinule,Porphyrio_porphyrio',
'American_coot,marsh_hen,mud_hen,water_hen,Fulica_americana',
'bustard',
'ruddy_turnstone,Arenaria_interpres',
'redshank,Tringa_totanus',
'dowitcher',
'oystercatcher,oyster_catcher',
'pelican',
'albatross,mollymawk',

#_cani
'Chihuahua',
'Japanese_spaniel',
'Maltese_dog,Maltese_terrier,Maltese',
'Pekinese,Pekingese,Peke',
'Shih-Tzu',
'Blenheim_spaniel',
'papillon',
'toy_terrier',
'Rhodesian_ridgeback',
'Afghan_hound,Afghan',
'basset,basset_hound',
'beagle',
'bloodhound,sleuthhound',
'bluetick',
'black-and-tan_coonhound',
'Walker_hound,Walker_foxhound',
'English_foxhound',
'redbone',
'borzoi,Russian_wolfhound',
'Irish_wolfhound',
'Italian_greyhound',
'whippet',
'Ibizan_hound,Ibizan_Podenco',
'Norwegian_elkhound,elkhound',
'otterhound,otter_hound',
'Saluki,gazelle_hound',
'Scottish_deerhound,deerhound',
'Weimaraner',
'Staffordshire_bullterrier,Staffordshire_bull_terrier',
'American_Staffordshire_terrier,Staffordshire_terrier,American_pit_bull_terrier,pit_bull_terrier',
'Bedlington_terrier',
'Border_terrier',
'Kerry_blue_terrier',
'Irish_terrier',
'Norfolk_terrier',
'Norwich_terrier',
'Yorkshire_terrier',
'wire-haired_fox_terrier',
'Lakeland_terrier',
'Sealyham_terrier,Sealyham',
'Airedale,Airedale_terrier',
'cairn,cairn_terrier',
'Australian_terrier',
'Dandie_Dinmont,Dandie_Dinmont_terrier',
'Boston_bull,Boston_terrier',
'miniature_schnauzer',
'giant_schnauzer',
'standard_schnauzer',
'Scotch_terrier,Scottish_terrier,Scottie',
'Tibetan_terrier,chrysanthemum_dog',
'silky_terrier,Sydney_silky',
'soft-coated_wheaten_terrier',
'West_Highland_white_terrier',
'Lhasa,Lhasa_apso',
'flat-coated_retriever',
'curly-coated_retriever',
'golden_retriever',
'Labrador_retriever',
'Chesapeake_Bay_retriever',
'German_short-haired_pointer',
'vizsla,Hungarian_pointer',
'English_setter',
'Irish_setter,red_setter',
'Gordon_setter',
'Brittany_spaniel',
'clumber,clumber_spaniel',
'English_springer,English_springer_spaniel',
'Welsh_springer_spaniel',
'cocker_spaniel,English_cocker_spaniel,cocker',
'Sussex_spaniel',
'Irish_water_spaniel',
'kuvasz',
'schipperke',
'groenendael',
'malinois',
'briard',
'kelpie',
'komondor',
'Old_English_sheepdog,bobtail',
'Shetland_sheepdog,Shetland_sheep_dog,Shetland',
'collie',
'Border_collie',
'Bouvier_des_Flandres,Bouviers_des_Flandres',
'Rottweiler',
'German_shepherd,German_shepherd_dog,German_police_dog,alsatian',
'Doberman,Doberman_pinscher',
'miniature_pinscher',
'Greater_Swiss_Mountain_dog',
'Bernese_mountain_dog',
'Appenzeller',
'EntleBucher',
'boxer',
'bull_mastiff',
'Tibetan_mastiff',
'French_bulldog',
'Great_Dane',
'Saint_Bernard,St_Bernard',
'Eskimo_dog,husky',
'malamute,malemute,Alaskan_malamute',
'Siberian_husky',
'dalmatian,coach_dog,carriage_dog',
'affenpinscher,monkey_pinscher,monkey_dog',
'basenji',
'pug,pug-dog',
'Leonberg',
'Newfoundland,Newfoundland_dog',
'Great_Pyrenees',
'Samoyed,Samoyede',
'Pomeranian',
'chow,chow_chow',
'keeshond',
'Brabancon_griffon',
'Pembroke,Pembroke_Welsh_corgi',
'Cardigan,Cardigan_Welsh_corgi',
'toy_poodle',
'miniature_poodle',
'standard_poodle',
'Mexican_hairless',

#_selvatici
'timber_wolf,grey_wolf,gray_wolf,Canis_lupus',
'white_wolf,Arctic_wolf,Canis_lupus_tundrarum',
'red_wolf,maned_wolf,Canis_rufus,Canis_niger',
'coyote,prairie_wolf,brush_wolf,Canis_latrans',
'dingo,warrigal,warragal,Canis_dingo',
'dhole,Cuon_alpinus',
'African_hunting_dog,hyena_dog,Cape_hunting_dog,Lycaon_pictus',
'hyena,hyaena',
'red_fox,Vulpes_vulpes',
'kit_fox,Vulpes_macrotis',
'Arctic_fox,white_fox,Alopex_lagopus',
'grey_fox,gray_fox,Urocyon_cinereoargenteus',

#_felini
'tabby,tabby_cat',
'tiger_cat',
'Persian_cat',
'Siamese_cat,Siamese',
'Egyptian_cat',
'cougar,puma,catamount,mountain_lion,painter,panther,Felis_concolor',
'lynx,catamount',
'leopard,Panthera_pardus',
'snow_leopard,ounce,Panthera_uncia',
'jaguar,panther,Panthera_onca,Felis_onca',
'lion,king_of_beasts,Panthera_leo',
'tiger,Panthera_tigris',
'cheetah,chetah,Acinonyx_jubatus',

#_selvatici
'brown_bear,bruin,Ursus_arctos',
'American_black_bear,black_bear,Ursus_americanus,Euarctos_americanus',
'ice_bear,polar_bear,Ursus_Maritimus,Thalarctos_maritimus',
'sloth_bear,Melursus_ursinus,Ursus_ursinus',
'mongoose',
'meerkat,mierkat',
'wood_rabbit,cottontail,cottontail_rabbit',
'hare',
'Angora,Angora_rabbit',
'hamster',
'porcupine,hedgehog',
'fox_squirrel,eastern_fox_squirrel,Sciurus_niger',
'marmot',
'beaver',
'guinea_pig,Cavia_cobaya',
'sorrel',
'hog,pig,grunter,squealer,Sus_scrofa',
'wild_boar,boar,Sus_scrofa',
'warthog',
'ox',
'water_buffalo,water_ox,Asiatic_buffalo,Bubalus_bubalis',
'bison',
'ram,tup',
'bighorn,bighorn_sheep,cimarron,Rocky_Mountain_bighorn,Rocky_Mountain_sheep,Ovis_canadensis',
'ibex,Capra_ibex',
'hartebeest',
'impala,Aepyceros_melampus',
'gazelle',
'Arabian_camel,dromedary,Camelus_dromedarius',
'llama',
'weasel',
'mink',
'polecat,fitch,foulmart,foumart,Mustela_putorius',
'black-footed_ferret,ferret,Mustela_nigripes',
'otter',
'skunk,polecat,wood_pussy',
'badger',
'armadillo',
'three-toed_sloth,ai,Bradypus_tridactylus',
'orangutan,orang,orangutang,Pongo_pygmaeus',
'gorilla,Gorilla_gorilla',
'chimpanzee,chimp,Pan_troglodytes',
'gibbon,Hylobates_lar',
'siamang,Hylobates_syndactylus,Symphalangus_syndactylus',
'guenon,guenon_monkey',
'patas,hussar_monkey,Erythrocebus_patas',
'baboon',
'macaque',
'langur',
'colobus,colobus_monkey',
'proboscis_monkey,Nasalis_larvatus',
'marmoset',
'capuchin,ringtail,Cebus_capucinus',
'howler_monkey,howler',
'titi,titi_monkey',
'spider_monkey,Ateles_geoffroyi',
'squirrel_monkey,Saimiri_sciureus',
'Madagascar_cat,ring-tailed_lemur,Lemur_catta',
'indri,indris,Indri_indri,Indri_brevicaudatus',
'Indian_elephant,Elephas_maximus',
'African_elephant,Loxodonta_africana',
'lesser_panda,red_panda,panda,bear_cat,cat_bear,Ailurus_fulgens',
'giant_panda,panda,panda_bear,coon_bear,Ailuropoda_melanoleuca',
]

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

def analisiFrame(model,img,confidenza,mosaico,frameSize):
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
        for nomi in listafauna:
            if(animale in nomi):
                if(percentuale >= confidenza):
                    print(" *** Fauna in crop %d: %s (%.2f%%)" %(i+1,animale,percentuale),flush=True)
                    contatore += 1
                    break
    
    return contatore

##############
#    main    #
##############
if(__name__ == "__main__"):
    print("********************************************")
    print("*                                          *")
    print("*              SCANNER VIDEO               *")
    print("*  A RETE NEURALE CONVOLUZIONALE PROFONDA  *")
    print("*               NasNetLarge                *")
    print("*                                          *")
    print("*      Progetto Monitoraggi Faunisti       *")
    print("* Parco Naturale Regionale Monti Lucretili *")
    print("*             Anno 2021/2022               *")
    print("*                                          *")
    print("********************************************")
    
    menu = input("Premi 'c' per continuare, 'h' per maggiori info, 'x' per uscire: ")
    if(menu == 'c' or menu == 'C'):
        pass
    elif(menu == 'h' or menu == 'H'):
        informazioni()
    else:
        quit()
    
    # dati generali
    dirname = input("Nome cartella video: ")
    
    skip = int(input("Inserisci il numero di frame da skippare: "))
    while(skip <= 0):
        print("Il valore dello skip deve essere maggiore di 0!")
        skip = int(input("Inserisci il numero di frame da skippare: "))
    
    confidenza = float(input("Inserisci la confidenza percentuale: "))
    while(confidenza <= 0.0 or confidenza >=100.0):
        print("La confidenza deve essere compresa tra 0% e 100%")
        confidenza = float(input("Inserisci la confidenza percentuale: "))
    
    # matrice mosaico sui frame
    print("Scegli la tipologia di mosaico da applicare:")
    print("     8 riquadri -> (primo piano)")
    print("    18 riquadri -> (animali lontani)")
    print("    32 riquadri -> (animali piccoli)")
    #print("4) 144 crop -> (sperimentale)")
    
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
        
    
    # lista dei video nella cartella
    listavideo = os.listdir(dirname + '/')
    listavideo.sort()
    numerovideo = len(listavideo)
    
    # cambio la dir operativa per consentire di trovare i file successivamente
    os.chdir(dirname + '/')
    
    # carico la rete neurale in memoria
    print("Caricamento rete neurale...\n",flush=True)
    ann = NASNetLarge(weights='imagenet')
    
    # analizzo i video uno dopo l'altro
    for i in range(numerovideo):
        
        # escludo eventuali directory dalla lista dei video presenti
        if(os.path.exists(listavideo[i]) and os.path.isdir(listavideo[i])):
            print("*** Escludo '%s': è una directory.\n" %(listavideo[i]))
            continue
        
        # escludo qualsisi altro file che non sia un video
        ext = os.path.splitext(listavideo[i])[1][1:]
        if(ext != "avi" and ext != "AVI" and ext != "mov" and ext != "MOV" and ext != "mp4" and ext != "MP4"):
            print("*** Escludo '%s': non è un video.\n" %(listavideo[i]))
            continue
        
        print("Analisi video '%s'..." %(listavideo[i]),flush=True)
        
        # apro il video e controllo che abbia una risoluzione di 1920x1080 per il mosaico successivo
        vidcap = cv2.VideoCapture(listavideo[i])
        if(vidcap.isOpened()):
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            numframe = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            frameSize = (width,height)
            
            if(width != 1920 or height != 1080):
                print("\n*** Errore! ***")
                print("Risoluzione video richiesta: 1920x1080")
                print("Il video aperto invece è: %dx%d\n" %(width,height))
                #print("Uscita...")
                #quit()
                continue
        else:
            print("*** Errore nell'apertura dei file! ***\n")
            continue
        
        # inizializzo l'elaborazione
        success = True
        count = 0
        
        # elaborazione
        try:
            while success:
                count += 1
                # non viene usato un for con cv2.CAP_PROP_FRAME_COUNT per controllare gli errori sui video
                success,frame = vidcap.read()
                
                if(success != True):
                    break
                
                if(count % skip == 0):
                    print(" Frame %d..." %count)
                    
                    fauna = analisiFrame(ann,frame,confidenza,mosaico,frameSize)
                    
                    if(fauna != 0):
                        vidcap.release()
                        print("Salvataggio...\n",flush=True)
                        # rinomino il video con le informazioni estratte
                        nomeVecchio = listavideo[i]
                        os.rename(nomeVecchio,"RISCONTRO" + ' ' + nomeVecchio)
                        #os.replace(nomeVecchio,"RISCONTRO" + ' ' + nomeVecchio)
                        break
                    else:
                        continue
                else:
                    continue
        
        except:
            break
    
    input("Premi INVIO per continuare...")
    quit()

