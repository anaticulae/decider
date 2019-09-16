#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import utila

import detector.cli
from decider import ROOT
from decider import __version__

PROCESS = 'decider'
DESCRIPTION = ''

TITLEPAGE = 'titlepage'

WORKPLAN = [
    utila.create_step(
        TITLEPAGE,
        [
            utila.ResultFile(
                detector.cli.PROCESS,
                f'{detector.cli.TITLEPAGE_STEP}_{detector.cli.TITLEPAGE_OUTPUT}'
            ),
        ],
        ('user', 'developer'),
    )
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='decider.features',
        name=PROCESS,
        description=DESCRIPTION,
        version=__version__,
    )
