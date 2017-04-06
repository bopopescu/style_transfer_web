# encoding=utf8
import ConfigParser
import logging
import socket
import os
import json
import struct
import yaml

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
        print 'file size:%d'%file_size
        self.send_int(file_size)
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                self.sock.send(chunk)
            else:
                break
        print self.sock.recv(chunk_size)


if __name__ == "__main__":
    master = master()
    args = {'task_id':2,'content':'sanfrancisco.jpg','style':'starry_night.jpg','model':'vgg16','ratio':1e4}
    # master.dispatch('10.0.0.64',8667,args)
    master.dispatch('127.0.0.1', 8666, args)