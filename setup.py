from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in migoo_crm/__init__.py
from migoo_crm import __version__ as version

setup(
	name="migoo_crm",
	version=version,
	description="MIGOO",
	author="Palak Padalia",
	author_email="padaliapalak19@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
