#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.md'), encoding='utf8') as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'decider/__init__.py'), encoding='utf8') as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), encoding='utf8') as fp:
    REQUIRES = [line for line in fp.readlines() if line and '#' not in line]

if __name__ == "__main__":
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        description='top or flop',
        include_package_data=True,
        install_requires=REQUIRES,
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
            'decider',
            'decider.features',
            'decider.links',
            'decider.utils',
            'decider_footnote',
            'decider_footnote.features',
            'decider_footnote.rules',
            'decider_imgfig',
            'decider_imgfig.features',
            'decider_smarty',
            'decider_smarty.features',
            'decider_textflow',
            'decider_textflow.features',
            'fonts',
            'fonts.features',
        ],
        entry_points={
            'console_scripts': [
                'decider = decider.cli:main',
                'decider_fonts = fonts.cli:main',
                'decider_footnote = decider_footnote.cli:main',
                'decider_imgfig = decider_imgfig.cli:main',
                'decider_smarty = decider_smarty.cli:main',
                'decider_textflow = decider_textflow.cli:main',
            ],
        },
    )
