import endpoints.auth.authOpps
import endpoints.auth.email_opps
import endpoints.auth.loginRegisterEndpoint
import endpoints.auth.passkeys


from os import getenv
if getenv("MODE") == "DEV":
    import endpoints.dev.table_manipulation
    import endpoints.dev.auth_check_endpoints