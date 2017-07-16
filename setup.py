from setuptools import setup

setup(
    name='praline',
    version='0.0.5',
    description='Bitcoin hardware wallet',
    url='https://github.com/zhouer/Praline/',
    author='En-Ran Zhou',
    author_email='zhouer@gmail.com',
    license='MIT',
    packages=["praline"],
    install_requires=['bitcoin', 'leveldb', 'pyserial', 'Pillow', 'RPi.GPIO', 'Adafruit_SSD1306'],
    entry_points={
        'console_scripts': ['praline=praline.main:main']
    }
)
