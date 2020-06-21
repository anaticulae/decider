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
import utila
import utilatest
import writers

import border.cli
import decider
import fonts.cli
import tests.resources
import tests.resources.utils

WORKER = 8


def install_requirements():
    install_and_run(
        decider.ROOT,
        decider.PACKAGE,
        [
            border.cli.PROCESS,
            decider.PROCESS,
            fonts.cli.PROCESS,
        ],
    )

    # TODO: AUTOMATE THIS
    # generate docs
    writers.generate()


def install_and_run(root, package, executable=None):
    """Install and run --help to ensure basic function"""
    executable = executable if executable else package
    if isinstance(executable, str):
        executable = executable.split()
    uninstall = 'pip uninstall %s -y' % package

    executable = ' && '.join(['%s --help' % item for item in executable])
    install = 'python setup.py install && %s ' % executable

    clean_and_run = uninstall + ' && ' + install
    result = utila.run(clean_and_run, cwd=root)
    assert result.returncode == utila.SUCCESS, result.stdout + result.stderr


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    destination = tests.resources.GENERATED
    if os.path.exists(destination):
        return

    todo = []
    todo.extend(extract())
    todo.extend(extract_without_titlepage())
    todo.extend(extract_without_toc())

    # sort jam first
    todo = sorted(todo, key=lambda x: x.startswith('jam'), reverse=True)

    tests.resources.utils.run_parallel(todo, worker=WORKER, progress=True)


def extract():
    utila.log('extract')
    items = tests.resources.TODO
    destination = tests.resources.GENERATED
    todo = []
    for item, page in items:
        utila.log(f'pages:{page:8} source:{item}')
    todo.extend(
        hey.example.todolist(
            items,
            destination=destination,
            groupme=True,
            sections=True,
            words=True,
            doctextstyle=True,
        ))
    return todo


def extract_without_titlepage():
    utila.log('extract without titlepage')
    files = tests.resources.GENERATE_NO_TITLE
    destination = tests.resources.NO_TITLE_PAGE
    # prepare
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(files, sort=False)
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        utila.log(inpath)
        todo.append(f'jam -i {inpath} -o {outpath} --remove=0')
    # generate
    todo.extend(
        hey.example.todolist(
            without_titlepage,
            destination,
            pages='0:10',
        ))
    return todo


def extract_without_toc():
    utila.log('extract without toc')
    files = tests.resources.GENERATE_NO_TOC
    destination = tests.resources.NO_TOC
    # prepare
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(files, sort=False)
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        utila.log(inpath)
        todo.append(f'jam -i {inpath} -o {outpath} --remove=1:5')
    # generate
    todo.extend(
        hey.example.todolist(
            without_titlepage,
            destination,
            pages='0:10',
        ))
    return todo
