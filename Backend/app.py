from server.server import server as svr
import server.route_includer
import atexit


def CleanUp():
    scheculer = svr.scheduler
    if scheculer.running:
        print("Cleaning up has started")
        scheculer.shutdown(wait=False)
        print("Cleaning up has ended")


# Make sure that 'svr' is an ASGI-compatible app (e.g., FastAPI instance)
app = svr.app

# Ensure that CleanUp is registered when the module is imported
atexit.register(lambda: CleanUp())
