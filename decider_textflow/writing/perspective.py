# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

INVALID_PERSPECTIVE = {'wir', 'man'}


def invalid_perspective(words) -> list:
    # TODO: REPLACE WITH EXTERNAL METHOD
    words = [word for word in words if isinstance(word, str)]
    words = [word for word in words if word.lower() in INVALID_PERSPECTIVE]
    return words
