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

import border.cli
import decider
import fonts.cli
import tests.resources


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


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    destination = tests.resources.GENERATED
    if os.path.exists(destination):
        return

    hey.example.extract(tests.resources.TODO, destination, pages=None)

    extract_without_titlepage()
    extract_without_toc()


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


def extract_without_titlepage():
    destination = tests.resources.NO_TITLE_PAGE
    files = tests.resources.TODO
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in hey.example.output_names(files)
    ]
    for inpath, outpath in zip(files, without_titlepage):
        completed = utila.run(f'jam -i {inpath} -o {outpath} --remove=0')
        assert completed.returncode == utila.SUCCESS, str(completed)

    hey.example.extract(without_titlepage, destination, pages='0:20')


def extract_without_toc():
    destination = tests.resources.NO_TOC
    files = tests.resources.TODO
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in hey.example.output_names(files)
    ]
    for inpath, outpath in zip(files, without_titlepage):
        completed = utila.run(f'jam -i {inpath} -o {outpath} --remove=1:5')
        assert completed.returncode == utila.SUCCESS, str(completed)

    hey.example.extract(without_titlepage, destination, pages='0:20')
