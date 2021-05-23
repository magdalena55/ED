from flask import Flask, render_template, request, url_for
import model as mod
import numpy as np
import plots as plot
import location_stat as stat

app = Flask(__name__)

plot.plot_avg_price_fo_each_loc()
plot.plot_number_of_offers()
plot.historical_plot()



@app.route('/')
def home():
    model, locations, off = mod.rent_price_model()
    return render_template('main.html', locations=locations, plot1='/static/images/plot_avg_price.png', plot2='/static/images/plot_number_of_offers.png', plot3='static/images/plot_historical.png')


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
    if predicted < 100:
        predicted = 100

    predicted = "Przewidywana cena: {}".format(*predicted)

    return render_template('main.html', locations=locations, predicted=predicted, plot1='/static/images/plot_avg_price.png', plot2='/static/images/plot_number_of_offers.png', plot3='static/images/plot_historical.png')


@app.route('/dzielnica', methods=['POST'])
def dzielnica():
    loc = request.form['chosen_location']
    loc = loc[1:]
    offers_count = stat.get_number(loc)
    avg = stat.get_avg_price(loc)
    stat.price_boxplot(loc)

    return render_template('location.html', off=offers_count,avg=avg,boxplot='/static/images/loc.png', loc=loc)


if __name__ == "__main__":
    app.run()







