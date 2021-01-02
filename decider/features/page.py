# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_page:

PageOrder
=========
"""

import typing

import protocol
import serializeraw

import decider
import decider.page

# TODO: ADD PROCESS TO CHECK THAT PAGE NUMER IS LOCATED ONLY IN HEADER OR
# FOOTER, NOT MIXED OR BOTH


def work(headerfooter: str, pages: tuple = None) -> typing.Tuple[str, str]:
    headerfooter = serializeraw.load_headerfooter(headerfooter, pages=pages)

    linter = protocol.from_module(__name__)

    linter.run(driver=headerfooter)
    # TODO: ADD PROCESS TO VALIDATE PAGE NUMBERS IN HEADER

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_1960 = """\
Dokument enthält nicht nur aufsteigende Seitenzahlen

Überprüfen Sie die Seitenzählung.

Zeile: {{text}}

Seite {{current}} folgt auf {{before}}.

{darstellung/seitenzahlen}
"""


def check_1960_ascending_pages(linter, headerfooter):
    footers = [item.footer for item in headerfooter]
    validated_footer = decider.page.validate(footers)

    for item in validated_footer:
        linter(current=item.current, before=item.before, text=item.text)
