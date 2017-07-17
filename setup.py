from setuptools import setup

setup(
    name='praline',
    version='0.0.6',
    description='Bitcoin hardware wallet',
    url='https://github.com/zhouer/Praline/',
    author='En-Ran Zhou',
    author_email='zhouer@gmail.com',
    license='MIT',
    packages=["praline"],
    install_requires=['bitcoin', 'leveldb', 'pyserial', 'Pillow', 'RPi.GPIO', 'smbus2', 'Adafruit_SSD1306'],
    entry_points={
        'console_scripts': ['praline=praline.main:main']
    }
)
