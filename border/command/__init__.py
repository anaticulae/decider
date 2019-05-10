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

from border.features.detection import work
from decider import ROOT
from decider import __version__
from decider.feature import HOOK
from decider.feature import INPUT
from decider.feature import NAME
from decider.feature import OUTPUT
from decider.feature import create_step
from decider.feature import featurepack

PROCESS_NAME = 'decider_border'

FEATURE_NAME = 'hitthebox'
DESCRIPTION = 'determine overlapping cotent'

WORKPLAN = [
    create_step(
        FEATURE_NAME,
        work,
        [
            ('rawmaker', 'border_boxes'),
            ('rawmaker', 'border_pages'),
        ],
        ('hits',),
    )
]
FEATURE_PATH = join(ROOT, 'border/features')


def main():
    featurepack(
        workplan=WORKPLAN,
        feature_path=FEATURE_PATH,
        feature_package='border.features',
        name=NAME,
        description=DESCRIPTION,
        version=__version__,
    )
