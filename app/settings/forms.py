from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


def gpio_pins():
    choices = list()
    choices.append(('', ''))

    for gpio_pin in range(2, 28):
        choice = (str(gpio_pin), 'GPIO{}'.format(str(gpio_pin)))
        choices.append(choice)

    return choices


class PyTenkiForm(FlaskForm):
    led_fine = SelectField(u'Fine', choices=gpio_pins())
    led_cloud = SelectField(u'Cloud', choices=gpio_pins())
    led_rain = SelectField(u'Rain', choices=gpio_pins())
    led_snow = SelectField(u'Snow', choices=gpio_pins())
    tts_button = SelectField(u'Text-to-Speech', choices=gpio_pins())

    submit = SubmitField('Apply')
