from setuptools import setup, find_packages

name = 'tetris'
version = '1.0'
description = 'Terminal tetris game, by BioTet team.'
long_description = """
Enjoy playing nostalgic tetris game in your terminal.
GitHub: emad-mohamadi & danial-fazel
Any issues? Let us know: t.me/emad_mohammadi 
"""
author = "Emad Mohamadi"
author_email = "semadmhmdi@gmail.com"
url = "https://github.com/emad-mohamadi/terminal-tetris"
install_requires = ['keyboard']
entry_points = {
    'console_scripts': [
        'tetris=tetris.main:main',
    ],
}
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    install_requires=install_requires,
    entry_points=entry_points,
)
