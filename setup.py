import os
from setuptools import setup


def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    return open(filepath, 'r').read()

setup(
    name='ao2pyv',
    version='0.0.1a',
    url='XXX',
    license='BSD',
    description=(
        'Converts Archive.org video searches into PyVideo.org API'
        ' submissions.'
    ),
    long_description=read_file('README.rst'),
    author='Simon Cross',
    author_email='hodgestar@gmail.com',
    modules=[
        'ao2pyv',
    ],
    install_requires=[
        'requests',
        'click',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
