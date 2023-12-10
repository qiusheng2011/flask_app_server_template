import socketserver
import logging
import pickle
import struct


class LogRecordStreamRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen-len(chunk))
            obj = pickle.loads(chunk)
            print(obj)
            record = logging.makeLogRecord(obj)
            logging.getLogger(self.server.logname).handle(record)


class LogRecordSocketServer(socketserver.ThreadingTCPServer):

    logname = "test_socket_log"

    def __init__(self, host, port, hander):
        super().__init__((host, port), hander)


def setting_logger(file_path, logname):
    logging.basicConfig(
        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
    logger = logging.getLogger(logname)
    logfile_handler = logging.FileHandler(
        f"{file_path}{logname}.log", encoding="utf8")
    logfile_handler.setFormatter(fmt=logging.Formatter('%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s'))
    logger.addHandler(logfile_handler)


def main():

    setting_logger("./","test_socket_log")

    with LogRecordSocketServer("0.0.0.0", 9020, LogRecordStreamRequestHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
