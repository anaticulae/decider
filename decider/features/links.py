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

import os
import typing

import iamraw
import linkify.serialize
import protocol
import serializeraw
import utila

import decider


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

Für den Hyperlink **{{link.href|wordwrap(40)}}** ist kein Aufrufdatum angegeben.

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


SOLUTION_10510 = """\
Hyperlink nicht erreichbar

Auf den Hyperlink **{{link.href|wordwrap(40)}}** kann nicht zugegriffen
werden. Überprüfen Sie die Schreibweise bzw. achten Sie darauf dass der
Hyerplink ohne weitere Authorisierung erreichbar ist.

{darstellung/hyperlink}
"""


def check_10510_hyperlink_existence(linter: callable, driver):
    hyperlinks = [item.href for item in driver.hyperlinks]
    hyperlinks = utila.NEWLINE.join(hyperlinks)

    directory = utila.tmpdir(decider.ROOT)
    todo = os.path.join(directory, 'links__todo.yaml')
    utila.file_create(todo, hyperlinks)

    online = os.getenv(decider.DECIDER_ONELINE_FLAG, 'False')
    online = utila.str2bool(online)
    offline = '--offline' if not online else ''
    done = utila.run(
        f'linkify -i {directory} -o {directory} {offline}',
        expect=None,
    )
    if done.returncode != utila.SUCCESS:
        utila.error(f'{done.stdout}\n{done.stderr}')
        return

    outpath = os.path.join(directory, 'linkify__verify_verified.yaml')
    result = linkify.serialize.load_links(outpath)

    for hyperlink, validated in zip(driver.hyperlinks, result):
        validated = validated.split()[0]
        if validated == 'True':
            continue
        location = iamraw.Location.from_page(hyperlink.page)
        linter(location=location, link=hyperlink)
