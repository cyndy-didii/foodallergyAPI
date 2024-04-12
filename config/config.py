class Config:
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60
    SECRET_KEY = 'secret key'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    MAX_UPLOAD_FILE_SIZE = 2 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/food_allergies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Change this to a random secret key
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expires in 1 hour