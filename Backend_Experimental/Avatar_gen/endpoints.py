import Avatar_gen.pymoji as mj
import tempfile
import os
from flask import send_file, request
from flask_restx import Resource
import json
import random

class AvatarRandom(Resource):
    def get(self):
        path = None
        # generate random string 20 char max
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=20))
        avatar, index_dict = mj.avatar_from_username(username)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmp_file:
            avatar.render(tmp_file.name)
            path = tmp_file.name
        response = send_file(path, mimetype='image/svg+xml')
        response.headers['index-dict'] = json.dumps(index_dict)

        @response.call_on_close
        def cleanup(response):
            try:
                os.remove(path)
            except Exception as e:
                pass
        return response


class AvatarUsername(Resource):
    def get(self, username):
        path = None
        avatar, index_dict = mj.avatar_from_username(username)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmp_file:
            print(tmp_file.name)
            avatar.render(tmp_file.name)
            path = tmp_file.name
        response = send_file(path, mimetype='image/svg+xml')
        response.headers['index-dict'] = json.dumps(index_dict)

        @response.call_on_close
        def cleanup(response):
            try:
                os.remove(path)
            except Exception as e:
                pass
        return response


class AvatarRegenerate(Resource):
    def get(self, action_type, attr):
        # Get index_dict from headers
        data = request.headers.get('index-dict', '{}')

        if not index_dict:
            return {'error': 'Index_dict not found in headers'}, 404

        try:
            index_dict = json.loads(data)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON in index_dict header'}, 400

        # Regenerate avatar
        avatar, index_dict = mj.regenerate_avatar(index_dict, action_type, attr)
        if avatar is None:
            return {'error': 'Invalid action_type or attr'}, 400

        path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmp_file:
            avatar.render(tmp_file.name)
            path = tmp_file.name
        response = send_file(path, mimetype='image/svg+xml')
        response.headers['index-dict'] = json.dumps(index_dict)

        @response.call_on_close
        def cleanup(response):
            try:
                os.remove(path)
            except Exception as e:
                pass

        return response
    
    def options(self, action_type, attr):
        # retunt that the aviavle headers are content type and index_dict
        return {'headers': ['Content-Type', 'Index_dict']}, 200