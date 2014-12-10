import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['babel', 'biryani', 'pymongo', 'pyramid', 'suq-monpyjama']

setup(name='open-chord-charts',
      version='0.0',
      description='open-chord-charts',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Christophe Benz',
      author_email='christophe.benz@gmail.com',
      url='http://www.openchordcharts.org/',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="openchordcharts",
      entry_points = """\
      [paste.app_factory]
      main = openchordcharts:main
      """,
      paster_plugins=['pyramid'],
      )

