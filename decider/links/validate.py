# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import linkify.serialize
import utila

import decider


def visit(hyperlinks: list) -> list:
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
        return None

    outpath = os.path.join(directory, 'linkify__verify_verified.yaml')
    result = linkify.serialize.load_links(outpath)
    return result
