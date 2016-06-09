import datetime
import logging
import os.path


class Logger():
    
    def __init__(self,output_dir,debug_level):

        self.debug = debug_level

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # create error file handler and set level to error
        handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # create debug file handler and set level to debug
        handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    def log(self,status,msg):
        dt = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
        msg = dt + ": " + msg
        if status == 'info' and self.debug:
            self.logger.info(msg)
        elif status == 'critical':
            self.logger.critical(msg)
    
