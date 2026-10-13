# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilo
import utilotest
import writers
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import decider

PACKAGE = decider.PACKAGE

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

RESOURCES = [
    (hoverpower.BACHELOR037_PDF, '0:20'),
    (hoverpower.BACHELOR051_PDF, '0:30'),
    (hoverpower.BACHELOR077_PDF, '10:40'),
    (hoverpower.BACHELOR128_PDF, '0:20,50:70'),
    (hoverpower.BOOK007_PDF, '0:10'),
    (hoverpower.DISS273_PDF, '0:50'),
    (hoverpower.DISS480_PDF, '0:20'),
    (hoverpower.DOCU035_PDF, '0:10'),
    (hoverpower.MASTER078_PDF, '0:10'),
    (hoverpower.MASTER089_PDF, '40:50'),
    (hoverpower.MASTER091B_PDF, '0:50'),
    (hoverpower.MASTER098_PDF, '0:10,43:65,88:97'),
    (hoverpower.MASTER099_PDF, '0:10'),
    (hoverpower.MASTER116_PDF, '0:50,75:115'),
    (hoverpower.MASTER155_PDF, '0:30'),
    (hoverpower.MASTER193_PDF, '80:100'),
    (hoverpower.TECH024_PDF, '0:15'),
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.HOME018_PDF,
    hoverpower.HOME025_PDF,
    hoverpower.MASTER031_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
]
WORKER = utilotest.worker_count(4, onci=len(RESOURCES))

RESOURCES_NOTITLE = [
    (hoverpower.BOOK007_PDF, ':'),
    (hoverpower.DOCU035_PDF, ':'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    print_resources(resources)
    gennex.extract(
        files=resources,
        full=True,
        worker=WORKER,
    )


def extract_notitle(resources):
    gennex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        worker=len(resources),
        groupme=True,
        footnote=True,
        headnote=True,
        pagenumber=True,
        cleanup=True,
        sections=True,
        detector=True,
    )


def install():
    # generate docs after project is installed properly
    writers.generate()


def print_resources(resources):
    for item in resources:
        try:
            source, page = item
        except ValueError:
            source, page, = item, 'all'
        utilo.log(f'source: {source}, pages: {page:8}')
