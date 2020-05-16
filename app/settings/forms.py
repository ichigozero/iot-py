from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
from wtforms.validators import DataRequired
from wtforms_alchemy.fields import QuerySelectField


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


def query_select_field(field_name):
    return QuerySelectField(
        field_name,
        get_label='name',
        allow_blank=True,
        validators=[DataRequired()]
    )


class PyTenkiForm(FlaskForm):
    region = query_select_field(u'Region')
    prefecture = query_select_field(u'Prefecture')
    city = query_select_field(u'City')
    pinpoint_loc = query_select_field(u'Pinpoint Location')
    fetch_intvl = IntegerRangeField(u'Data Fetch Interval')
    blink_on_time = DecimalRangeField(u'On Time', places=1)
    blink_off_time = DecimalRangeField(u'Off Time', places=1)
    fade_in_time = DecimalRangeField(u'Fade In Time', places=1)
    fade_out_time = DecimalRangeField(u'Fade Out Time', places=1)
    led_fine = gpio_select_field(u'Fine')
    led_cloud = gpio_select_field(u'Cloud')
    led_rain = gpio_select_field(u'Rain')
    led_snow = gpio_select_field(u'Snow')
    tts_button = gpio_select_field(u'Text-to-Speech')

    submit = SubmitField('Apply')

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        seen = set()
        result = True
        message = 'Unable to assign GPIO pin more than once at a time'

        for field in [self.led_fine, self.led_cloud,
                      self.led_rain, self.led_snow,
                      self.tts_button]:
            if field.data in seen:
                field.errors.append(message)
                result = False
            else:
                seen.add(field.data)

        return result


class PyDenshaForm(FlaskForm):
    led_normal = SelectField(u'Normal', choices=gpio_pins())
    led_delayed = SelectField(u'Delayed', choices=gpio_pins())
    led_other = SelectField(u'Other ', choices=gpio_pins())

    submit = SubmitField('Apply')
