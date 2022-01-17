#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
from utila import ResultFile as RF
from utila import create_step as step
from utila import featurepack

from decider import ROOT
from decider import __version__

PROCESS = 'decider_fonts'
FEATURE_NAME = 'ugly'
DESCRIPTION = 'determine ugly fonts'

# pylint:disable=C0103
ResultFile = lambda producer, name: RF(producer=producer, name=name)

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile('decider_fonts_config', 'ugly_fonts'),
            ResultFile('rawmaker', 'fonts_header'),
            ResultFile('rawmaker', 'fonts_content'),
        ],
        ('ugly',),
    )
]

UGLY_STEP_OUTPUT_FILE = f'{PROCESS}__{FEATURE_NAME}_ugly.yaml'


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='fonts.features',
        config=utila.FeaturePackConfig(
            name=PROCESS,
            description=DESCRIPTION,
            version=__version__,
        ),
    )
