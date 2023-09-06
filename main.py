from flask import Flask

from blueprints.distance_calc.distance_calc import distance_calc

app = Flask(__name__)
app.register_blueprint(distance_calc)

if __name__ == '__main__':
    app.run(debug=False)
