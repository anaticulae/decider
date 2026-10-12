# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import utilo

RUNNER = [
    'textflow',
    'decider_textflow',
    'decider_imgfig',
    'decider_smarty',
]

SELECTED = {
    "caption": True,
    "codero": True,
    "detector": True,
    "docref": True,
    "doctextstyle": True,
    "groupme": True,
    "headlines": True,
    "lists": True,
    "magic": True,
    "sections": True,
    "smarty": True,
    "spacestation": True,
    "words": True,
}


@utilo.rename(destination='dest')
def extract(
    files: list,
    dest: str,
    pages: str = '0:10',
    worker: int = 12,
    morefeatures: list = None,
    selected: dict = None,
    full: bool = False,
):
    """Run rawmaker, groupmes, sections, verbo, detector, decider for
    given `files` and write result to `dest`.

    Args:
        files(list): list of files to work on
        dest(path): create folder for every file and save result
        pages(str): default selection if `file` does not provide `page`
                    selection
        worker(int): number of threads to extract examples
        morefeatures(list): add list to run additional runner
        selected(dict): select runner to execute
        full(bool): run all generator
    Raises:
        Exception: if Exception occurs while extracting file
    """
    morefeatures = morefeatures + RUNNER if morefeatures is not None else RUNNER
    selected = selected if selected is not None else SELECTED
    gennex.extract(
        files=files,
        dest=dest,
        pages=pages,
        morefeatures=morefeatures,
        oneline=gennex.ONELINE,
        rawmaker=gennex.CONFIG,
        worker=worker,
        full=full,
        **selected,
    )
