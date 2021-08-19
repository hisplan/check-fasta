from check_fasta import CheckFasta


def test_file_extension():
    "The file extension must be .fa"

    cf = CheckFasta()

    assert False == cf.check_filename("data/wront-extension.fasta")

    assert True == cf.check_filename("data/wront-extension.fa")

    assert False == cf.check_filename("data/wrong-extension")


def test_header():
    """
    The header must start with the `>` character.
    There must be no whitespaces after the `>` character.
    """

    cf = CheckFasta()

    fasta = """>EGFP
ATGGTGAGCAAGGGCG
"""
    assert True == cf.check_header(fasta)

    fasta = """EGFP
ATGGTGAGCAAGGGCG
"""
    assert False == cf.check_header(fasta)

    fasta = """>    EGFP
ATGGTGAGCAAGGGCG
"""
    assert False == cf.check_header(fasta)

    fasta = """>        EGFP
ATGGTGAGCAAGGGCG
"""
    assert False == cf.check_header(fasta)


def test_multiline():
    "The entire sequence must be in one line."

    cf = CheckFasta()

    fasta = cf.load_fasta("data/err-multiline.fa")

    assert False == cf.check_multiline(fasta)

    fasta = """>EGFP
ATGGTGAGCAAGGGCGAGG
GGCGACGTAAACGGCCACA
GGCAAGCTGACCCTGAAGT
CTCGTGACCACCTTCGGCT
CAGCACGACTTCTTCAAGT
TTCAAGGACGACGGCAACT
GTGAACCGCATCGAGCTGA
AAGCTGGAGTACAACTACA
"""
    assert False == cf.check_multiline(fasta)

    fasta = """>EGFP
ATGGTGAGCAAGGGCGAGG
"""
    assert True == cf.check_multiline(fasta)


def test_empty_line():
    "There must be no empty lines."

    cf = CheckFasta()

    fasta = """>EGFP
ATGGTGAGCAAGGGCGAGG
GGCGACGTAAACGGCCACA

TTCAAGGACGACGGCAACT
GTGAACCGCATCGAGCTGA
AAGCTGGAGTACAACTACA
"""
    assert False == cf.check_empty_line(fasta)


def test_last_character():
    "The sequence must end with a newline character."

    cf = CheckFasta()

    fasta = """>EGFP
ATGGTGAGCAAGGGCGAGG
"""
    assert True == cf.check_last_character(fasta)

    fasta = """>EGFP
ATGGTGAGCAAGGGCGAGG"""
    assert False == cf.check_last_character(fasta)


def test_bad_fasta():
    "Test bad FASTA files."

    cf = CheckFasta()

    assert 0 < cf.run_all_tests(path_fasta="data/err-multiline.fa")

    assert 0 < cf.run_all_tests(path_fasta="data/err-wrong-extension.fasta")

    assert 0 < cf.run_all_tests(path_fasta="data/err-last-char.fa")


def test_good_fasta():
    "Test good FASTA files."

    cf = CheckFasta()

    assert 0 == cf.run_all_tests(path_fasta="data/good.fa")
