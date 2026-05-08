from pathlib import Path

from download_ncrb_pdfs import is_pdf, output_name, part_label, slugify


def test_slugify_normalizes_to_flat_ascii_name():
    assert slugify("Crime in India 2018 - Volume 1_3_0_0.pdf") == "crime-in-india-2018-volume-1-3-0-0-pdf"


def test_part_label_prefers_part_and_volume_markers():
    assert part_label("https://example.test/1CrimeinIndia2023PartII.pdf", "") == "part-ii"
    assert part_label("https://example.test/CII%202019%20Volume%201.pdf", "") == "volume-1"


def test_output_name_is_flat_and_year_prefixed():
    name = output_name(2023, "https://example.test/1CrimeinIndia2023PartI.pdf", "", 1)
    assert name == "crime-in-india-2023-part-i.pdf"


def test_is_pdf_checks_magic_bytes(tmp_path: Path):
    pdf = tmp_path / "ok.pdf"
    pdf.write_bytes(b"%PDF-1.7\n")
    not_pdf = tmp_path / "bad.pdf"
    not_pdf.write_bytes(b"<html>")
    assert is_pdf(pdf)
    assert not is_pdf(not_pdf)
