#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import quickfix44 as fix44
import quickfix as fix
from quickfix import Side_BUY
from quickfix import Side_SELL
import time
import logging

from datetime import datetime

# configured
__SOH__ = chr(1)

# Logger
logfix = logging.getLogger('FIX')


class Application(fix.Application):
    """FIX Application"""

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogon(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogout(self, sessionID): 
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)
        return
        
    def fromApp(self, message, sessionID):
        print ("The FIX message is : ", message)
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        self.onMessage(message, sessionID)
        return

   
    def onMessage(self, message, sessionID):
        """on Message"""
        pass

    def run(self):
        
        logon = fix44.Logon()

        #Keep sending a sample set of messages to server, where the second message

        while(1):
            
            message = fix.Message()
            header = message.getHeader()

            header.setField(fix.BeginString("FIX.4.4"))
            header.setField(fix.SenderCompID("COEPUSER"))
            header.setField(fix.TargetCompID("COEPEXCH"))
            header.setField(fix.MsgType("D"))
            message.setField(fix.ClOrdID("3"))
            message.setField(fix.Symbol("amzn"))
            message.setField(fix.Side(Side_BUY))
            message.setField(58, "Buy shares")
            message.setField(fix.Price(87))
            message.setField(fix.OrderQty(2))
            transact_time = datetime.utcnow() 
            message.setField(60, transact_time.strftime("%Y%m%d-22:29:00.000"))
            message.setField(fix.Account("EXECLINKS"))
            message.setField(40, "2")
            status = fix.Session.sendToTarget(message, self.sessionID)
            print("Status: ", status)
            print(message)

            time.sleep(5)

            message = fix.Message()
            header = message.getHeader()
            header.setField(fix.BeginString("FIX.4.4"))
            header.setField(fix.SenderCompID("COEPUSER"))
            header.setField(fix.TargetCompID("COEPEXCH"))
            header.setField(fix.MsgType("D"))
            message.setField(fix.ClOrdID("3"))
            message.setField(fix.Symbol("amzn"))
            message.setField(fix.Side(Side_SELL))
            message.setField(58, "Sell shares")
            message.setField(fix.Price(87))
            message.setField(fix.OrderQty(2))
            transact_time = datetime.utcnow() 
            message.setField(60, transact_time.strftime("%Y%m%d-22:29:00.000"))         
            message.setField(fix.Account("EXECLINKS"))
            message.setField(40, "2")
            status = fix.Session.sendToTarget(message, self.sessionID)
            print("Status: ", status)
            print(message)
            time.sleep(100)
