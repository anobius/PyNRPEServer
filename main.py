from lib.server import NRPEServer
from lib.shared.log import logIntf

def main():
    ######
    import sys
    rs = sys.stdout;
    rserr = sys.stderr;
    logIntf.write = staticmethod(logIntf.info)
    logIntf.flush = staticmethod(rs.flush)
    sys.stdout = logIntf;
    #####
    a = NRPEServer(sys.argv[1]);

    a.listen();

main()
