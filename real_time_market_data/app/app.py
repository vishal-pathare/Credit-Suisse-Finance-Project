from flask import Flask, render_template, request, session, redirect
import socket
import pickle

serverIP = "127.0.0.1"
serverPort = 9999
app = Flask(__name__)
app.secret_key = "SECRETKEY"


def parse_data(file):
    '''
    This is just a utility function to obtain the
    data in correct form
    It can be modified later if needed
    '''
    return list(map(lambda element: element.strip("\n"), file))


@app.route("/", methods=['GET', 'POST'])
def index():

    # Getting the list of companies and exchanges
    data = {}
    data['name_companies'] = parse_data(open("companies.txt").readlines())
    data['name_exchanges'] = parse_data(open("exchanges.txt").readlines())

    if request.method == 'POST':
        # Obtaining the input from the user
        company = request.form['company']
        exchange = request.form['exchange']
        num_transactions = request.form['num_transactions']

        # Making it global so that other page can make use of it
        session['company'] = company
        session['exchange'] = exchange
        session['num_transactions'] = num_transactions

        # Here, the hyperlink to the market data will be visible
        return render_template("layer.html", data=data, flag=1)
    else:
        # Here, the hyperlink to the market data won't be visible
        return render_template("layer.html", data=data, flag=0)


@app.route("/results")
def results():

    # Obtaining the information to sent to the Market-data team
    name_company = session.get('company', None)
    name_exchange = session.get('exchange', None)
    num_transactions = str(session.get('num_transactions', None))

    if name_company and name_exchange and num_transactions:
        # Encoding the data for safety
        name_company = str.encode(name_company)
        name_exchange = str.encode(name_exchange)
        num_transactions = str.encode(num_transactions)

        # Serialize the data to send
        data = (name_company, name_exchange, num_transactions)
        bytesToSend = pickle.dumps(data)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to a client
        client.connect((serverIP, serverPort))
        client.send(bytesToSend)
        response = client.recv(4096)

        # Deserialize the response
        response = pickle.loads(response)
        return render_template("result.html", recv_data=response, user_data=data)

    else:
        print(session)
        return redirect("/")


'''
@app.route("/results")
def results():

    # Obtaining the information to sent to the Market-data team
    name_company = session.get('company', None)
    name_exchange = session.get('exchange', None)
    num_transactions = str(session.get('num_transactions', 5))

    if name_company and name_exchange and num_transactions:
        # Encoding the data for safety
        name_company = str.encode(name_company)
        name_exchange = str.encode(name_exchange)
        num_transactions = str.encode(num_transactions)

        # Preparing the requirements for UDP Socket
        data = (name_company, name_exchange, num_transactions)
        bytesToSend = pickle.dumps(data)
        bufferSize = 4096

        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, (serverAddress, serverPort))

        print("aaaaaaaaaaa")

        market_data, _ = UDPClientSocket.recvfrom(bufferSize)
        print(market_data)

        print('bbbbbbbbbbbbbb')
        UDPClientSocket.close()
        return render_template("result.html", data=market_data)

    else:
        print(session)
        return redirect("/")
'''

if __name__ == "__main__":

    app.run(debug=True)
