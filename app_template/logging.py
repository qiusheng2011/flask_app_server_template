

import logging



class ApplicationLoggingSetting():

    def __init__(self, logger_name, host:str, port:int):
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.log_file_path = log_file_path
        self.host = host
        self.port = port 
    
    def setting_logger(self):
        socket_handler = logging.handlers.SocketHandler(self.host, self.port)
        self.logger.addHandler(socket_handler)

    def get_logger(self):
        return self.logger
