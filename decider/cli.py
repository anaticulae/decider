#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import detector
import detector.cli
import groupme
import groupme.cli
import utila

import decider

DESCRIPTION = ''

TITLEPAGE = 'titlepage'
TOC = 'toc'
FOOTNOTE = 'footnote'

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        FOOTNOTE,
        [
            utila.ResultFile(groupme.PROCESS, 'footer_footerheader'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        TITLEPAGE,
        [
            utila.ResultFile(
                detector.PROCESS,
                f'{detector.cli.TITLEPAGE_STEP}_{detector.cli.TITLEPAGE_OUTPUT}'
            ),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        TOC,
        [
            utila.ResultFile(groupme.PROCESS, 'toc_toc'),
        ],
        (USER, DEVELOPER),
    )
]

USER_LINT_OUTPUT = f'{decider.PROCESS}__{TITLEPAGE}_{USER}.yaml'
DEVELOPER_LINT_OUTPUT = f'{decider.PROCESS}__{TITLEPAGE}_{DEVELOPER}.yaml'


def main():
    utila.featurepack(
        description=DESCRIPTION,
        featurepackage='decider.features',
        name=decider.PROCESS,
        root=decider.ROOT,
        version=decider.__version__,
        workplan=WORKPLAN,
        multiprocessed=True,
    )
