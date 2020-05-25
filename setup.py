#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import chdir
from os.path import abspath
from os.path import dirname
from os.path import join
from re import search

from setuptools import setup

ROOT = abspath(dirname(__file__))
UTF8 = 'utf8'

with open(join(ROOT, 'README.md'), mode='rt', encoding=UTF8) as fp:
    README = fp.read()

with open(join(ROOT, 'decider/__init__.py'), mode='rt', encoding=UTF8) as fp:
    VERSION = search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(join(ROOT, "requirements.txt"), mode='rt', encoding=UTF8) as fp:
    INSTALL_REQUIRES = [
        line for line in fp.readlines() if line and '#' not in line
    ]

with open(join(ROOT, "requirements.dev"), mode='rt', encoding=UTF8) as fp:
    REQUIREMENTS_DEV = [
        line for line in fp.readlines() if line and '#' not in line
    ]

if __name__ == "__main__":
    # allow setup.py to run from another directory
    chdir(ROOT)
    setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        description='top or flop',
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        tests_require=REQUIREMENTS_DEV,
        long_description=README,
        name='decider',
        platforms='any',
        url='https://dev.package.checkitweg.de/decider',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'border',
            'border.features',
            'decider',
            'decider.features',
            'decider.utils',
            'decider_footnote',
            'decider_footnote.features',
            'decider_textflow',
            'decider_textflow.features',
            'decider_textflow.quotation',
            'decider_textstyle',
            'decider_textstyle.features',
            'decider_toc',
            'decider_toc.features',
            'fonts',
            'fonts.config',
            'fonts.features',
        ],
        entry_points={
            'console_scripts': [
                'decider = decider.cli:main',
                'decider_border = border.cli:main',
                'decider_fonts = fonts.cli:main',
                'decider_footnote = decider_footnote.cli:main',
                'decider_textflow = decider_textflow.cli:main',
                'decider_textstyle = decider_textstyle.cli:main',
                'decider_toc = decider_toc.cli:main',
            ],
        },
    )
