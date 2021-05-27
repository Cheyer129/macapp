from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path

# Creating Path
CurrentDirectory = Path.cwd()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# start up python "python(3)" in terminal
# creating the db
# from app import db
# db.create_all()

class Payoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower = db.Column(db.String(25), nullable=False)
    loan_number = db.Column(db.String(10), nullable=True)
    heloc_number = db.Column(db.String(10), nullable=True)
    loan_type = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.today())
    contact = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=True)
    residents = db.Column(db.String(50), nullable=False)
    street_address = db.Column(db.String(50), nullable=False)
    city_state_zip = db.Column(db.String(50), nullable=False)
    documents_received = db.Column(db.DateTime, nullable=True)
    new_lender_info = db.Column(db.Boolean, nullable=True)
    closing_date = db.Column(db.String(15), nullable=True)
    funding_date = db.Column(db.String(15), nullable=True)
    cancel_date = db.Column(db.String(15), nullable=True)
    fedex_no = db.Column(db.String(14), nullable=True)
    file_comment = db.Column(db.String(120), nullable=True)

    # A function telling us how old the file is
    # def days_old(self):



    def __repr__(self):
        return '<Payoff %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f_borrower = request.form['borrower']
        f_loan_number = request.form['loan_number']
        f_loan_type = request.form['loan_type']
        f_contact = request.form['contact']
        f_contact_email = request.form['contact_email']
        f_phone_number = request.form['phone_number']
        f_residents = request.form['residents']
        f_street_address = request.form['street_address']
        f_city_state_zip = request.form['city_state_zip']
        new_file = Payoff(borrower=f_borrower, loan_number=f_loan_number,
                        loan_type=f_loan_type, contact=f_contact, contact_email=f_contact_email, 
                        phone_number=f_phone_number, residents=f_residents,
                        street_address=f_street_address, city_state_zip=f_city_state_zip)

        try:
            db.session.add(new_file)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your payoff'

    else:
        payoffs = Payoff.query.order_by(Payoff.date_created).all()
        return render_template('index.html', payoffs=payoffs)


# Delete
@app.route('/delete/<int:id>')
def delete(id):
    payoff_to_delete = Payoff.query.get_or_404(id)

    try:
        db.session.delete(payoff_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that payoff'


# Update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    payoff = Payoff.query.get_or_404(id)

    if request.method == 'POST':
        payoff.borrower = request.form['borrower']
        payoff.loan_number = request.form['loan_number']
        payoff.heloc_number = request.form['heloc_number']
        payoff.contact = request.form['contact']
        payoff.contact_email = request.form['contact_email']
        payoff.phone_number = request.form['phone_number']
        payoff.residents = request.form['residents']
        payoff.street_address = request.form['street_address']
        payoff.city_state_zip = request.form['city_state_zip']
        payoff.loan_type = request.form['loan_type']
        payoff.closing_date = request.form['closing_date']
        payoff.funding_date = request.form['funding_date']
        payoff.cancel_date = request.form['cancel_date']
        payoff.fedex_no = request.form['fedex_no']
        payoff.file_comment = request.form['comment']
        if request.form['docs_received'] == 'on':
            payoff.documents_received = datetime.today()
        if request.form['new_lender_info'] == 'on':
            payoff.new_lender_info == True
        try:
            print(request.form['docs_received'])
        except:
            print('could not print')
        try:
            print(request.form['new_lender_info'])
        except:
            print('could not print')



        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your payoff'

    else:
        return render_template('update.html', payoff=payoff)


if __name__ == "__main__":
    app.run(debug=True)