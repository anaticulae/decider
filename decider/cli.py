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

import decider

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'color',
        [
            utilo.ResultFile('colors', 'statistics_statistics'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'header',
        [
            utilo.ResultFile('headnote', 'result_result'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'links',
        [
            utilo.ResultFile('weblink', 'biblio_biblio'),
            utilo.ResultFile('weblink', 'footer_footer'),
            utilo.ResultFile('weblink', 'sentence_sentence'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'page',
        [
            utilo.ResultFile('groupme', 'footer_footerheader'),
            utilo.ResultFile('sections', 'section_result'),
            utilo.ResultFile('pagenumber', 'result_result'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'titlepage',
        [
            utilo.ResultFile('detector', 'titlepage_detected'),
        ],
        protoerror.ResultDefault,
    ),
]

USER_LINT_OUTPUT = f'{decider.PROCESS}__titlepage_user.yaml'
DEVELOPER_LINT_OUTPUT = f'{decider.PROCESS}__titlepage_developer.yaml'


def main():
    hook = protoerror.integrate(root=decider.ROOT, features='decider.features')
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider.ROOT,
        featurepackage='decider.features',
        config=utilo.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider.PROCESS,
            pages=True,
            version=decider.__version__,
        ),
    )
