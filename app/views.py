from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db, app
from .models import Employee, User
from .forms import EmployeeForm, UserForm


def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@login_required
def employee_create():
    form = EmployeeForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('Работник успешно сохранен', 'success')
            return redirect(url_for('index'))
    return render_template('employee_create.html', form=form)


def employee_detail(id):
    employee = Employee.query.get(id)
    return render_template('employee_detail.html', employee=employee)


@login_required
def employee_delete(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('employee_delete.html', employee=employee)


@login_required
def employee_update(id):
    employee = Employee.query.get(id)
    form = EmployeeForm(request.form, obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('employee_update.html', form=form, employee=employee)


def register():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            flash(f'Пользователь {user.username} успешно зарегистрирован!', 'primary')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


def login():
    logout_user()
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                flash('Успешно авторизован!', 'primary')
                return redirect(url_for('index'))
            else:
                flash('Неправильно введенные данные', 'danger')
    return render_template('login.html', form=form)


def logout():
    logout_user()
    return redirect(url_for('login'))
