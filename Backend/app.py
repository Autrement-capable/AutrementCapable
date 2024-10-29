from server.server import server
import server.route_includer
import atexit


def CleanUp():
    scheculer = server.scheduler
    if scheculer.running:
        print("Cleaning up has started")
        scheculer.shutdown(wait=False)
        print("Cleaning up has ended")

if __name__ == "__main__":
    try:
        server.Run()
        atexit.register(CleanUp)
    except Exception as e:
        print("Error: " + str(e))
        exit(1)