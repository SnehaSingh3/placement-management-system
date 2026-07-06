from flask import Flask
from models import db, Admin

app = Flask(__name__)

app.config.from_object("config")
db.init_app(app)    


import routes

with app.app_context():
      db.create_all()   
      admin = Admin.query.first()

      if not admin:
            admin = Admin(
                username="admin",
                passhash="admin123"
        )

            db.session.add(admin)
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
