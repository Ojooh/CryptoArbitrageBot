import os
import datetime

class Logger:
    def __init__(self, log_file_name=None):
        if log_file_name is None:
            current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            log_file_name = f"crypto_arbitrage_log_{current_timestamp}.log"

        self.log_file_path = self.get_log_file_path(log_file_name)
        
    def get_log_file_path(self, log_file_name):
        # Get the absolute path of the directory containing the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get the absolute path of the 'data' directory relative to the script directory
        data_dir = os.path.join(script_dir, '..', 'logs')

        # Construct the absolute path of the JSON file
        log_file_path = os.path.join(data_dir, log_file_name)

        return log_file_path

    def log(self, message, status='info'):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time} [{status.upper()}]: {message}"

        # Append log to file
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_message + '\n')

        # Print log to screen with different color based on status
        if status == 'info':
            print(log_message)
        elif status == 'success':
            print('\033[92m' + log_message + '\033[0m')  # Green text
        elif status == 'error':
            print('\033[91m' + log_message + '\033[0m')  # Red text

# Example usage:
# logger = Logger()
# logger.log("Starting Crypto Arbitrage Bot...")
# logger.log("Arbitrage opportunity found!", status='success')
# logger.log("Error occurred!", status='error')
# ...
