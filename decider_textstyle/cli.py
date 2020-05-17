# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_textstyle

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'headlines',
        inputs=[],
        output=('user', 'developer'),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_textstyle.ROOT,
        featurepackage='decider_textstyle.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_textstyle.PROCESS,
            version=decider_textstyle.__version__,
        ),
    )
