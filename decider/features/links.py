# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Decider Links
=============

10500: date of hyperlink access
"""

import typing

import iamraw
import protocol
import serializeraw


def work(links: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)
    # load data
    hyperlinks = serializeraw.load_hyperlinks(links, pages=pages)  # pylint:disable=E1101
    driver = protocol.driver(hyperlinks=hyperlinks)

    # run linter
    linter.run(driver=driver)

    # write result
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_10500 = """\
Aufrufdatum fehlt

Für den Hyperlink **{{link.href}}** ist kein Aufrufdatum angegeben.

{darstellung/hyperlink}
"""

PARAGRAPH_TOO_SHORT = 3


def check_10500_hyperlink_require_date(linter: callable, driver):
    """Check that Hyperlink has access label."""
    hyperlinks = driver.hyperlinks
    for link in hyperlinks:
        if link.visited:
            continue
        location = iamraw.Location.from_page(link.page)
        linter(location=location, link=link)
