# encoding=utf8
import ConfigParser
import logging
import socket
import json
import struct
import os
import time


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
            obj = self.receive_json()
            content = obj.get('content')
            style = obj.get('style')
            self.receive_file(os.path.join(self.conf.get('runtime','content_dir'),content))
            self.receive_file(os.path.join(self.conf.get('runtime','style_dir'),style))
            self.transfer('content.jpg','style.jpg')
            # data = conn.recv(1024)
            # print data
            # conn.send("slave receive your order. Your order is '%s'"%data)

    #json
    def receive_json(self):
        unpacker = struct.Struct('I')
        data = self.conn.recv(unpacker.size)
        length = unpacker.unpack(data)[0]
        jstr = self.conn.recv(length)
        obj  = json.loads(jstr)
        return obj

    def receive_int(self):
        unpacker = struct.Struct('I')
        data = self.conn.recv(unpacker.size)
        return unpacker.unpack(data)[0]

    #receive the image to be transferred
    def receive_file(self,filename,chunk_size=1024):
        f = open(filename,'wb')
        print 'Receiving...'
        file_size = self.receive_int()
        while file_size>0:
            if file_size>chunk_size:
                chunk = self.conn.recv(chunk_size)
                file_size -= chunk_size
            else:
                chunk = self.conn.recv(file_size)
                file_size=0
            f.write(chunk)
        self.conn.send("Done")
        f.close()

    def transfer(self,content,style):
        logging.info('Transferring...')
        time.sleep(5)
        logging.info('Transfer Done...')
        pass

if __name__=="__main__":
    conf = ConfigParser.ConfigParser()
    conf.read('./client.config')
    logging.basicConfig(format=LOG_FORMAT, datefmt="%H:%M:%S", level=logging.INFO)
    slave =slave(conf)
    slave.start()