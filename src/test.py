import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH)

from Network import Network


SERVER = "192.168.100.202"
PORT = 5050


client = Network(SERVER, PORT)
a = client.connect()
print(a)
