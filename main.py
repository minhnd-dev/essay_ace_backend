from flask import Flask

from app.routes.auth import auth_bp
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    app.register_blueprint(auth_bp)
    app.run(debug=True, host='0.0.0.0')
