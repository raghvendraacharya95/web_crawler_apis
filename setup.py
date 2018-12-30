from setuptools import setup, find_packages
setup(
	name='Rest APIs For A Web Crawler',
	version='1.0',
	author='Raghevndra Acharya',
	install_requires=[
					"requests"
					,"Flask"
                    ,"flask-restful"
					,"flask-cors"
					,"flask-restplus"
					,"bs4"
					],
	packages = find_packages()
    )
