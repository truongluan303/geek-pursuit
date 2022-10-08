from flask import Flask

from geek_pursuit.routes import *


app = Flask(__name__)

app.register_blueprint(routes)


if __name__ == "__main__":
    app.run()
