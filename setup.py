from setuptools import find_packages, setup

setup(
	name="expense_tracker",
	version="0.0.1",
	description="Simple Daily Expense Tracking Application",
	author="Your Company",
	author_email="support@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	python_requires=">=3.10,<3.12",
	install_requires=[
		"frappe>=15.0.0,<16.0.0"
	]
)
