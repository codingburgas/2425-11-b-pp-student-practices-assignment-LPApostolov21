# main/routes.py:

from flask import Blueprint, render_template
from flask_login import login_required

from forms import LogisticsForm

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/main')
def index():
    return render_template('main.html')


@main.route('/predict')
def predict():
    form = LogisticsForm()
    if form.validate_on_submit():
        pass
    return render_template('predict.html', form=form)