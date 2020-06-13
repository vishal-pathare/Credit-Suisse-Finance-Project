import quickfix as fix
import quickfix44 as fix44
import sys, time
import sqlite3
import argparse



'''
Quickfix imports onCreate(), onLogon(), onLogout(),toAdmin(), fromAdmin(), toApp() and fromApp()
toApp() is a callback for application messages that are being sent to a counterparty.
fromApp() receives application level request.

Quickfix triggers fromApp() when it receives messages on the Socket. So we will receive a snapshot every time
matching engine sends it which will be received within fromApp(). No of Entries can be found with noMDEntries()
Each group represents one order, we add order to the orderList and keep updating database

A configuration file needs to be set up for connection between counterparties(Matching Engine & RTMD in this case)
we need to configure username, sender-receiver IP addresses & ports
'''
class Application(fix.Application):


    def onCreate(self, sessionID):
        self.sessionID = sessionID
        print('Session Created')
        return

    def returnSessionID(self, sessionID):
        return (self.sessionID)

    def onLogon(self, sessionID):
        print('Logon called')
        return

    def onLogout(self, sessionID):
        print('Logout called')
        return

    def toAdmin(self, message, sessionID):
        print('toAdmin: ', end = '')
        #print(str(message))
        return

    def fromAdmin(self, message, sessionID):
        print('::::fromAdmin:::: ', end='')
        #print(str(message))
        return

    def toApp(self, message, sessionID):
        print('::::toApp called::::')
        print('Message to client: ', end = '')
        print(str(message))
        return

    def fromApp(self, message, sessionID):
        print('::::fromApp called::::')
        conn = sqlite3.connect('rtmd.db')
        c = conn.cursor()
        c.execute('''
                create table if not exists ask(
                orderId text primary key unique,
                price int,
                quantity int,
                company text,
	            exchange text,
	            time text
            );
            '''
        )

        c.execute('''
            create table if not exists bid(
                orderId text primary key unique,
                price int,
                quantity int,
                company text,
                exchange text,
                time text
            );
            '''
        )

        class order:
            def __init__(self, id, price, type, qty, company, exchg, time):
                self.id = id
                self.price = price
                self.type = type
                self.qty = qty
                self.company = company
                self.exchg = exchg
                self.time = time

        group = fix44.MarketDataSnapshotFullRefresh().NoMDEntries()

        #orderList = [] #to store each order entry sent in an object of <class 'order'> in order to send to UI team

        orderID = fix.OrderID() #represents orderID
        MDEntryType = fix.MDEntryType()
        NumberOfOrders = fix.NumberOfOrders() #represents quantity
        MDEntryPx = fix.MDEntryPx() #represents the price
        MDEntrySeller = fix.MDEntrySeller() #represents company
        MDMkt = fix.MDMkt() #represents exchange
        #MDEntrytime = fix.MDEntryTime() #represents time

        noMDEntries = fix.NoMDEntries() #get the total number of groups in snapshot
        message.getField(noMDEntries)
        tag, numberOfGroups = str(noMDEntries).split('=')
        numberOfGroups = numberOfGroups[:-1]
        numberOfGroups = int(numberOfGroups)

        for i in range(1, numberOfGroups+1):
            message.getGroup(i, group)
            tag, type = str(group.getField(MDEntryType)).split('=') #storing order type in var 'type'
            type = type[:-1] #to ignore the last special character

            tag, price = str(group.getField(MDEntryPx)).split('=')
            price = price[:-1]

            tag, id = str(group.getField(orderID)).split('=')
            id = id[:-1]

            tag, qty = str(group.getField(NumberOfOrders)).split('=')
            qty = qty[:-1]

            tag, company = str(group.getField(MDEntrySeller)).split('=')
            company = company[:-1]

            tag, exchg = str(group.getField(MDMkt)).split('=')
            exchg = exchg[:-1]

            # tag, time = str(group.getField(MDEntrytime)).split('=')
            # time = time[:-1]
            time = '2020-06-12 15:02:30'

            orderc = order(id, price, type, qty, company, exchg, time)
            print(orderc.id, orderc.price, orderc.qty, orderc.company, orderc.exchg,  end = ' ')
            print(' :: will be put in table ' + str(orderc.type))
            params = (orderc.id, orderc.price, orderc.qty, orderc.company, orderc.exchg, orderc.time)
            if(orderc.type == '0'):
                c.execute("insert or ignore into ask values(?, ?, ?, ?, ?, ?)", params)
            elif(orderc.type == '1'):
                c.execute("insert or ignore into bid values(?, ?, ?, ?, ?, ?)", params)

        print('ask table has: ')
        for row in c.execute("select * from ask"):
            print(row)
        print()
        print('bid table has: ')
        for row in c.execute("select * from bid"):
            print(row)

        conn.commit()
        conn.close()

        return

def main(config_file):
    try:
        settings = fix.SessionSettings(config_file)
        application = Application()
        storefactory = fix.FileStoreFactory(settings)
        logfactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        while True:
            time.sleep(0)
        initiator.stop()

    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()
    main(args.file_name)







# message = fix44.MarketDataSnapshotFullRefresh()
# group = fix44.MarketDataSnapshotFullRefresh().NoMDEntries()
#
# group.setField(fix.MDEntryType('0'))
# group.setField(fix.MDEntryPx(12.32))
# group.setField(fix.MDEntrySize(100))
# group.setField(fix.OrderID("ORDERID"))
# message.addGroup(group)
#
# group.setField(fix.MDEntryType('1'))
# group.setField(fix.MDEntryPx(12.32))
# group.setField(fix.MDEntrySize(100))
# group.setField(fix.OrderID("ORDERID"))
# message.addGroup(group)
#
#
#
# fix.MDEntryType() fix.MDEntryPx() fix.MDEntrySize() fix.OrderID();
#
# message.getGroup(1, group);
# a, b = str(group.getField(MDEntryType)).split('=');
# print(b[:-1])
# group.getField(MDEntryPx);
# group.getField(MDEntrySize);
# c, d = str(group.getField(orderID)).split('=');
# print(d[:-1])
# message.getGroup(2, group);
# group.getField(MDEntryType);
# group.getField(MDEntryPx);
# group.getField(MDEntrySize);
# group.getField(orderID);

'''
37: orderID
269: MDEntryType
346: NumberOfOrders
270	MDEntryPx

'''
