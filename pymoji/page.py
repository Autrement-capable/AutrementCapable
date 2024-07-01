from flask import Flask, send_file, render_template_string
import io
import python_avatars as pa
import tempfile
import os
 # Assuming 'pa' is the module providing the Avatar functionality

app = Flask(__name__)

# Function to generate a random avatar
def random_avatar():
    return pa.Avatar.random()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Random Avatar</title>
    </head>
    <body>
        <h1>Random Avatar Generator</h1>
        <div id="avatar">
            <img src="/avatar" alt="Avatar" id="avatar-image">
        </div>
        <button onclick="generateAvatar()">Generate</button>

        <script>
            function generateAvatar() {
                fetch('/avatar')
                .then(response => response.blob())
                .then(blob => {
                    let url = URL.createObjectURL(blob);
                    document.getElementById('avatar-image').src = url;
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/avatar')
def avatar():
    avatar = random_avatar()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmp_file:
        avatar.render(tmp_file.name)
        tmp_file_path = tmp_file.name
    
    response = send_file(tmp_file_path, mimetype='image/svg+xml')
    
    # Clean up the temporary file after sending it
    @response.call_on_close
    def remove_file():
        try:
            os.remove(tmp_file_path)
        except OSError:
            pass
    
    return response

if __name__ == '__main__':
    app.run(debug=True)