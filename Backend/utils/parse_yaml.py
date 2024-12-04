import yaml
from datetime import timedelta

def parse_duration(duration_config):
    """
    Parse a duration configuration and return the total duration in seconds.
    """
    months = duration_config.get("months", 0)
    days = duration_config.get("days", 0)
    hours = duration_config.get("hours", 0)
    minutes = duration_config.get("minutes", 0)
    seconds = duration_config.get("seconds", 0)

    # Convert months to days (approximate, assuming 30 days per month)
    total_days = months * 30 + days

    # Calculate total duration in seconds
    total_seconds = (
        total_days * 86400 +
        hours * 3600 +
        minutes * 60 +
        seconds
    )

    return total_seconds


def get_property(config:dict, property_name:str, sub_propertyList:list[str]=None, type:str="Time"):
    """
    Get the value of a property from a YAML file.

    Args:
        config (dict): The configuration dictionary. (YAML file loaded as a dictionary)
        property_name (str): The name of the property to retrieve.
        sub_propertyList (list[str], optional): The list of sub-properties to retrieve. Defaults to None.
        type (str, optional): The type of the property. Defaults to "Time".
    """
    if sub_propertyList:
        return_dict = {}
        work_config:dict = config.get(property_name)
        for sub_property in sub_propertyList:
            if type == "Time":
                prop_config:dict = work_config.get(sub_property)
                if not prop_config or not isinstance(prop_config, dict):
                    continue
                return_dict[sub_property] = parse_duration(prop_config)
            else:
                return_dict[sub_property] = work_config.get(sub_property)
        return return_dict
    else:
        return config.get(property_name)

# # Example usage
# if __name__ == "__main__":
#     with open("./server/config_files/config.yaml", "r") as file:
#         config = yaml.safe_load(file)

#     # Get the duration of the access token
#     token_duration = get_property(config, "auth", ["access_token_duration", "refresh_token_duration"])
#     print(f"access token duration: {token_duration['access_token_duration']} seconds")
#     print(f"refresh token duration: {token_duration['refresh_token_duration']} seconds")

#     # Get the mail server configuration
#     mail_server_config = get_property(config, "verify", ["email_verification_code_duration", "password_reset_code_duration"])
#     print(f"email verification code duration: {mail_server_config['email_verification_code_duration']} seconds")
#     print(f"password reset code duration: {mail_server_config['password_reset_code_duration']} seconds")