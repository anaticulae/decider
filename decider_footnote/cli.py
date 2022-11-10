#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import protocol
import utila

import decider_footnote

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'global',
        [
            utila.ResultFile('footnote', 'result_result'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'rules',
        [
            utila.ResultFile('footnote', 'result_result'),
            utila.ResultFile('rawmaker', 'horizontals_horizontals'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'style',
        [
            utila.ResultFile('footnote', 'result_result'),
            utila.ResultFile('rawmaker', 'fonts_header'),
            utila.ResultFile('rawmaker', 'fonts_content'),
        ],
        protocol.ResultDefault,
    ),
]


def main():
    root, features = decider_footnote.ROOT, 'decider_footnote.features'
    hook = protocol.integrate(root=root, features=features)
    utila.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utila.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_footnote.PROCESS,
            pages=True,
            version=decider_footnote.__version__,
        ),
    )
