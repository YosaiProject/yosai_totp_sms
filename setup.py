import os
from setuptools import setup, find_packages, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info; py.cleanup -d')


here = os.path.abspath(os.path.dirname(__file__))

requires = ['yosai',
            'twilio']

setup(name='yosai_totp_sms',
      version='0.1.1',
      description='Yosai Time-Based One Time Password (TOTP) Token SMS Messaging',
      long_description='Yosai Time-Based One Time Password (TOTP) Token SMS Messaging',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='yosai security authentication otp totp',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      cmdclass={'clean': CleanCommand}
      )
