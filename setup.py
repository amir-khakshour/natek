from setuptools import setup, find_packages

setup(name="nanotek", packages=find_packages())

test_requires = [
    'WebTest==2.0.34',
    'coverage>=5.0,<5.1',
    'django-webtest>=1.9,<1.10',
    'psycopg2-binary>=2.8,<2.9',
    'pytest-django==3.8.0',
    'pytest-xdist>=1.31,<1.32',
    'tox>=3.14,<3.15',
    'freezegun>=0.3,<0.4',
]
