from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

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

    if latest_car:
        car_brand = latest_car.car_brand
        mileage = latest_car.mileage
        man_year = latest_car.man_year
    else:
        car_brand = None
        mileage = None
        man_year = None

    return render_template('model_pred.html', car_brand=car_brand, mileage=mileage, man_year=man_year)
