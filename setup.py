from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
#    'iconfile': 'icon.icns',  # Optional – nur wenn du ein Icon hast
    'packages': [
        'PIL',
        'cv2',
        'imagehash',
        'filetype',
        'tkinter'
    ],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

