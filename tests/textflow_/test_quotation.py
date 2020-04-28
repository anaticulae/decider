# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import words.text.sentence
import words.text.word

import decider_textflow.quotation.validate as dtqv

STANDARD = """„Protest“, so schreibt Sigrid Baringhorst, „ist
kommunikatives Handeln“ (1998: 327). Will man das Phänomen ‚Protest‘
angemessen erfassen, so gilt es zu untersuchen, wie er kommuniziert
wird."""


def test_german_double_quote():
    first = words.text.word.split_words(
        words.text.sentence.split_sentences(STANDARD)[0])
    assert dtqv.german_double_quotation_closed(first)
    assert dtqv.german_no_double_quotes_inside_double(first)


REQUIRE_SINGLE_INSIDE = """\
Bevor die Konzepte der Privatheit und Öffentlichkeit
systemtheoretisch näher betrachtet werden, soll vorab kurz umrissen
werden, was darunter verstanden wird. Rössler beschreibt etwas
Privates folgendermaßen: „‚privat‘ nennen wir einerseits Handlungs-
und Verhaltensweisen, zum Zweiten ein bestimmtes Wissen und drittens
Räume“ und weiter: „als privat gilt etwas dann, wenn man selbst
den Zugang zu diesem „etwas“ kontrollieren kann“. Privatheit
beinhaltet also den Aspekt der Zugangskontrolle seitens des
Individuums.
"""


def test_german_double_quote_inside_double():
    splitted = words.text.sentence.split_sentences(REQUIRE_SINGLE_INSIDE)
    assert len(splitted) == 5

    third = words.text.word.split_words(splitted[2])
    assert dtqv.german_no_double_quotes_inside_double(third)

    fourth = words.text.word.split_words(splitted[3])
    double_inside_double = dtqv.german_no_double_quotes_inside_double(fourth)
    assert double_inside_double is False
