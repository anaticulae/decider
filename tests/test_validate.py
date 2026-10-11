# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import protoerror
import pytest
import utilo
import utilotest

import decider
import tests
import tests.footnote_
import tests.imgfig_

ARCHIVE = utilo.join(decider.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.BACHELOR063_PDF, id='bachelor063'),
    pytest.param(hoverpower.BACHELOR076_PDF, id='bachelor076'),
    pytest.param(hoverpower.BACHELOR090_PDF, id='bachelor090'),
    pytest.param(hoverpower.MASTER072_PDF, id='master072'),
    pytest.param(hoverpower.MASTER075_PDF, id='master075'),
])
@utilotest.nightly
def test_validate_all(source, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


def run_extraction(cmd, mp):  # pylint:disable=W0613
    tests.run(cmd, mp=mp)
    tests.footnote_.run(cmd, mp=mp)
    tests.imgfig_.run(cmd, mp=mp)


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, workdir, mp):
        super().__init__(
            program=functools.partial(
                run_extraction,
                mp=mp,
            ),
            step=None,
            pages=':',
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )
        self.headlines = hoverpower.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        return protoerror.findings_from_path(path)

    def raw(self, value) -> str:
        findings = utilo.flatten_content(value)
        findings = [line(item) for item in findings]
        findings = sorted(findings, key=utilo.alphabetically)
        result = utilo.NEWLINE.join(findings)
        return result


def line(finding) -> str:
    result = str(finding.msgid).zfill(5) + ' '
    result += str(finding.location) + ' '
    result += finding.solution.title
    return result
