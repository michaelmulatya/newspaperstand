from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DateField
from wtforms.fields.html5 import EmailField


class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})


class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Username'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobile'})


class MessageForm(Form):  # Create Message Form
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})


class OrderForm(Form):  # Create Order Form
    name = StringField('Name', [validators.length(min=1)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('Mobile Number', [validators.length(min=10), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    # quantity = SelectField('', [validators.DataRequired()],
    #                        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    email = EmailField('Email', [validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})


class UpdateRegisterForm(Form):
    name = StringField('Full Name', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Mobile', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobile'})


class DeveloperForm(Form):  #
    id = StringField('', [validators.length(min=1)],
                     render_kw={'placeholder': 'Input a product id...'})

class RequestForm(Form):
    category = SelectField('', [validators.DataRequired()],
                           choices=[('magazines', 'Magazines'), ('comics', 'Comics'), ('textbooks', 'Textbooks'), ('newspapers', 'Newspapers')])
    title = StringField('Ebook Name',[validators.DataRequired(),validators.length(min=1)],render_kw={'placeholder':'Ebook Name'})
    pubmonth = DateField('Publication Month & Year', )
    description = TextAreaField('Description (Optional)',[validators.length(min=1)],render_kw={'placeholder':'Description'})

