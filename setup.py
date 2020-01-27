from setuptools import setup


dependencies = [
    'yhttp',
    'redis',
    'hashids'
]


setup(
    name='shortener',
    version='0.1',
    description='Url shortener web application',
    long_description=open('README.md').read(),
    install_requires=dependencies,
    py_modules=['shortener'],
    license='MIT'
)
