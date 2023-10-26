

import sys
import argparse
import logging
import os



class CommunicationAgent:
    def __init__(self):
        self.setup_logger()
    
    def setup_logger(self):
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to the log file within that directory
        log_filename = os.path.join(script_dir, 'workflow.log')

        # Check if the file already exists
        if os.path.exists(log_filename):
            os.remove(log_filename)

        # Configure logging settings
        logging.basicConfig(filename=log_filename,
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def run(self):
        role = "Communication Agent"
        print("Communication Agent initialized")

        message = "Communication Agent has been initiated"

        # Write a sample message to the log file
        self.log_message(role, message)

    @staticmethod
    def log_message(role, message):
        logging.info(' ' + role + '\n' + '\n' + 'Message: ' + message + '\n')

if __name__ == "__main__":
    agent = CommunicationAgent()
    agent.run()