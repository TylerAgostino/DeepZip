from setuptools import setup

setup(
    name='example',
    version='0.1.0',
    py_modules=['example'],
    entry_points='''
        [console_scripts]
        example=example:example
    ''',
)