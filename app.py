from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import UserForm

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

    def __repr__(self):
        return f'<User:{self.name}>'


@app.route('/userlist')
def user_list():
    user = User.query.all()
    return render_template('userList.html', user=user, title='RM-FORM-Excercise')


@app.route('/', methods=['GET', 'POST'])
def user_define():
    user = User.query.all()
    form = UserForm()
    if form.validate_on_submit():
        names = User(name=form.name.data, email=form.email.data)
        db.session.add(names)
        db.session.commit()
        flash('Submitted')
        return redirect(url_for('user_define'))
    return render_template('index.html', title='ORM-FORM-Excercise', form=form, user=user)

@app.route('/userlist/<int:user_id>/update', methods=['GET','POST'])
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
    return render_template('index.html', title = 'update User',
                           form=form)




@app.route('/userlist/<int:user_id>/delete', methods=['GET', 'POST'])
def user_delete(user_id):
    users = User.query.get_or_404(user_id)
    db.session.delete(users)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('user_list', user_id=users.id))


if __name__ == '__main__':
    app.run()
