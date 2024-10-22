import modules.auth.authOpps
import modules.auth.loginRegisterEndpoint


from os import getenv
if getenv("MODE") == "DEV":
    import modules.testing