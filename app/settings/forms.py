from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


def gpio_pins():
    choices = list()
    choices.append(('', ''))

    for gpio_pin in range(2, 28):
        choice = (str(gpio_pin), 'GPIO{}'.format(str(gpio_pin)))
        choices.append(choice)

    return choices


def gpio_select_field(field_name):
    return SelectField(
        field_name,
        choices=gpio_pins(),
        validators=[DataRequired()]
    )


class PyTenkiForm(FlaskForm):
    led_fine = gpio_select_field(u'Fine')
    led_cloud = gpio_select_field(u'Cloud')
    led_rain = gpio_select_field(u'Rain')
    led_snow = gpio_select_field(u'Snow')
    tts_button = gpio_select_field(u'Text-to-Speech')

    submit = SubmitField('Apply')
