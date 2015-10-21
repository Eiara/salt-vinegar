from distutils.core import setup
from vinegar.lib.version import VERSION

setup(name='salt-vinegar',
      version=VERSION,
      description='salt-ssh cli management toolkit',
      author='Aurynn Shaw',
      author_email='aurynn@eiara.nz',
      url='https://github.com/eiara/salt-vinegar/',
      packages=['vinegar'],
      license="GPLv3",
      data_files=[("bin",["vinegar"])]
     )
