from setuptools import setup


dependencies = [
    'yhttp >= 2.5, < 3',
    'redis',
]


setup(
    name='shortener',
    version='0.1',
    description='Url shortener web application',
    long_description=open('README.md').read(),
    install_requires=dependencies,
    py_modules=['shortener'],
    entry_points=dict(console_scripts='shortener=shortener:app.climain'),
    license='MIT',
)
