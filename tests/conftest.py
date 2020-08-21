# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hey.example
import power
import pytest
import utila
import utilatest
import writers

import decider
import tests.resources
import tests.resources.utils

PACKAGE = decider.PACKAGE

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

WORKER = 8

RESOURCES = tests.resources.TODO
RESOURCES_NOTOC = tests.resources.GENERATE_NO_TOC
RESOURCES_NOTITLE = tests.resources.GENERATE_NO_TITLE


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.REQURIED_RESOURCES)


def extract(resources):
    print_resources(resources)
    destination = tests.resources.GENERATED
    todo = hey.example.todolist(
        resources + [power.REPOSITORY],
        destination=destination,
        caption=True,
        detector=True,
        doctextstyle=True,
        groupme=True,
        magic=True,
        sections=True,
        words=True,
    )
    tests.resources.utils.run_parallel(todo, worker=WORKER, progress=True)


def extract_notoc(resources):
    destination = power.generated(folder='notoc')
    print_resources(resources)
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
        todo.append(f'jam -i {inpath} -o {outpath} --remove=1:5')
    # generate
    todo.extend(
        hey.example.todolist(
            without_titlepage + [destination],  # ensure correct parent
            destination,
            groupme=True,
        ))
    # avoid race condition that jam is not ready before starting extraction
    worker = utila.mins(len(files), WORKER)
    tests.resources.utils.run_parallel(todo, worker=worker, progress=True)


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
    todo.extend(
        hey.example.todolist(
            without_titlepage + [destination],  # ensure correct parent
            destination,
            groupme=True,
        ))
    # avoid race condition that jam is not ready before starting extraction
    worker = utila.mins(len(files), WORKER)
    tests.resources.utils.run_parallel(todo, worker=worker, progress=True)


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
