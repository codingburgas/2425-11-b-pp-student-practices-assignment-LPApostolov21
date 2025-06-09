from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
import random
from forms import LogisticsForm
from models import db, Cars

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/main')
def index():
    return render_template('main.html')


@main.route('/predict', methods=['GET', 'POST'])
def predict():
    form = LogisticsForm()
    if form.validate_on_submit():
        car_brand = form.car_brand.data
        mileage = form.mileage.data
        man_year = form.man_year.data
        new_car = Cars(car_brand=car_brand, mileage=mileage, man_year=man_year)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('main.model_pred'))
    return render_template('predict.html', form=form)


@main.route('/model_pred', methods=['GET', 'POST'])
def model_pred():
    latest_car = Cars.query.order_by(Cars.id.desc()).first()

    prediction = None  # Default

    if latest_car:
        car_brand = latest_car.car_brand
        mileage = latest_car.mileage
        man_year = latest_car.man_year

        # --- Training Data (example)
        data = [
            (500500, 2006, 1),
            (400400, 2005, 0),
            (300300, 2004, 1),
            (200200, 2003, 0),
            (100100, 2002, 1),
            (500000, 2001, 0),
            (400000, 2000, 1),
            (300000, 1999, 0),
            (200000, 1998, 1),
            (100000, 1997, 0)
        ]

        # --- Helper: Mean
        def mean(values):
            return sum(values) / len(values)

        # --- Extract and Normalize
        mileages = [d[0] for d in data]
        years = [d[1] for d in data]
        labels = [d[2] for d in data]

        mean_mileage = mean(mileages)
        mean_year = mean(years)

        mileages = [m - mean_mileage for m in mileages]
        years = [y - mean_year for y in years]

        # --- Gradient Descent
        w0, w1, w2 = 0.0, 0.0, 0.0
        learning_rate = 0.00000001
        epochs = 1000

        for _ in range(epochs):
            dw0, dw1, dw2 = 0.0, 0.0, 0.0
            for i in range(len(data)):
                x1 = mileages[i]
                x2 = years[i]
                y = labels[i]
                y_pred = w0 + w1 * x1 + w2 * x2
                error = y_pred - y
                dw0 += error
                dw1 += error * x1
                dw2 += error * x2
            w0 -= learning_rate * dw0
            w1 -= learning_rate * dw1
            w2 -= learning_rate * dw2

        # --- Predict
        def predict(mileage_input, year_input):
            x1 = mileage_input - mean_mileage
            x2 = year_input - mean_year
            y_pred = w0 + w1 * x1 + w2 * x2
            return "Yes" if y_pred >= 0.5 else "No"

        prediction = predict(mileage, man_year)

        return render_template('model_pred.html',
                               car_brand=car_brand,
                               mileage=mileage,
                               man_year=man_year,
                               prediction=prediction)

    # If no car found
    return render_template('model_pred.html', prediction="No car found.")