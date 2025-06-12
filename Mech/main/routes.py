from flask import Blueprint, render_template, flash, redirect, url_for
from flask import Response
from forms import LogisticsForm
from models import db, Cars
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/admin_main')
def admin_main():
    return render_template('admin.html')

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


@main.route('/model_pred', methods=['GET'])
def model_pred():
    # Sample training data
    data = [
        (500000, 1998, 15000),
        (300000, 1995, 20000),
        (100000, 1994, 8000),
        (70000, 1997, 12000),
        (250000, 2005, 25000),
        (31000, 2000, 25000),
        (425070, 2003, 25000),
        (201111, 2006, 25000),
    ]

    X = [[mileage, year] for mileage, year, _ in data]
    y = [price for _, _, price in data]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    def predict_price(mileage, man_year):
        return model.predict([[mileage, man_year]])[0]

    car = Cars.query.order_by(Cars.id.desc()).first()
    if not car:
        flash("No car data available.")
        return redirect(url_for('main.predict'))

    predicted_price = predict_price(car.mileage, car.man_year)

    # --- Matplotlib visualization ---
    fig, ax = plt.subplots()
    mileage_data = [m for m, _, _ in data]
    price_data = [p for _, _, p in data]

    # Scatter training data
    ax.scatter(mileage_data, price_data, color='blue', label='Training Data')
    # Plot the predicted point
    ax.scatter(car.mileage, predicted_price, color='red', label='Predicted Car', marker='x', s=100)
    ax.set_xlabel('Mileage')
    ax.set_ylabel('Price')
    ax.set_title('Car Price Prediction')
    ax.legend()

    # Convert plot to PNG image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render_template('model_pred.html', car=car, predicted_price=round(predicted_price, 2), plot_url=image_base64)
