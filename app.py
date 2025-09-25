
from flask import Flask
from models.user import db
from extensions.login_manager import login_manager
from extensions.mail import mail
from routes.auth import auth
from routes.main import main

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
