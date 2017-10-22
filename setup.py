from setuptools import setup

setup(
	name='gcspypi',
	version='1.0.3',
	author='Ethronsoft',
	author_email='dev@ethronsoft.com',
	license=open("LICENSE").read(),
	keywords="pypi private repository gcs google cloud storage",
	url="https://github.com/ethronsoft/gcspypi",
	description="Private packages repository backed by Google Cloud Storage",
	packages=['ethronsoft','ethronsoft.gcspypi'],
	install_requires=[
		"google-cloud-storage==1.5.0"
	],
	entry_points={
		'console_scripts': [
			'gcspypi = ethronsoft.gcspypi.__main__:main'
		]
	}
)
