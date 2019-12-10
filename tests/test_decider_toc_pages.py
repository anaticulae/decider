# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider.toc.pages as dtp
import tests
import tests.resources


def test_toc_pages_validate():
    toc = tests.tableofcontent(tests.resources.TECHNICAL_24PAGES_GENERATED) # yapf:disable

    validated = dtp.validate(toc)
