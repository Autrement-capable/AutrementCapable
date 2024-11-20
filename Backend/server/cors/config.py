from fastapi.middleware.cors import CORSMiddleware

def init_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],  # Update this as per your allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
