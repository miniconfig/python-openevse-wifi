from setuptools import setup
setup(
  name = 'openevsewifi',
  packages = ['openevsewifi'],
  version = '0.1',
  description = 'A python library for communicating with the ESP8266-based wifi module from OpenEVSE',
  author = 'Michelle Avery',
  author_email = 'dev@miniconfig.com',
  url = 'https://github.com/miniconfig/python-openevse-wifi',
  download_url = 'https://github.com/miniconfig/python-openevse-wifi/tarball/0.1',
  install_requires='urllib'
)
