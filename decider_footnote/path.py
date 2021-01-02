# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_footnote


def global_(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_footnote.PROCESS,
        'global_user',
        prefix,
    )


def rules(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_footnote.PROCESS,
        'rules_user',
        prefix,
    )


def style(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_footnote.PROCESS,
        'style_user',
        prefix,
    )
