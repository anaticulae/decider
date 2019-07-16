#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from decider import ROOT
from decider import __version__

PROCESS_NAME = 'decider_border'

FEATURE_NAME = 'hitthebox'
DESCRIPTION = 'determine overlapping content'

ResultFile = lambda producer, name: RF(producer=producer, name=name)

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile('rawmaker', 'border_boxes'),
            ResultFile('rawmaker', 'border_pages'),
        ],
        ('hits',),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='border.features',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
