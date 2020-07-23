from app import app

if __name__ == "__main__":
    app.debug = True
    app.run(ssl_context='adhoc', port=5001, debug=True)
