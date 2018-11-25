from distutils.core import setup


setup(
    name='seldon-api',
    version='0.0.1',
    description='Seldon API',
    author='Anton Gladkov',
    author_email='anton.gladkov@gmail.com',
    url='http://github.com/agladkov/seldon-api',
    install_requires=['requests'],
    packages=['seldon', 'seldon.basis']
)
