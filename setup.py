from setuptools import setup
from toast import __version__

setup(name='toast',
      version=__version__,
      description='A little toasty structure for your pygame peanut butter.',
      url='https://github.com/JoshuaSkelly/Toast',
      author='Joshua Skelton',
      author_email='joshua.skelton@gmail.com',
      license='MIT',
      packages=['toast', 'toast.decorators', 'toast.gui', 'toast.math', 'toast.text_effects'])
