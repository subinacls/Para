import os
import sys
import inspect
import threading
import socket
from SocketServer import TCPServer, BaseRequestHandler, ThreadingMixIn
from modules.security.validation.hardvalidation import db_handler as dbh
from modules.security.validation.datavalidator import initdecrypt as idc
from modules.security.validation.clienthandler import datarouter as dar
from modules.security.firewall.fw_controller import fw_actions as fwa
from modules.security.encryption.decryptwkey import *
from modules.security.encryption.encryptwkey import *
from config.client.defaultconfig import *
from modules.data.formats import *

def checkpath():
    project_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
    if project_folder not in sys.path:
        sys.path.insert(0, project_folder)

checkpath()

serverport = 6543

# Init the clientdb
try:
    dbh().open_clientdb()
except Exception as failedtoloadclientdb:
    print(failedtoloadclientdb)
    dbh().init_clientdb()

class ThreadedTCPRequestHandler(BaseRequestHandler): 
    def handle(self):
        try:
            self.data = self.request.recv(65535, socket.MSG_WAITALL)
            datarouter().offload(self.data)
        except Exception as tcpreqhandlerfail:
            print(tcpreqhandlerfail)

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass

class TcpServer(object):
    def __init__(self):
        self.serverport = serverport

    def start(self):
        TCPServer.allow_reuse_address = True
        socketserver = ThreadedTCPServer(('', int(self.serverport)), ThreadedTCPRequestHandler)
        socketserver_thread = threading.Thread(target=socketserver.serve_forever)
        socketserver_thread.setDaemon(False)
        socketserver_thread.start()
        fwa().init_fw(self.serverport)

def main():
    tserver = TcpServer()
    tserver.start()

if __name__ == "__main__":
    main()
