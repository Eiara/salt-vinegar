from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))
# from vinegar.lib.version import VERSION

setup(name='salt-vinegar',
      use_incremental=True,
      setup_requires=["incremental"],
      install_requires=["incremental"],
      description='salt-ssh cli management toolkit',
      author='Aurynn Shaw',
      author_email='aurynn@eiara.nz',
      url='https://github.com/eiara/salt-vinegar/',
      packages=['vinegar', 
            'vinegar.lib', 
            'vinegar.commands', 
            'vinegar.commands.plugins'],
      license="MIT",
      # data_files=[("bin", ["bin/vinegar"])]
      entry_points = {
          'console_scripts': ['vinegar=vinegar.command_line:main'],
      }
     )
