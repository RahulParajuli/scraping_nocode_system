import logging

class ClickClickLogger:
    def __init__(self, log_file='app.log', log_level=logging.DEBUG):
        self.logger = logging.getLogger('ClickClickLogger')
        self.logger.setLevel(log_level)
        
    
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)

if __name__ == '__main__':
    # Example usage:
    logger = ClickClickLogger()
    logger.log('This is an info message.', logging.INFO)
    logger.log('This is a warning message.', logging.WARNING)
    logger.log('This is an error message.', logging.ERROR)
