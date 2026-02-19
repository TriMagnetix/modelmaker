from setuptools import setup, find_packages

setup(
	name='modelmaker',
	version='1.0.0',
	description='A library for creating small and precise 3d models',
	url='https://github.com/trimagnetix/modelmaker',
	author='Madison Hanberry',
	author_email='madison@trimagnetix.com',
	license='GPL-3.0-or-later',
	packages=find_packages(),
	test_suite='tests',
	install_requires=[
		'raylib',
		'scipy',
	],
	extras_require={
		'test': [
			'pytest',
			'flake8-tabs',
			'black-with-tabs',
		],
	},
	classifiers=[
		'Intended Audience :: Science/Research',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
		'Programming Language :: Python :: 3',
	],
)
