# encoding=utf8
import ConfigParser
import logging
import socket
import os
import json
import struct

# start listening
class master:
    sock = None
    def __init__(self):
        pass

    def dispatch(self,host,port,args):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        self.send_json(args)
        self.send_file(args.get('content'))
        self.send_file(args.get('style'))
        self.sock.close()


    def send_int(self,integer):
        packer = struct.Struct('I')
        packed = packer.pack(integer)
        self.sock.sendall(packed)

    def send_json(self,obj):
        packer =struct.Struct('I')
        jstr = json.dumps(obj)
        packed = packer.pack(len(jstr))
        self.sock.send(packed)
        self.sock.send(jstr)


    def send_file(self,filename,chunk_size=1024):
        f = open(filename, 'rb')
        f.seek(0,os.SEEK_END)
        file_size = f.tell()
        f.seek(0,0)
        print 'Sending...'
        self.send_int(file_size)
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                self.sock.send(chunk)
            else:
                break
        print self.sock.recv(chunk_size)


if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    conf.read('./slave.config')
    master = master()
    args = {'content':'yourname.jpg','style':'yourname.jpg'}
    master.dispatch('127.0.0.1',8666,args)