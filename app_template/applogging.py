

import logging
import socketserver


class ApplicationLoggingSetting():

    def __init__(self, logger_name, host:str, port:int):
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.root_logger = logging.getLogger()
        self.host = host
        self.port = port 

    
    def setting_logger(self):
        socket_handler = logging.handlers.SocketHandler(self.host, self.port)
        self.root_logger.addHandler(socket_handler)

    def get_logger(self):
        return self.logger