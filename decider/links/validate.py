# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import linkify.serialize
import utilo

import decider


def visit(hyperlinks: list) -> list:
    hyperlinks = utilo.NEWLINE.join(hyperlinks)

    directory = utilo.tmpdir(decider.ROOT)
    todo = os.path.join(directory, 'links__todo.yaml')
    utilo.file_create(todo, hyperlinks)

    online = os.getenv(decider.DECIDER_ONELINE_FLAG, 'False')
    online = utilo.str2bool(online)
    offline = '--offline' if not online else ''
    done = utilo.run(
        f'linkify -i {directory} -o {directory} {offline}',
        expect=None,
    )
    if done.returncode != utilo.SUCCESS:
        utilo.error(f'{done.stdout}\n{done.stderr}')
        return None

    outpath = os.path.join(directory, 'linkify__verify_verified.yaml')
    result = linkify.serialize.load_links(outpath)
    return result
