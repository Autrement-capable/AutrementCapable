import endpoints.auth.authOpps
import endpoints.auth.email_opps
import endpoints.auth.loginRegisterEndpoint


from os import getenv
if getenv("MODE") == "DEV":
    import endpoints.dev.table_manipulation