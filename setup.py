from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys, os

version = '0.1'

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--cov-report', 'term-missing', '--cov', 'flattr',
            '--doctest-modules', 'flattr']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='flattr',
      version=version,
      description="Implementation of a python client for the flattr restful api",
      long_description="""\
""",
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          ],
      keywords='flattr',
      author='Christoph Glaubitz',
      author_email='chris@chrigl.de',
      url='https://github.com/chrigl/python-flattr',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest', 'pytest-cov'],
      cmdclass = {'test': PyTest},
      install_requires=[
          # -*- Extra requirements: -*-
          'six',
          'requests',
          'simplejson',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
