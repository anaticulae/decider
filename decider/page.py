# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider_toc.pages


def validate(footers):
    # TODO: ADD PARSED PDF RAW_LOCATION to `PagesFooterInformation`
    # TODO: REPLACE 1024 afterwards
    pages = [(item.page.value, item.page.raw, 1024) for item in footers]
    validated = decider_toc.pages.validate_pageorder(pages)
    return validated
