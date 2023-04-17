import pandas as pd
import numpy as np
import joblib
import flask
from flask import render_template, request
from wtforms import Form, IntegerField, validators

model = joblib.load('models/randomForestModel.pkl')


class CustomerDetails(Form):
    current_loan_amount = IntegerField('current loan amount',[validators.InputRequired()])
    term = IntegerField('term', [validators.InputRequired()])
    annual_income = IntegerField('annual income', [validators.InputRequired()])
    years_in_current_job = IntegerField('years in current job' ,[validators.InputRequired()])
    home_ownership = IntegerField('No. of homes you own', [validators.InputRequired()])
    current_credit_balance = IntegerField('current credit balance', [validators.InputRequired()])
    number_of_open_accounts = IntegerField('number of open accounts', [validators.InputRequired()])
    credit_score = IntegerField('credit score', [validators.InputRequired()])


app = flask.Flask(__name__, static_folder='statics')


@app.route('/', methods=['GET', 'POST'])
def index():
    is_qualified = None
    pred = [0]
    form = CustomerDetails(request.form)
    if request.method == 'POST' and form.validate():
# ['Current Loan Amount', 'Term', 'Annual Income', 'Years in current job','Current Credit Balance', 'Credit Score', 'Number of Open Accounts','Home Ownership']
        pred = model.predict([[
            form.data['current_loan_amount'],
            form.data['term'],
            form.data['annual_income'],
            form.data['years_in_current_job'],
            form.data['current_credit_balance'],
            form.data['credit_score'],
            form.data['number_of_open_accounts'],
            form.data['home_ownership'],
                      ]])
        print(pred[0])
        if pred[0] > 0:
            is_qualified = True
        else:
            is_qualified = False
    if is_qualified ==True:
        result_bg = "bg-success"
    elif is_qualified == False:
        result_bg = "bg-warning"
    else:
        result_bg = "bg-secondary text-light bg-gradient"
    return render_template('index.html', result_bg=result_bg, form=form, amount=pred[0])


app.run(debug=True)
