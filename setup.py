from setuptools import setup, find_packages


setup(
    name='nete',
    version='0.1',
    author='Frank Ploss',
    author_email='nete@fqxp.de',
    license='GPL',
    url='https://github.com/fqxp/nete-qt',
    packages=find_packages(),
    package_data={
        'nete.qtgui': [
            'qml/*.qml',
            'qml/controls/*.qml',
        ],
    },
    entry_points={
        'gui_scripts': [
            'nete-qt = nete.qtgui.application:main',
        ],
        'console_scripts': [
            'nete-cli = nete.cli.main:main',
        ],
    },
)
