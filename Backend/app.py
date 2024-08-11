from config.mainConfig import server
import config.auth
import modules.login.loginEndpoint

import atexit


def CleanUp(): # runs twice, but that's ok , this is beacuse of flask debug mode creating a child process
    scheculer = server.scheduler
    if scheculer.running:
        print("Cleaning up has started")
        scheculer.shutdown(wait=False)
        print("Cleaning up has ended")
    # config.client.close()

if __name__ == "__main__":
    try:
        server.Run()
        atexit.register(CleanUp)
    except Exception as e:
        print("Error: " + str(e))
        exit(1)