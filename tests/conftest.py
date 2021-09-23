# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utila
import writers

import decider

PACKAGE = decider.PACKAGE

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

WORKER = 6

RESOURCES = [
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
    (power.MASTER110_PDF, '0:70'),
    power.MASTER075_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR076_PDF,
    power.MASTER072_PDF,
    power.BACHELOR090_PDF,
    power.HOME025_PDF,
    power.MASTER031_PDF,
    (power.MASTER091B_PDF, '0:50'),
    (power.MASTER155_PDF, '0:30'),
    (power.BACHELOR037_PDF, '0:20'),
    (power.BACHELOR051_PDF, '0:30'),
    (power.BACHELOR056_PDF, '0:20'),
    (power.BACHELOR128_PDF, '0:20,50:70'),
    (power.BOOK007_PDF, '0:10'),
    (power.DOCU035_PDF, '0:10'),
    power.HOME018_PDF,
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.MASTER089_PDF, '40:50'),
    (power.MASTER099_PDF, '0:10'),
    (power.TECH024_PDF, '0:15'),
]

RESOURCES_NOTITLE = [
    (power.DOCU035_PDF, ':'),
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
        pages=':',
    )


def extract_notitle(resources):
    genex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        worker=WORKER,
        groupme=True,
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
        utila.log(f'source: {source}, pages: {page:8}')
