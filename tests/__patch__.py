# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: REMOVE THIS PATCH AFTER UPGRADING HEY
import hey.example


def create_job(
        src: str,
        dest: str,
        rawmaker: str,
        oneline: str,
        pages: tuple = None,
        config: dict = None,
) -> str:
    """Create job to run required steps for next processing unit.

    Args:
        src: pdf file for processing
        dest: output path to output folder
        rawmaker: default config
        oneline: default oneline config
        pages: shrink processing if given - if None process all pages
        config: select which processes to run
    Returns:
        Created process todo description.
    """
    if config is None:
        config = {}

    pages = f'--pages={pages}' if pages is not None else ''
    task = [
        f'rawmaker -j=auto -i {src} -o {dest} {rawmaker} {pages}',
        f'rawmaker -j=auto -i {src} -o {dest} {oneline} {pages}',
        f'linero -i {dest} -o {dest}',
    ]
    if config.get('groupme', False):
        # run all, disable --toc
        task.append(f'groupme --toc! -j=auto -i {dest} -o {dest}')
        # toc only
        task.append(f'groupme --toc --pages=0:10 -i {dest} -o {dest}')
    if config.get('sections', False):
        task.append(f'sections -j=auto -i {dest} -o {dest}')
    if config.get('words', False):
        task.append(f'words -j=auto -i {dest} -o {dest}')
    if config.get('detector', False):
        task.append(f'detector -i {dest} -o {dest}')
    if config.get('textflow', False):
        task.append(f'textflow -i {dest} -o {dest}')
    if config.get('doctextstyle', False):
        task.append(f'doctextstyle -i {dest} -o {dest}')
    if config.get('caption', False):
        task.append(f'caption -i {dest} -o {dest}')
    if config.get('magic', False):
        task.append(f'magic -i {dest} -o {dest}')
    todo = ' && '.join(task)
    return todo


hey.example.create_job = create_job
