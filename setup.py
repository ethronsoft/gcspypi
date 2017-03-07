from setuptools import setup

setup(
	name='gcspypi',
	version='0.1.0',
	packages=['gcspypi'],
	install_requires=[
		"google-cloud"
	],
	entry_points={
		'console_scripts': [
			'gcspypi = gcspypi.__main__:main'
		]
	}
)