#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import decider_footnote

DESCRIPTION = ''

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        'global',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'rules',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'style',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
        ],
        (USER, DEVELOPER),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_footnote.ROOT,
        featurepackage='decider_footnote.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_footnote.PROCESS,
            version=decider_footnote.__version__,
        ),
    )
