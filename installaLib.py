import subprocess as sp
import sys

def installa(pacchetto):
    sp.check_call([sys.executable,"-m","pip","install",pacchetto])

installa("numpy")
installa("opencv-python")
installa("pytest-shutil")
installa("statistics")
installa("tensorflow")
installa("tensorflow-gpu")
installa("keras")
installa("Keras-Applications")
installa("Keras-Preprocessing")
#installa("matplotlib")
#installa("pandas")
