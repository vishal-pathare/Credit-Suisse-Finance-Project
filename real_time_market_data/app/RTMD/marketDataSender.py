import quickfix as fix
import quickfix44 as fix44
import sys, time








class Application(fix.Application):

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        print('Session Created')
        return

    def onLogon(self, sessionID):
        print('Logon called')
        return

    def onLogout(self, sessionID):
        print('Logout called')
        return

    def toAdmin(self, message, sessionID):
        return

    def fromAdmin(self, message, sessionID):
        print('fromAdmin: ', end='')
        #print(str(message))
        return

    def toApp(self, message, sessionID):
        print('toApp called')
        print('Message to client: ', end = '')
        print('toAdmin: ', end='')
        print(str(message))
        return

    def run(self):

        message = fix44.MarketDataSnapshotFullRefresh()
        group = fix44.MarketDataSnapshotFullRefresh().NoMDEntries()


        group.setField(fix.MDEntryType('0'))
        group.setField(fix.MDEntryPx(12.32))
        group.setField(fix.MDEntrySize(100))
        group.setField(fix.OrderID("ORDERID"))
        group.setField(fix.NumberOfOrders(1000))
        group.setField(fix.MDEntrySeller('RIL'))
        group.setField(fix.MDMkt('BSE'))
        #group.setField(fix.MDEntryTime(20200723))
        message.addGroup(group)

        group.setField(fix.MDEntryType('0'))
        group.setField(fix.MDEntryPx(12.32))
        group.setField(fix.MDEntrySize(100))
        group.setField(fix.OrderID("ORDERID"))
        group.setField(fix.NumberOfOrders(1000))
        group.setField(fix.MDEntrySeller('RIL'))
        group.setField(fix.MDMkt('BSE'))
        # group.setField(fix.MDEntryTime(20200723))
        message.addGroup(group)

        group.setField(fix.MDEntryType('1'))
        group.setField(fix.MDEntryPx(12.34))
        group.setField(fix.MDEntrySize(104))
        group.setField(fix.OrderID("ORDERID2"))
        group.setField(fix.NumberOfOrders(9087))
        group.setField(fix.MDEntrySeller('BHEL'))
        group.setField(fix.MDMkt('NSE'))
       # group.setField(fix.MDEntryTime(20200429))
        message.addGroup(group)

        group.setField(fix.MDEntryType('1'))
        group.setField(fix.MDEntryPx(12.34))
        group.setField(fix.MDEntrySize(104))
        group.setField(fix.OrderID("ORDERID2"))
        group.setField(fix.NumberOfOrders(9087))
        group.setField(fix.MDEntrySeller('BHEL'))
        group.setField(fix.MDMkt('NSE'))
        # group.setField(fix.MDEntryTime(20200429))
        message.addGroup(group)

        group.setField(fix.MDEntryType('0'))
        group.setField(fix.MDEntryPx(18.92))
        group.setField(fix.MDEntrySize(2000))
        group.setField(fix.OrderID("ORDERID3"))
        group.setField(fix.NumberOfOrders(10050))
        group.setField(fix.MDEntrySeller('TCS'))
        group.setField(fix.MDMkt('BSE'))
        # group.setField(fix.MDEntryTime(20200723))
        message.addGroup(group)

        group.setField(fix.MDEntryType('0'))
        group.setField(fix.MDEntryPx(200.32))
        group.setField(fix.MDEntrySize(1006))
        group.setField(fix.OrderID("ORDERID4"))
        group.setField(fix.NumberOfOrders(1000))
        group.setField(fix.MDEntrySeller('Credit Suisse'))
        group.setField(fix.MDMkt('BSE'))
        # group.setField(fix.MDEntryTime(20200723))
        message.addGroup(group)

        group.setField(fix.MDEntryType('0'))
        group.setField(fix.MDEntryPx(1000))
        group.setField(fix.MDEntrySize(100))
        group.setField(fix.OrderID("ORDERID6"))
        group.setField(fix.NumberOfOrders(1000))
        group.setField(fix.MDEntrySeller('Aramco'))
        group.setField(fix.MDMkt('BSE'))
        # group.setField(fix.MDEntryTime(20200723))
        message.addGroup(group)

        group.setField(fix.MDEntryType('1'))
        group.setField(fix.MDEntryPx(12.67))
        group.setField(fix.MDEntrySize(1045))
        group.setField(fix.OrderID("ORDERID7"))
        group.setField(fix.NumberOfOrders(8960))
        group.setField(fix.MDEntrySeller('Zomato'))
        group.setField(fix.MDMkt('NSE'))
        # group.setField(fix.MDEntryTime(20200429))
        message.addGroup(group)

        group.setField(fix.MDEntryType('1'))
        group.setField(fix.MDEntryPx(129))
        group.setField(fix.MDEntrySize(10894))
        group.setField(fix.OrderID("ORDERID8"))
        group.setField(fix.NumberOfOrders(9076))
        group.setField(fix.MDEntrySeller('Gilbarco'))
        group.setField(fix.MDMkt('NSE'))
        # group.setField(fix.MDEntryTime(20200429))
        message.addGroup(group)

        group.setField(fix.MDEntryType('1'))
        group.setField(fix.MDEntryPx(198))
        group.setField(fix.MDEntrySize(1034))
        group.setField(fix.OrderID("ORDERID9"))
        group.setField(fix.NumberOfOrders(9087))
        group.setField(fix.MDEntrySeller('Huwawei'))
        group.setField(fix.MDMkt('NSE'))
        # group.setField(fix.MDEntryTime(20200429))
        message.addGroup(group)



        fix.Session_sendToTarget(message, self.sessionID)
        return

    def fromApp(self, message, sessionID):
        return



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Incorrect number of arguments. Please run again')
        sys.exit(1)
    fileName = sys.argv[1]

    try:
        settings = fix.SessionSettings(fileName)
        application = Application()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        acceptor = fix.SocketAcceptor(application, storeFactory, settings, logFactory)
        acceptor.start()
        application.run()
        while True:
            time.sleep(0)
        acceptor.stop()
    except(fix.ConfigError) as  e:
        print(e)




'''if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Incorrect number of arguments. Please run again')
        sys.exit(1)
    fileName = sys.argv[1]

    try:
        settings = fix.SessionSettings(fileName)
        application = Application()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        initiator = fix.SocketInitiator(application, storefactory, settings, logfactory)
        #initiator.start()
        while True:
            time.sleep(0)
        #initiator.stop()
    except(fix.ConfigError, fix.RuntimeError) as  e:
        print(e)
'''