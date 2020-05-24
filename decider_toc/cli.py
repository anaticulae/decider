# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_toc

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'toc',
        [
            utila.ResultFile('groupme', 'toc_toc'),
        ],
        ('user', 'developer'),
    )
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_toc.ROOT,
        featurepackage='decider_toc.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            pages=True,
            name=decider_toc.PROCESS,
            version=decider_toc.__version__,
        ),
    )
