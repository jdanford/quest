import os

from quest import db
from quest.factory import create_app, register_blueprints


app = create_app()
register_blueprints(app)

db.init_app(app)
db.create_all(app=app)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
