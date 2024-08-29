from app import app
# from cryptography.hazmat.backends import default_backend

if __name__ == '__main__':
    app.run(debug=True, port=5001)

#backend = default_backend()