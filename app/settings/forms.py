from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
from wtforms.validators import DataRequired
from wtforms_alchemy.fields import QuerySelectField, QuerySelectMultipleField


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
        validators=[DataRequired()]
    )


def query_select_multiple_field(field_name):
    return QuerySelectMultipleField(
        field_name,
        get_label='name',
        validators=[DataRequired()]
    )


class PyTenkiForm(FlaskForm):
    region = query_select_field(u'Region')
    prefecture = query_select_field(u'Prefecture')
    subprefecture = query_select_field(u'Subprefecture')
    city = query_select_field(u'City')
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
    category = query_select_field(u'Category')
    company = query_select_field(u'Company')
    region = query_select_field(u'Region')
    line = query_select_multiple_field(u'Line')
    fetch_intvl = IntegerRangeField(u'Data Fetch Interval')
    led_red = gpio_select_field(u'Red')
    led_green = gpio_select_field(u'Green')
    led_blue = gpio_select_field(u'Blue')
    blink_on_time = DecimalRangeField(u'On Time', places=1)
    blink_off_time = DecimalRangeField(u'Off Time', places=1)

    submit = SubmitField('Apply')

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        seen = set()
        result = True
        message = 'Unable to assign GPIO pin more than once at a time'

        for field in [self.led_red, self.led_green,
                      self.led_blue]:
            if field.data in seen:
                field.errors.append(message)
                result = False
            else:
                seen.add(field.data)

        return result
