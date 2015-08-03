from setuptools import setup, find_packages


setup(
    name='nete',
    version='0.1',
    author='Frank Ploss',
    author_email='nete@fqxp.de',
    license='GPL',
    url='https://github.com/fqxp/nete-qt',
    scripts=[
        'scripts/nete-cli',
        'scripts/nete-qt',
    ],
    packages=find_packages(),
    package_data={
        'nete.qtgui': [
            'qml/*.qml',
            'qml/controls/*.qml',
        ],
    },
)
