from flask import Flask, render_template, request, url_for
import model as mod
import numpy as np
import plots as plot
import location_stat as stat

app = Flask(__name__)


@app.route('/')
def home():
    model, locations, off = mod.rent_price_model()
    return render_template('main.html', locations=locations, plot1='/static/images/plot_avg_price.png', plot2='/static/images/plot_number_of_offers.png', plot3='static/images/plot_historical.png')


@app.route('/estimate_cost', methods=['POST'])
def estimate_cost():
    model, locations, order = mod.rent_price_model()
    loc = request.form['chosen_location']

    loc = mod.hot_one_encoding('location_'+loc, order)
    loc = [float(l) for l in loc]
    try:
        area = float(request.form['area'])
        rooms = int(request.form['rooms'])
    except ValueError:
        print("hello")
        answer = "Podano błędny format danych"
        return render_template('main.html', locations=locations, predicted=answer,
                               plot1='/static/images/plot_avg_price.png',
                               plot2='/static/images/plot_number_of_offers.png',
                               plot3='static/images/plot_historical.png')
    if area < 0 or rooms < 0:
        answer = "Podane dane nie mogą być ujemne"

        return render_template('main.html', locations=locations, predicted=answer,
                               plot1='/static/images/plot_avg_price.png', plot2='/static/images/plot_number_of_offers.png', plot3='static/images/plot_historical.png')

    data = np.asarray([rooms, area, *loc]).reshape(-1, 19)
    predicted = model.predict(data)
    if predicted < 100:
        predicted = 100
    answer = "Przewidywana cena: {} PLN".format(round(*predicted, 2))

    return render_template('main.html', locations=locations, predicted=answer, plot1='/static/images/plot_avg_price.png', plot2='/static/images/plot_number_of_offers.png', plot3='static/images/plot_historical.png')


@app.route('/dzielnica', methods=['POST'])
def dzielnica():
    loc = request.form['chosen_location']
    loc = loc[1:]
    offers_count = stat.get_number_of_offers(loc)
    #avg = stat.get_avg_price(loc)
    avg_ratio, med, q1, q3 = stat.get_location_stats(loc)

    location = loc.replace(' ', '_')
    all_offers_count, all_avg_price_ratio, all_med, all_q1, all_q3 = plot.get_data()
    offers_ratio = 100*round(offers_count/all_offers_count, 2)
    all_avg_price_ratio = round(all_avg_price_ratio, 2)


    return render_template('location.html', off=offers_count, off_ratio=offers_ratio, boxplot='/static/images/loc_{}.png'.format(location), loc=loc, avg_ratio=avg_ratio,all_avg_price_ratio=all_avg_price_ratio, price_plot='/static/images/loc_price__{}.png'.format(location),all_med=all_med, all_q1=all_q1, all_q3=all_q3, med=med, q1=q1, q3=q3)


if __name__ == "__main__":
    app.run()







