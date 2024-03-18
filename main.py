from flask import Flask

from app.routes.auth import auth_bp
from flask_cors import CORS

from app.routes.feedback import feedback_bp
from app.routes.response import response_bp
from app.routes.topic import topic_bp
from app.routes.writing import write_bp

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    app.register_blueprint(auth_bp)
    app.register_blueprint(write_bp)
    app.register_blueprint(topic_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(response_bp)
    app.run(debug=True, host="0.0.0.0")
