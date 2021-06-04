import socket
import threading
import pickle

# Some global variables
BUFF_SIZE = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

# binding the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# Player data

class Player:
	def __init__(self, x, y):
		self.pos = (x, y)

players = [Player(100, 100), Player(200, 200)]
player_cnt = 0


def handler(conn, addr):
	# Client's ip address
	ip = addr[0]

	info = players[player_cnt]
	print(info)
	conn.send(pickle.dumps(info))

# Function to start server
def start():
	server.listen()
	print(f"Server is listening on {SERVER}")

	while True:
		conn, addr = server.accept()
		print(conn, addr)

		thread_1 = threading.Thread(target=handler, args=(conn, addr))
		thread_1.daemon = True
		thread_1.start()

		print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")

start()