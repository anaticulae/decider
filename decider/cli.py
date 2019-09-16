#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import utila

import decider
import detector.cli

PROCESS = 'decider'
DESCRIPTION = ''

TITLEPAGE = 'titlepage'

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        TITLEPAGE,
        [
            utila.ResultFile(
                detector.cli.PROCESS,
                f'{detector.cli.TITLEPAGE_STEP}_{detector.cli.TITLEPAGE_OUTPUT}'
            ),
        ],
        (USER, DEVELOPER),
    )
]

USER_LINT_OUTPUT = f'{PROCESS}__{TITLEPAGE}_{USER}.yaml'
DEVELOPER_LINT_OUTPUT = f'{PROCESS}__{TITLEPAGE}_{DEVELOPER}.yaml'


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider.ROOT,
        featurepackage='decider.features',
        name=PROCESS,
        description=DESCRIPTION,
        version=decider.__version__,
    )
