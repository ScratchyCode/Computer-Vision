import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # da scegliere tra {'0', '1', '2'}
import tensorflow as tf
from tensorflow.python.client import device_lib

print("Check presenza GPU:")
print(device_lib.list_local_devices())

print("\nNum GPU disponibili: ",len(tf.config.list_physical_devices('GPU')))

input("Premi INVIO...")
