from app.models import Setting


def test_load_setting(client):
    setting = Setting.load_setting('gpio')

    assert setting['weather']['led']['fine'] == '2'
    assert setting['weather']['tts_button'] == '4'


def test_update_setting(client):
    new_value = {'weather': {'tts_button': '5'}}

    Setting.update_setting('gpio', new_value)
    assert Setting.load_setting('gpio') == new_value
