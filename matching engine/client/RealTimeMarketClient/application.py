#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import quickfix44 as fix44
import quickfix as fix
from quickfix import Side_BUY
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
        print ("SENDING DUMMY MESSAGE TO MATCHING ENGINE")
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)
        return

    def fromApp(self, message, sessionID):
        print ("The FIX messages received is : ", message)
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        self.onMessage(message, sessionID)
        return

   
    def onMessage(self, message, sessionID):
        """on Message"""
        pass

    def run(self):
        
        #logon
        logon = fix44.Logon()
        while(1):

            time.sleep(10)

