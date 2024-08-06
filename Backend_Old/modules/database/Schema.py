users_collection_name = 'users'

# MongoDB schema for creating the users collection
create_user_collection_schema = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['id', 'name', 'surname', 'email', 'password'],
            'properties': {
                'id': {'bsonType': 'int'},
                'name': {'bsonType': 'string'},
                'surname': {'bsonType': 'string'},
                'email': {'bsonType': 'string'},
                'password': {'bsonType': 'string'},
                'subscribed': {'bsonType': 'bool'},
            },
        },
    },
}
user_activities_collection_name = 'userActivities'

# MongoDB schema for creating the userActivities collection
create_user_activities_collection_schema = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['id', 'userId', 'data-type', 'total-clicks'],
            'properties': {
                'id': {'bsonType': 'int'},
                'userId': {'bsonType': 'int'},
                'data-type': {'bsonType': 'string'},
                'total-clicks': {'bsonType': 'int'},
            },
        },
    },
}
