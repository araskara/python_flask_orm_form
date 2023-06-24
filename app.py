from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import UserForm, UserAddress

app = Flask(__name__)
app.config['SECRET_KEY'] = '83C551DCFC2BAB5671487DADAF8CB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Not registered')
    addresses = db.relationship('Address', backref='user')

    def __repr__(self):
        return f'<User:{self.name}>'


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50))
    street = db.Column(db.String(100))
    zip_code = db.Column(db.String(50))
    city = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<User:{self.name}>'


@app.route('/userlist')
def user_list():
    users = User.query.all()
    return render_template('userList.html', users=users, title='RM-FORM-Excercise')


@app.route('/', methods=['GET', 'POST'])
def user_define():
    users = User.query.all()
    form = UserForm()
    if form.validate_on_submit():
        names = User(name=form.name.data, email=form.email.data)
        db.session.add(names)
        db.session.commit()
        flash('Submitted')
        return redirect(url_for('user_define'))
    return render_template('index.html', title='ORM-FORM-Excercise', form=form, users=users)


@app.route('/userlist/<int:user_id>/update', methods=['GET', 'POST'])
def update_user(user_id):
    users = User.query.get_or_404(user_id)
    form = UserForm()
    if form.validate_on_submit():
        users.name = form.name.data
        users.email = form.email.data
        db.session.commit()
        flash('User has been updated')
        return redirect(url_for('user_list'))
    elif request.method == 'GET':
        form.name.data = users.name
        form.email.data = users.email
    return render_template('index.html', title='update User',
                           form=form)


@app.route('/userlist/<int:user_id>/delete', methods=['GET', 'POST'])
def user_delete(user_id):
    users = User.query.get_or_404(user_id)
    db.session.delete(users)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('user_list', user_id=users.id))


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    address = Address.query.filter_by(user_id=user.id).all()

    return render_template('user_page.html', user=user, address=address, title='User Page')


@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    form = UserAddress()
    form.user.choices = [(user.id, user.name) for user in User.query.all()]
    if form.validate_on_submit():
        address = Address(user_id=form.user.data, number=form.number.data,
                          street=form.street.data, zip_code=form.zip_code.data,
                          city=form.city.data)
        db.session.add(address)
        db.session.commit()
        flash('Address has been created!')
        return redirect(url_for('add_address'))
    return render_template('add_address.html', title='create Address', form=form)


@app.route('/update_status/<int:user_id>', methods=['POST'])
def user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.status = request.form.get('status')  # directly get status from form data
    db.session.commit()
    return redirect(url_for('user_list'))


if __name__ == '__main__':
    app.run()
