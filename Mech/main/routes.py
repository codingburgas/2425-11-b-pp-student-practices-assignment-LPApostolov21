from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from forms import LinearForm
from models import db, Cars, User
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64

main = Blueprint('main', __name__, template_folder='templates')

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

@main.route('/model_pred', methods=['GET'])
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
        (380000, 1990, 2200)
    ]

    X = [[mileage, year] for mileage, year, _ in data]
    y = [price for _, _, price in data]
    model = LinearRegression()
    model.fit(X, y)

    def predict_price(mileage, man_year):
        return model.predict([[mileage, man_year]])[0]

    car = Cars.query.order_by(Cars.id.desc()).first()
    if not car:
        flash("No car data available.")
        return redirect(url_for('main.predict'))

    predicted_price = predict_price(car.mileage, car.man_year)

    fig, ax = plt.subplots()

    # Scatter plot of training data (mileage vs price)
    mileage_data = [m for m, _, _ in data]
    price_data = [p for _, _, p in data]
    ax.scatter(mileage_data, price_data, color='blue', label='Training Data')

    # Scatter plot of predicted car price
    ax.scatter(car.mileage, predicted_price, color='red', label='Predicted Car', marker='x', s=100)

    # --- Add regression line ---

    # Generate mileage values for line plot (cover the range in data)
    mileage_range = list(range(min(mileage_data), max(mileage_data), 1000))  # step 1000 for smoothness

    # Predict prices for each mileage at the fixed car.man_year
    predicted_line_prices = [predict_price(mileage, car.man_year) for mileage in mileage_range]

    # Plot the regression line
    ax.plot(mileage_range, predicted_line_prices, color='green', label=f'Regression Line (Year={car.man_year})', linewidth=2)

    ax.set_xlabel('Mileage')
    ax.set_ylabel('Price')
    ax.set_title('Car Price Prediction')
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render_template('model_pred.html', car=car, predicted_price=round(predicted_price, 2), plot_url=image_base64)

@main.route('/admin/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('main.view_users'))
