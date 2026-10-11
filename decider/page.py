# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elementae


def validate(footers):
    # TODO: ADD PARSED PDF RAW_LOCATION to `PagesFooterInformation`
    # TODO: REPLACE 1024 afterwards
    # skip footer without page number
    pages = [
        (item.page.value, item.page.raw, 1024) for item in footers if item.page
    ]
    validated = elementae.validate_pageorder(pages)
    return validated
