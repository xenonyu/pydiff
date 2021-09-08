from setuptools import setup

#APP would be the name of the file your code is in.
APP = ['OmapDiff.py']
DATA_FILES = []
#The Magic is in OPTIONS.
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'logo.icns', #change app.icns to the image file name!!!
    }

setup(
    app=APP,
    name='OmapDiff', #change to anything
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)