import socket
import threading
import subprocess
import signal

try:
    import ssl
except ImportError:
    ssl = None;

from .cfgparser import parseCFG
from .nrpe import *


SERVER_ACTIVE = True


class NRPEServer(object):
    def session_processor(self,sockobj):
        data = sockobj.recv(1036);
        try:
            version, res_type, crc, res_code, buffer, idk = struct.unpack(PACKET_FORMAT, data);
        except:
            print("Received unknown packet format");
            sockobj.close();
            return;

        #test crc
        test_crc = NrpePacket(buffer,version,res_type,res_code,idk);
        if test_crc.crc != crc:
            response = NrpePacket("CRC ERROR", version, 2, 2, '\x00\x00')
        else:
            command = buffer.split()[0].strip('\x00'); #get command only. ignore arguments

            if command not in self.options['command']:
                response = NrpePacket("Unknown command: %s" % command, version, 2, 127, '\x00\x00');
            else:
                print("<%s> Running %s.." % (sockobj,self.options['command'][command]))
                try:
                    proc = subprocess.Popen(self.options['command'][command],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True);

                    #countdown for command execution time timeout
                    countdown = threading.Timer(int(self.options['command_timeout']),proc.send_signal,[signal.SIGKILL])
                    countdown.start();

                    stdout,stderr = proc.communicate(); #execute command
                    countdown.cancel();

                    exit_code = proc.returncode & 0xffff; #apply two's complement
                    response = NrpePacket((stdout if stdout else stderr) if exit_code != 65527 else "Command timeout exceeded",version,2,exit_code,'\x00\x00')
                except Exception as e:
                    response = NrpePacket(str(e),2,2,2,'\x00\x00')

        #do command
        print("<%s> Sending response: %s" % (sockobj,response._NrpePacket__buffer));
        sockobj.send(response.data);
        sockobj.close();

    def __set_default_options(self):
        self.options.setdefault('connection_timeout',120)
        self.options.setdefault('server_port',5666)
        self.options.setdefault('command_timeout',30)
        self.options.setdefault('server_address',"")


    def listen(self,use_ssl=True):
        #check if ssl module exists
        use_ssl = use_ssl if ssl else False;

        self.__set_default_options();
        #socket.setdefaulttimeout(int(self.options['connection_timeout']));

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        sock.bind((self.options['server_address'],int(self.options['server_port'])));
        sock.listen(32);
        print("NRPE Emulator is now running");
        print("SSL is " + ("enabled" if use_ssl else "disabled"));
        while SERVER_ACTIVE:
            conn, addr = sock.accept()

            if 'allowed_hosts' in self.options:
                if addr[0] not in self.options['allowed_hosts'].split():
                    print("Blocked connection request from %s:%s" % (addr))
                    conn.close();
                    continue;

            if use_ssl:
                #wrap socket in ssl. protocol is abstracted from me yay
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23);
                context.set_ciphers("ALL:DH");
                context.load_dh_params("dhparam.pem");
                try:
                    conn = context.wrap_socket(conn,server_side=True);
                except Exception as e:
                    print(e)
                    conn.close();

            conn.settimeout(int(self.options['connection_timeout']));
            print("<%s> Accepted connection request from %s:%s" % ((conn,) + addr));
            threading.Thread(target=self.session_processor,args=(conn,)).start();
        sock.close();

    def __init__(self,nrpecfg_path):
        self.options = parseCFG(nrpecfg_path);




