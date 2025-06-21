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


@main.route('/profile')
@login_required
def profile():
    existing_user = User.query.get(current_user.id)
    return render_template('profile.html', user=existing_user)

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

    # Scatter plot of training data
    mileage_data = [m for m, _, _ in data]
    price_data = [p for _, _, p in data]
    ax.scatter(mileage_data, price_data, color='blue', label='Training Data')

    # Predicted point
    ax.scatter(car.mileage, predicted_price, color='red', label='Predicted Car', marker='x', s=100)

    # Regression line
    mileage_range = list(range(min(mileage_data), max(mileage_data), 1000))
    predicted_line_prices = [predict_price(mileage, car.man_year) for mileage in mileage_range]
    ax.plot(mileage_range, predicted_line_prices, color='green',
            label=f'Regression Line (Year={car.man_year})', linewidth=2)

    ax.set_xlabel('Mileage')
    ax.set_ylabel('Price')
    ax.set_title('Car Price Prediction')
    ax.legend()

    # Save to buffer and static file
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Save to file
    static_path = os.path.join('static', 'prediction_chart.png')
    with open(static_path, 'wb') as f:
        f.write(buf.getbuffer())

    # Encode for inline display
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render_template(
        'model_pred.html',
        car=car,
        predicted_price=round(predicted_price, 2),
        plot_url=image_base64
    )

@main.route('/send_email', methods=['POST'])
@login_required
def send_email():
    sender_email = "LPApostolov21@codingburgas.bg"
    app_password = "my_secret_key"
    receiver_email = "ktotev@codingburgas.bg"
    subject = "🚗 Car Price Prediction Chart"
    body = "Attached is the chart from the latest car price prediction."

    chart_path = os.path.join('static', 'prediction_chart.png')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    try:
        with open(chart_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='prediction_chart.png')
            msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        flash("✅ Email sent successfully to ktotev@codingburgas.bg", "success")
    except Exception as e:
        flash(f"❌ Failed to send email: {str(e)}", "danger")

    return redirect(url_for('main.model_pred'))

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
