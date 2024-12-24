from routes import app  # Import the app instance from routes.py


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)