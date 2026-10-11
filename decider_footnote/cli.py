#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import protoerror
import utilo

import decider_footnote

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'global',
        [
            utilo.ResultFile('footnote', 'result_result'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'rules',
        [
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'horizontals_horizontals'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'style',
        [
            utilo.ResultFile('footnote', 'result_result'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
        ],
        protoerror.ResultDefault,
    ),
]


def main():
    root, features = decider_footnote.ROOT, 'decider_footnote.features'
    hook = protoerror.integrate(root=root, features=features)
    utilo.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utilo.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_footnote.PROCESS,
            pages=True,
            version=decider_footnote.__version__,
        ),
    )
