from modules.config.Config import Config

import atexit
import os


def CleanUp(): # runs twice, but that's ok , this is beacuse of flask debug mode creating a child process
    print("Cleaning up has started")
    # config.client.close()

if __name__ == "__main__":
    try:
        config = Config()
        config.Run()
        atexit.register(CleanUp)
    except Exception as e:
        print("Error: " + str(e))
        exit(1)