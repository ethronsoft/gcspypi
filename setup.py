from setuptools import setup

setup(
	name='gcspypi',
	version='1.0.1',
	author='Ethronsoft',
	author_email='dev@ethronsoft.com',
	license=open("LICENSE").read(),
	keywords="pypi private repository gcs google cloud storage",
	url="https://github.com/ethronsoft/gcspypi",
	description="Private packages repository backed by Google Cloud Storage",
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
