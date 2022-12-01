from flask_wtf import FlaskForm
import wtforms as ws

from app import app
from app.models import User


class EmployeeForm(FlaskForm):
    fullname = ws.StringField('ФИО', validators=[ws.validators.DataRequired(), ])
    phone = ws.StringField('Номер телефона', validators=[ws.validators.DataRequired(), ])
    short_info = ws.TextAreaField('Краткая информация', validators=[ws.validators.DataRequired(), ])
    experience = ws.IntegerField('Опыт работы', validators=[ws.validators.DataRequired(), ])
    preferred_position = ws.StringField('Предпочитаемая позиция')
    user_id = ws.SelectField('Аккаунт', choices=[])
    # submit = ws.SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = []
        with app.app_context():
            for user in User.query.all():
                self.result.append((user.id, user.username))
        self._fields['user_id'].choices = self.result

    def validate(self):
        if not super().validate():
            return False
        error_counter = 0

        if ' ' not in self.fullname.data:
            self.fullname.errors.append('ФИО должно состоять из 2 и более слов')
            error_counter += 1

        if '+' not in self.phone.data or not self.phone.data[1:].isdigit() or len(
                self.phone.data) != 13:
            self.phone.errors.append('Номер телефона должен начинаться с +,'
                                            ' всего должно быть 13 символов')
            error_counter += 1

        if error_counter > 0:
            return False
        else:
            return True


class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=4, max=20)
    ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8, max=24)
    ])
    submit = ws.SubmitField('Сохранить')




