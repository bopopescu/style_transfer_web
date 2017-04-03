# encoding=utf8
import ConfigParser
import logging
import socket
import json
import struct
import os
import time
from transfer import transfer
import yaml

# logging
LOG_FORMAT = "%(filename)s:%(funcName)s:%(asctime)s.%(msecs)03d -- %(message)s"

class slave:
    conf = None
    sock = None
    host = None
    port =None
    conn = None #保存和master的socket
    #start listening
    def __init__(self,conf):
        self.conf =conf
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = conf.get("transmission", "slave_ip")
        self.port = conf.getint("transmission", "slave_port")

    def start(self):

        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        logging.info('Server start at: %s:%d' % (self.host, self.port))
        while True:
            logging.info("wait for connection...")
            self.conn, addr = self.sock.accept()
            logging.info('Connected by %s'%(addr[0]))
            args = self.receive_json()
            content = os.path.split(args.get('content'))[1]
            style = os.path.split(args.get('style'))[1]
            args["gpu_id"] = self.conf.getint("runtime",'gpu_id')
            args["content"] = os.path.join(self.conf.get('runtime','content_dir'),content)
            args["style"] = os.path.join(self.conf.get('runtime','style_dir'),style)
            print args
            self.receive_file(args["content"])
            self.receive_file(args["style"])
            trans = transfer(args,send_result)
            #trans.process()
            # data = conn.recv(1024)
            # print data
            # conn.send("slave receive your order. Your order is '%s'"%data)

    #json
    def receive_json(self):
        unpacker = struct.Struct('I')
        data = self.conn.recv(unpacker.size)
        length = unpacker.unpack(data)[0]
        jstr = self.conn.recv(length)
        obj  = yaml.safe_load(jstr)
        return obj

    def receive_int(self):
        unpacker = struct.Struct('I')
        data = self.conn.recv(unpacker.size)
        return unpacker.unpack(data)[0]

    #receive the image to be transferred
    def receive_file(self,filename,chunk_size=1024):
        f = open(filename, 'wb')
        print 'Receiving...'
        file_size = self.receive_int()
        print "filesize:",file_size
        while file_size > 0:
            if file_size > chunk_size:
                chunk = self.conn.recv(chunk_size)
            else:
                chunk = self.conn.recv(file_size)
            file_size -= len(chunk)
            f.write(chunk)
        self.conn.send("Done")
        f.close()

def send_result(result):
    logging.info('Sending result %s to web server...'%result)

if __name__=="__main__":
    conf = ConfigParser.ConfigParser()
    conf.read('./client.config')
    logging.basicConfig(format=LOG_FORMAT, datefmt="%H:%M:%S", level=logging.INFO)
    slave =slave(conf)
    slave.start()