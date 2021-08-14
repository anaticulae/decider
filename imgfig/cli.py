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

import imgfig

DESCRIPTION = ''

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        'quality',
        [
            utila.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'position',
        [
            utila.Pattern('rawmaker__border_pages', 'yaml'),
            utila.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        (USER, DEVELOPER),
    ),
]


def main():
    root, features = imgfig.ROOT, 'imgfig.features'
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
            name=imgfig.PROCESS,
            version=imgfig.__version__,
        ),
    )
