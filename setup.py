from distutils.core import setup
setup(
  name = 'python-openevse-wifi',
  packages = ['python-openevse-wifi'],
  version = '0.1',
  description = 'A python library for communicating with the ESP8266-based wifi module from OpenEVSE',
  author = 'Michelle Avery',
  author_email = 'dev@miniconfig.com',
  url = 'https://github.com/miniconfig/python-openevse-wifi',
  download_url = 'https://github.com/miniconfig/python-openevse-wifi/tarball/0.1',
  install_requires=['urllib']
)
