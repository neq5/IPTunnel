#!/usr/bin/env python3

from socketserver import ForkingTCPServer, StreamRequestHandler
import socket
import select
import time
import argparse

LOCAL_PORT = 20009
DESTINATION_IP = '127.0.0.1'
DESTINATION_PORT = 22

parser = argparse.ArgumentParser(description='IP Tunnel 0.3', epilog='neq5@o2.pl')

parser.add_argument('-l', '--local_port', metavar='local_port', dest='lp', type=int, default=LOCAL_PORT)
parser.add_argument('-i', '--ip', metavar='destination_ip', dest='ip', type=str, default=DESTINATION_IP)
parser.add_argument('-d', '--destination-port', metavar='destination_port', dest='dp', type=int, default=DESTINATION_PORT)

args = parser.parse_args()

class EchoHandler(StreamRequestHandler):
    def handle(self):
        ess = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ess.connect((args.ip, args.dp))

        self.request.settimeout(None)

        print('Connection request from', self.client_address)

        while True:
            x, _, _ = select.select([ess, self.request], [], [])
                   
            if ess in x:
                data = ess.recv(4096)
                if len(data) == 0:
                    break
                self.request.send(data)
            if self.request in x:
                msg = self.request.recv(4096)
                if len(msg) == 0:
                    break
                ess.send(msg)
            time.sleep(0)
           
        print('Connection ended with', self.client_address)


if __name__ == "__main__":
    serv = ForkingTCPServer(('', args.lp), EchoHandler)
    serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.serve_forever()
