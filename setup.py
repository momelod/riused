from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='riused',
    version='0.1.0',
    description='Commandline aws reserved instance counter',
    long_description=readme,
    author='David Cabral',
    author_email='david.cabral@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'riused=riused.riused:main',
        ],
    },
)
