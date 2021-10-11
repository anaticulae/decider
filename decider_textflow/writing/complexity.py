# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

MAX_SENTENCE_COMPLEXITY = 7  # TODO: HOLY VALUE


def too_complex(line: str) -> bool:
    if ':' in line:
        return False
    subsentence = [item for item in line.split(',;') if len(item.split()) > 3]
    if len(subsentence) > MAX_SENTENCE_COMPLEXITY:
        return True
    return False
