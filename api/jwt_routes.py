from flask import jsonify

def setup_routes(app, jwt):
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "code": 'FAILED',
            "message": "Authorization is required"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, expired_token):
        return jsonify({
            "code": 'FAILED',
            "message": "Token has expired. Please log in again."
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "code": 'FAILED',
            "message": "Signature verification failed. Please provide a valid token."
        }), 401
