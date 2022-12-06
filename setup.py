from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='tiniworld_core',
      version="0.0.5",
      description="A Time-Series Forecasting Project with Facebook Prophet",
      packages=find_packages(),
      install_requires=requirements,
      #test_suite='tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      #scripts=['scripts/tiniworld_core-run'],
      zip_safe=False)
