# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import genex
import power
import pytest
import utila
import utilatest
import writers

import decider

PACKAGE = decider.PACKAGE

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

WORKER = 6

RESOURCES = [
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
    (power.MASTER110_PDF, '0:70'),
    (power.MASTER089_PDF, '40:50'),
    (power.MASTER075_PDF, ':'),
    (power.BACHELOR063_PDF, ':'),
    (power.BACHELOR076_PDF, ':'),
    (power.MASTER072_PDF, ':'),
    (power.BACHELOR090_PDF, ':'),
    (power.BACHELOR037_PDF, '0:10'),
    (power.BACHELOR056_PDF, '0:20'),
    (power.DOCU35_PDF, '0:10'),
    (power.HOME025_PDF, ':'),
    (power.BOOK007_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.MASTER099_PDF, '0:10'),
    (power.TECH024_PDF, '0:15'),
    (power.BACHELOR128_PDF, '0:20'),
]

RESOURCES_NOTITLE = [
    (power.DOCU35_PDF, ':'),
    (power.BOOK007_PDF, ':'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    print_resources(resources)
    genex.extract(
        files=resources,
        destination=power.generated(),
        full=True,
        base=power.REPOSITORY,
        worker=WORKER,
    )


def extract_notitle(resources):
    print_resources(resources)
    destination = power.generated(folder='notitle')
    files = [item[0] for item in resources]
    # prepare
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(
            files + [power.REPOSITORY],  # ensure correct parent
            sort=False,
        )
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        todo.append(f'jam -i {inpath} -o {outpath} --remove=0')
    # generate
    for job in genex.todolist(
            without_titlepage + [destination],  # ensure correct parent
            destination,
            groupme=True,
    ):
        job = ' && '.join(job)
        todo.append(job)
    # avoid race condition that jam is not ready before starting extraction
    worker = utila.mins(len(files), WORKER)
    utila.run_parallel(todo, worker=worker)


def install():
    # generate docs after project is installed properly
    writers.generate()


def print_resources(resources):
    for item in resources:
        try:
            source, page = item
        except ValueError:
            source, page, = item, 'all'
        utila.log(f'source: {source}, pages: {page:8}')
