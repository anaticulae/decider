# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. todo:: reduce code duplication, see `hey`."""
import concurrent
import os

import hey.example
import utila
import utilatest


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
    assert len(files) >= 2, ('require at least to files to '
                             'determine output file name correctly')
    for pdf in files:
        pdf = pdf if isinstance(pdf, str) else pdf[0]  # remove pages
        assert pdf.endswith('.pdf') and os.path.exists(pdf), str(pdf)

    # ensure that generation directory exists
    os.makedirs(destination, exist_ok=True)

    def run_job(job: str):
        utila.log(f'start: {job[0:150]}')
        completed = utila.run(job)
        utila.assert_success(completed)
        utila.log(f'complete: {job[0:100]}')

    # add selected page to every file if required
    files = [(item, pages) if isinstance(item, str) else item for item in files]
    generated = generate(files, destination)

    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = {executor.submit(run_job, pdf): pdf for pdf in generated}
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception as error:
                utila.info(f'{error}\n{future} failed.')
                raise


def generate(files: list, outpath: str) -> list:
    todo = []
    names = utilatest.simplify_testfile_names(
        files=[item for item, _ in files],  # remove page attribute
        sort=False,
    )
    for (inpath, pages), output in zip(files, names):
        outdir = os.path.join(outpath, output)
        job = hey.example.create_job(
            inpath,
            outdir,
            config=dict(
                detector=True,
                doctextstyle=True,
                groupme=True,
                magic=True,
                sections=True,
                words=True,
            ),
            pages=pages,
        )
        next_job = create_job(
            outdir,
            pages=pages,
        )
        in_a_row = f'{job} && {next_job}'
        todo.append(in_a_row)
    return todo


def create_job(path: str, pages: tuple = None) -> str:
    """Create job to run required steps for next processing unit.

    Args:
        path: source with extract pdf
        pages: shrink processing if given - if None process all pages
    Returns:
        Created process todo description.
    """
    pages = f'--pages={pages}' if pages is not None else ''
    task = [
        f'detector -j 8 -i {path} -o {path} {pages}',
        f'decider -j 8 -i {path} -o {path}',
        f'decider_border -i {path} -o {path} {pages}',
        f'textflow -i {path} -o {path} {pages}',
        f'decider_textflow -i {path} -o {path}',
        f'decider_textstyle -j8 -i {path} -o {path}',
    ]
    todo = ' && '.join(task)
    return todo
