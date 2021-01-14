# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex

RUNNER = [
    'textflow',
    'decider_textflow',
    'decider_imgfig',
    'decider_smarty',
]

SELECTED = dict(
    caption=True,
    detector=True,
    docref=True,
    doctextstyle=True,
    groupme=True,
    magic=True,
    sections=True,
    smarty=True,
    spacestation=True,
    words=True,
)


def extract(
        files: list,
        destination: str,
        pages: str = '0:10',
        worker: int = 12,
):
    """Run rawmaker, groupme, sections, words, detector, decider for
    given `files` and write result to `destination`.

    Args:
        files(list): list of files to work on
        destination(path): create folder for every file and save result
        pages(str): default selection if `file` does not provide `page`
                    selection
        worker(int): number of threads to extract examples
    Raises:
        Exception: if Exception occurs while extracting file
    """
    assert len(files) >= 2, ('require at least two files to '
                             'determine output file names correctly')
    genex.extract(
        files=files,
        destination=destination,
        pages=pages,
        morefeatures=RUNNER,
        oneline=genex.ONELINE,
        rawmaker=genex.CONFIG,
        worker=worker,
        **SELECTED,
    )
