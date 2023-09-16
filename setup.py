from setuptools import setup, find_packages

setup(
    name='yokai',
    version='2.0.0',
    author='Jacob Moore',
    description='An automation framework with special python syntax extension and preprocessor',
    url='https://github.com/moorejacob2017/Yokai',
    packages=find_packages(),
    keywords="yokai automation automate",
    license='GPLv3',
    install_requires=[
        "python-dateutil",
        "pytz>=2020.1",
    ],
    entry_points={
        'console_scripts': [
            'yokai=yokai.cli:main',
        ],
    },
)

