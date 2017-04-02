from setuptools import setup

setup(
	name='gcspypi',
	version='0.1.0',
	packages=['ethronsoft','ethronsoft.gcspypi'],
	namespace_packages = ['ethronsoft'],
	install_requires=[
		"google-cloud"
	],
	entry_points={
		'console_scripts': [
			'gcspypi = ethronsoft.gcspypi.__main__:main'
		]
	}
)