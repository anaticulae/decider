#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from decider import ROOT
from decider import __version__

PROCESS = 'decider_border'

FEATURE_NAME = 'detection'
DESCRIPTION = 'determine overlapping content'

# pylint:disable=C0103
ResultFile = lambda producer, name: RF(producer=producer, name=name)

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile('rawmaker', 'border_boundingboxes'),
            ResultFile('rawmaker', 'border_pages'),
        ],
        ('hits', 'user', 'developer'),
    )
]


def main():
    featurepack(
        description=DESCRIPTION,
        featurepackage='border.features',
        name=PROCESS,
        pages=True,
        root=ROOT,
        version=__version__,
        workplan=WORKPLAN,
    )
