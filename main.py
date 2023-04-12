from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired()])
    open = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rate = SelectField("Coffee Rating", choices=["☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"])
    wifi_rate = SelectField("Wifi Strength Rating", choices=["✘","💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power_socket = SelectField("Coffee Rating", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit() and request.method == "POST":
        with open(r"cafe-data.csv", mode="a", encoding="UTF-8") as cs:
            cs.write(f"\n{form.cafe.data},{form.location.data},{form.open.data},{form.close.data},{form.coffee_rate.data},{form.wifi_rate.data},{form.power_socket.data}\n")

            cs.close()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
