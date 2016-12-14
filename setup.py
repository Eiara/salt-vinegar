from distutils.core import setup
from vinegar.lib.version import VERSION

setup(name='salt-vinegar',
      version=VERSION,
      description='salt-ssh cli management toolkit',
      author='Aurynn Shaw',
      author_email='aurynn@eiara.nz',
      url='https://github.com/eiara/salt-vinegar/',
      packages=['vinegar', 
            'vinegar.lib', 
            'vinegar.commands', 
            'vinegar.commands.plugins'],
      license="MIT",
      data_files=[("bin", ["bin/vinegar"])]
     )
