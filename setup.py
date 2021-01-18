from setuptools import find_packages
from setuptools import setup

setup(
    name='iot-py',
    version='0.0.1',
    description='IoT web app built with Flask for Raspberry Pi',
    license='MIT',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.1.1',
        'Flask-Login>=0.5.0',
        'Flask-Migrate>=2.5.3',
        'Flask-SQLAlchemy>=2.4.1',
        'Flask-SSE>=0.2.1',
        'Flask-WTF>=0.14.3',
        'gevent>=20.4.0',
        'gunicorn>=20.0.4',
        'pydensha>=1.0.0',
        'pytenki>=1.0.0',
        'python-dotenv>=0.12.0',
        'redis>=3.4.1',
        'simplejson>=3.17.0',
        'tenki-no-ko>=0.0.0',
        'traininfojp>=1.0.0',
        'WTForms-Alchemy>=0.16.9',
    ],
)
