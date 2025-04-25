from fastapi.middleware.cors import CORSMiddleware

def init_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8080",
            "http://localhost:8081",
            "https://localhost:8080",
            "https://localhost:8081",
            "http://localhost:5000",
            "https://localhost:5000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
