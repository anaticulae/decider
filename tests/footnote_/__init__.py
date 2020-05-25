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

import decider_footnote.cli

# pylint:disable=C0103
run = functools.partial(
    utila.run_command,
    main=decider_footnote.cli.main,
    process=decider_footnote.PROCESS,
    success=True,
)
fail = functools.partial(
    utila.run_command,
    main=decider_footnote.cli.main,
    process=decider_footnote.PROCESS,
    success=False,
)
