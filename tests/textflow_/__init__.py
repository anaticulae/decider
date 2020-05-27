# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila

import decider_textflow.cli

# pylint:disable=C0103
run = functools.partial(
    utila.run_command,
    main=decider_textflow.cli.main,
    process=decider_textflow.PROCESS,
    success=True,
)
fail = functools.partial(
    utila.run_command,
    main=decider_textflow.cli.main,
    process=decider_textflow.PROCESS,
    success=False,
)


def run_textflow(
        source,
        pages,
        lineending: bool = False,
        quotation: bool = False,
):
    actions = ''
    if lineending:
        actions += ' --lineending'
    if quotation:
        actions += ' --quotation'
    utila.run(f'textflow -i={source}  --pages={pages} {actions}')
