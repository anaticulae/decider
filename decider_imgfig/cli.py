# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import decider_imgfig

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'quality',
        [
            utilo.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'position',
        [
            utilo.Pattern('rawmaker__border_pages', 'yaml'),
            utilo.ResultFile('sections', 'docinfo_docinfo'),
            utilo.Pattern('rawmaker__images_images/*', 'yaml'),
        ],
        protoerror.ResultDefault,
    ),
]


def main():
    root, features = decider_imgfig.ROOT, 'decider_imgfig.features'
    hook = protoerror.integrate(root=root, features=features)
    utilo.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            pages=True,
            name=decider_imgfig.PROCESS,
            version=decider_imgfig.__version__,
        ),
    )
