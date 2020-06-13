from collections import OrderedDict
from random import randint
import socket
import pickle
import threading
import rtdb

serverIP = "127.0.0.1"
serverPort = 9999
pathDb = "RTMD/rtmd.db"

def prep_test_data():
    test_data = [['20', '10'], ['19', '18'],
                 ['11', '11'], ['24', '10'],
                 ['1000', '10']]
    bid_data = OrderedDict()
    ask_data = OrderedDict()
    for i in range(5):
        bid_data[i] = " ".join(test_data[randint(0, 4)])
        ask_data[i] = " ".join(test_data[randint(0, 4)])

    return (bid_data, ask_data)


def get_data(name_company, name_exchange, num_transactions):
    '''
    The main function for getting the market data for
    the given name of company and exchange
    It takes in three arguments:
    The name of the company
    The name of the exchange
    The number of transactions you are interested in
    '''

    # Add your code here
    # rtdb.create_table(db)
    bid_data, ask_data = rtdb.retrieve(pathDb, name_company, name_exchange, num_transactions)
    return bid_data, ask_data

def send_market_data():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverIP, serverPort))
    server.listen(5)  # max backlog of connections

    def handle_client_connection(client_socket):

        data = client_socket.recv(1024)
        data = pickle.loads(data)
        data_to_send = get_data(data[0].decode(), data[1].decode(), data[2].decode())
        data_to_send = pickle.dumps(data_to_send)
        client_socket.send(data_to_send)
        client_socket.close()

    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(
            target=handle_client_connection, args=(client_sock,))
        client_handler.start()


if __name__ == '__main__':
    send_market_data()
