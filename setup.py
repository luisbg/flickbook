#!/usr/bin/python

from distutils.core import setup

setup(name="Flickbook",
      version="0.1",
      author="Luis de Bethencourt",
      author_email="luis@debethencourt.com",
      license = "GPL v2",
      package_dir = {'':'src'},
      packages = "flickbook",
      scripts = ["src/flickbook", "src/flickbook-old"],
      data_files = [("src/gui.glade", "files/")]
      )
