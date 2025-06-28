from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from forms import LinearForm
from models import db, Cars, User
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

main = Blueprint('main', __name__, template_folder='templates')



@main.route('/market')
@login_required
def market():

    car = Cars.query.order_by(Cars.id.desc()).first()

    if not car:
        flash("No car data available.")
        return redirect(url_for('main.predict'))

    # Data for regression
    data = [
        (320000, 1992, 3200),
        (280000, 1995, 4500),
        (350000, 1996, 3800),
        (310000, 1998, 5200),
        (400000, 1990, 2100),
        (390000, 1993, 3050),
        (270000, 2000, 5900),
        (330000, 1997, 4700),
        (300000, 1999, 4250),
        (360000, 1991, 3100),
        (340000, 1994, 3600),
        (260000, 2001, 4950),
        (295000, 1996, 2800),
        (130000, 2005, 6000),
        (280000, 2003, 3300),
        (270000, 2004, 3900),
        (250000, 2007, 5100),
        (320000, 2002, 2950),
        (310000, 2006, 5750),
        (380000, 1995, 2200),
        (240000, 2008, 5500),
        (180000, 2010, 7200),
        (150000, 2012, 7500),
        (200000, 2011, 6800),
        (220000, 2009, 6100),
        (140000, 2014, 8200),
        (100000, 2015, 8900),
        (175000, 2013, 7700),
        (90000, 2016, 9200),
        (80000, 2017, 9600),
        (195000, 2011, 6900),
        (160000, 2012, 7400),
        (230000, 2008, 5650),
        (145000, 2013, 8000),
        (120000, 2014, 8500),
        (105000, 2016, 9100),
        (85000, 2018, 9800),
        (75000, 2019, 10200),
        (60000, 2020, 11000),
        (50000, 2021, 11500),
        (45000, 2022, 12000),
        (38000, 2023, 12500),
        (32000, 2024, 13000),
        (90000, 2017, 9500),
        (190000, 2009, 6050),
        (210000, 2010, 6400),
        (205000, 2009, 6150),
        (225000, 2007, 5300),
        (285000, 2005, 4700),
        (310000, 2006, 5600)
    ]

    # Train model
    X = [[mileage, year] for mileage, year, _ in data]
    y = [price for _, _, price in data]
    model = LinearRegression()
    model.fit(X, y)

    # Predict price
    predicted_price = model.predict([[car.mileage, car.man_year]])[0]

    return render_template(
        'market.html',
        brand=car.car_brand,
        mileage=car.mileage,
        predicted_price=round(predicted_price, 2)
    )

@main.route('/profile')
@login_required
def profile():
    example_cars = [
        {"brand": "Toyota", "mileage": 55000, "year": 2018, "price": 13500,
         "image": "https://img-optimize.toyota-europe.com/resize/ccis/680x680/zip/bg/product-token/f3520d05-ebaf-4991-adfc-fbea35192b82/vehicle/78088/padding/50,50,50,50/image-quality/70/day-exterior-03_2VN.png"},

        {"brand": "BMW", "mileage": 72000, "year": 2016, "price": 17000,
         "image": "https://www.bmw.bg/content/dam/bmw/common/all-models/m-series/m8-coupe/2022/navigation/bmw-8series-coupe-modellfinder.png"},

        {"brand": "Honda", "mileage": 45000, "year": 2019, "price": 14200,
         "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQMfyGxQjEh4nd3Kpc-NjowoP4uiWV9I-lOw&s"},

        {"brand": "Audi", "mileage": 61000, "year": 2017, "price": 19000,
         "image": "https://autodir.bg/wp-content/uploads/2024/11/gamata-avtomobili-na-audi-za-2025-g-oshte-po-usyvyrshenstvan-a3-optimiziran-a5-i-predstoyashti-elekt.jpg"},

        {"brand": "Mazda", "mileage": 38000, "year": 2020, "price": 12500,
         "image": "https://7cars.bg/wp-content/uploads/2024/05/3-copy-4.jpg"},

        {"brand": "Ford", "mileage": 83000, "year": 2015, "price": 9800,
         "image": "https://ford-cdn.fsn1.your-objectstorage.com/koe55a7btgkbs8y0s9qihcuyiw8e"},

        {"brand": "Mercedes-Benz", "mileage": 59000, "year": 2018, "price": 22000,
         "image": "https://images.netdirector.co.uk/gforces-auto/image/upload/w_412,h_309,dpr_2.0,q_auto,c_fill,f_auto,fl_lossy/auto-client/e8a412e90a1a356ab8ffd5e2aaa7e268/untitled_123.png"},

        {"brand": "Volkswagen", "mileage": 47000, "year": 2021, "price": 17800,
         "image": "https://groupcms-services-api.porsche-holding.com/dam/images/b9f671ae257ad59305d0f5e7e46c9775cda8eb8a/e2b72b06274ea54d0111788da54530e0/b1c4d4ab-997d-4178-b161-251ba1f63e29/crop:SMART/resize:3840:1743/derneuegolfvariantfrontside"},

        {"brand": "Hyundai", "mileage": 52000, "year": 2020, "price": 13900,
         "image": "https://hips.hearstapps.com/hmg-prod/images/2025-hyundai-tucson-phev-113-660424e2cef90.jpg?crop=0.753xw:0.637xh;0.0994xw,0.322xh&resize=2048:*"},

        {"brand": "Nissan", "mileage": 61000, "year": 2019, "price": 12700,
         "image": "https://www-europe.nissan-cdn.net/content/dam/Nissan/bulgaria/juke/F16/Juke_Desktop-Tablet_3000x1160.jpg.ximg.l_full_m.smart.jpg"}
    ]

    # If you really need to query the user from DB (instead of just using current_user):
    # user = User.query.get(current_user.id)
    # return render_template('profile.html', user=user, example_cars=example_cars)

    # Otherwise, this is totally fine:
    return render_template('profile.html', user=current_user, example_cars=example_cars)


@main.route('/admin_main')
@login_required
def admin_main():
    return render_template('admin.html')

@main.route('/main')
@login_required
def index():
    return render_template('main.html')

@main.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = LinearForm()
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
@login_required
def model_pred():
    data = [
        (320000, 1992, 3200),
        (280000, 1995, 4500),
        (350000, 1996, 3800),
        (310000, 1998, 5200),
        (400000, 1990, 2100),
        (390000, 1993, 3050),
        (270000, 2000, 5900),
        (330000, 1997, 4700),
        (300000, 1999, 4250),
        (360000, 1991, 3100),
        (340000, 1994, 3600),
        (260000, 2001, 4950),
        (295000, 1996, 2800),
        (130000, 2005, 6000),
        (280000, 2003, 3300),
        (270000, 2004, 3900),
        (250000, 2007, 5100),
        (320000, 2002, 2950),
        (310000, 2006, 5750),
        (380000, 1995, 2200),
        (240000, 2008, 5500),
        (180000, 2010, 7200),
        (150000, 2012, 7500),
        (200000, 2011, 6800),
        (220000, 2009, 6100),
        (140000, 2014, 8200),
        (100000, 2015, 8900),
        (175000, 2013, 7700),
        (90000, 2016, 9200),
        (80000, 2017, 9600),
        (195000, 2011, 6900),
        (160000, 2012, 7400),
        (230000, 2008, 5650),
        (145000, 2013, 8000),
        (120000, 2014, 8500),
        (105000, 2016, 9100),
        (85000, 2018, 9800),
        (75000, 2019, 10200),
        (60000, 2020, 11000),
        (50000, 2021, 11500),
        (45000, 2022, 12000),
        (38000, 2023, 12500),
        (32000, 2024, 13000),
        (90000, 2017, 9500),
        (190000, 2009, 6050),
        (210000, 2010, 6400),
        (205000, 2009, 6150),
        (225000, 2007, 5300),
        (285000, 2005, 4700),
        (310000, 2006, 5600)
    ]

    X = [[mileage, year] for mileage, year, _ in data]
    y = [price for _, _, price in data]
    model = LinearRegression()
    model.fit(X, y)

    def predict_price(mileage, man_year):
        return model.predict([[mileage, man_year]])[0]

    if request.method == 'POST':
        # Extract user input from form
        car_brand = request.form.get('car_brand')
        mileage = request.form.get('mileage')
        man_year = request.form.get('man_year')

        # Basic validation - you can improve this as needed
        if not car_brand or not mileage or not man_year:
            flash('Please provide all required fields.')
            return redirect(url_for('main.predict'))

        try:
            mileage = int(mileage)
            man_year = int(man_year)
        except ValueError:
            flash('Mileage and Year must be numbers.')
            return redirect(url_for('main.predict'))

        # Save new car data to DB
        new_car = Cars(car_brand=car_brand, mileage=mileage, man_year=man_year)
        db.session.add(new_car)
        db.session.commit()

        car = new_car
    else:
        # If GET or no POST data, get latest car for prediction
        car = Cars.query.order_by(Cars.id.desc()).first()
        if not car:
            flash("No car data available.")
            return redirect(url_for('main.predict'))

    predicted_price = predict_price(car.mileage, car.man_year)

    # Plot code same as before...

    fig, ax = plt.subplots()

    mileage_data = [m for m, _, _ in data]
    price_data = [p for _, _, p in data]
    ax.scatter(mileage_data, price_data, color='blue', label='Training Data')
    ax.scatter(car.mileage, predicted_price, color='red', label='Predicted Car', marker='x', s=100)

    mileage_range = list(range(min(mileage_data), max(mileage_data), 1000))
    predicted_line_prices = [predict_price(mileage, car.man_year) for mileage in mileage_range]
    ax.plot(mileage_range, predicted_line_prices, color='green',
            label=f'Regression Line (Year={car.man_year})', linewidth=2)

    ax.set_xlabel('Mileage')
    ax.set_ylabel('Price')
    ax.set_title('Car Price Prediction')
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    static_path = os.path.join('static', 'prediction_chart.png')
    with open(static_path, 'wb') as f:
        f.write(buf.getbuffer())

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render_template(
        'model_pred.html',
        car=car,
        predicted_price=round(predicted_price, 2),
        plot_url=image_base64
    )


@main.route('/admin/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('main.view_users'))


@main.route('/progress')
@login_required
def progress():
    return('Hellow World')