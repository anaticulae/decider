#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from os.path import join

from utila import SUCCESS
from utila import create_parser
from utila import parse
from utila import saveme
from utila import sources

from decider import ROOT
from decider import __version__
from decider.feature import create_step
from decider.feature import featurepack
from fonts.features.ugly import work

PROCESS_NAME = 'decider_fonts'

FEATURE_NAME = 'iamugly'
DESCRIPTION = 'determine ugly fonts'

WORKPLAN = [
    create_step(
        FEATURE_NAME,
        work,
        [
            ('decider_fonts', 'ugly_fonts'),
            ('rawmaker', 'fonts_header'),
            ('rawmaker', 'fonts_content'),
        ],
        ('ugly',),
    )
]
FEATURE_PATH = join(ROOT, 'fonts/features')


def main():
    featurepack(
        workplan=WORKPLAN,
        feature_path=FEATURE_PATH,
        feature_package='fonts.features',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
