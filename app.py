from flask import Flask, render_template, request, url_for
import model as mod
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    model, locations, off = mod.rent_price_model()
    return render_template('main.html', locations=locations)


@app.route('/estimate_cost', methods=['POST'])
def estimate_cost():
    model, locations, order = mod.rent_price_model()
    area = float(request.form['area'])
    rooms = float(request.form['rooms'])
    loc = request.form['chosen_location']

    loc = mod.hot_one_encoding('location_'+loc, order)
    loc = [float(l) for l in loc]

    data = np.asarray([rooms, area, *loc]).reshape(-1, 19)
    predicted = model.predict(data)

    return render_template('main.html', locations=locations, predicted=predicted)


if __name__ == "__main__":
    app.run()