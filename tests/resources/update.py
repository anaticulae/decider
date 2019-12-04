# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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
    files = [
        tests.resources.DOCU_TWINE,
        tests.resources.MASTER_72_PAGES_NOIMAGES,
        tests.resources.MASTER_78_PAGES_IMAGES,
    ]
    destination = tests.resources.GENERATED
    hey.example.extract(files, destination, pages=None)


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
