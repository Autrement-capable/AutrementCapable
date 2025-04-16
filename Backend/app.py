from server.server import server as svr
import endpoints
import atexit

def CleanUp():
    scheduler = svr.scheduler
    if scheduler.running:
        print("Cleaning up has started")
        scheduler.shutdown(wait=False)
        print("Cleaning up has ended")

# Ensure that CleanUp is registered when the module is imported
atexit.register(lambda: CleanUp())

# Make sure that 'svr' is an ASGI-compatible app (e.g., FastAPI instance)
app = svr.app
