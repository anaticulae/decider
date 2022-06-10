# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_page:

PageOrder
=========
"""

import iamraw
import protocol
import serializeraw
import utila

import decider.page

# TODO: ADD PROCESS TO CHECK THAT PAGE NUMER IS LOCATED ONLY IN HEADER OR
# FOOTER, NOT MIXED OR BOTH


def work(
    headerfooter: str,
    sections: str,
    pagenumbers: str = None,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = create_driver(
        headerfooter,
        sections,
        pagenumbers,
        pages=pages,
    )
    # TODO: ADD PROCESS TO VALIDATE PAGE NUMBERS IN HEADER
    result = protocol.run(
        __name__,
        driver=driver,
    )
    return result


def create_driver(
    headerfooter: str,
    sections: str,
    pagenumbers: str,
    pages: tuple = None,
):
    headerfooter = serializeraw.load_headerfooter(
        headerfooter,
        pages=pages,
    )
    if utila.exists(sections):
        sections = serializeraw.load_sections(
            sections,
            pages=pages,
        )
    else:
        utila.error(f'missing: {sections}')
        sections = None
    if utila.exists(pagenumbers):
        pagenumbers = serializeraw.load_pagenumbers(
            pagenumbers,
            pages=pages,
        )
    else:
        utila.error(f'missing: {pagenumbers}')
        pagenumbers = None
    result = protocol.driver(
        headerfooter=headerfooter,
        sections=sections,
        pagenumbers=pagenumbers,
    )
    return result


SOLUTION_E1960 = """\
Dokument enthält nicht nur aufsteigende Seitenzahlen

Überprüfen Sie die Seitenzählung.

Zeile: {{text}}

Seite {{current}} folgt auf {{before}}.

{darstellung/seitenzahlen}
"""


def check_1960_ascending_pages(linter, driver):
    footers = [item.footer for item in driver.headerfooter]
    validated_footer = decider.page.validate(footers)
    for item in validated_footer:
        linter(
            current=item.current,
            before=item.before,
            text=item.text,
        )
