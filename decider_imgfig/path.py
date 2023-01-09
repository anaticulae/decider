# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def quality(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'decider_imgfig', 'quality_user', prefix)


def position(path: str, prefix: str = '') -> str:
    return utila.pathconnector(path, 'decider_imgfig', 'position_user', prefix)
