from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='VimTube',
    version='0.1a',
    description='A ncurses-based YouTube client with Vim key bindings written in Python',
    url='http://github.com/LelouchLamperougeVI/vimtube',
    author='HaoRan Chang',
    author_email='haoran.chang@mail.mcgill.ca',
    license='GPLv3',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'pafy',
        'youtube-dl',
        'python-vlc',
    ],
    long_description=long_description,
    long_description_centent_type='text/markdown',
)
