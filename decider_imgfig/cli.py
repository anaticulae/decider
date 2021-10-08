# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_imgfig

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'quality',
        [
            utila.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'position',
        [
            utila.Pattern('rawmaker__border_pages', 'yaml'),
            utila.ResultFile('sections', 'docinfo_docinfo'),
            utila.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        protocol.ResultDefault,
    ),
]


def main():
    root, features = decider_imgfig.ROOT, 'decider_imgfig.features'
    hook = protocol.integrate(root=root, features=features)
    utila.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            pages=True,
            name=decider_imgfig.PROCESS,
            version=decider_imgfig.__version__,
        ),
    )
