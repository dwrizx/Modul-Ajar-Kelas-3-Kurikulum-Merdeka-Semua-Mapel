from webdl.downloader import _extract_drive_confirm_request, guess_filename


def test_guess_filename_from_query_id() -> None:
    url = "https://drive.google.com/uc?export=download&id=1Ct4heDzgDedF6fPKSahZ9OGINgOm9_GW"
    assert guess_filename(url, {}) == "1Ct4heDzgDedF6fPKSahZ9OGINgOm9_GW"


def test_guess_filename_from_content_disposition() -> None:
    headers = {"Content-Disposition": 'attachment; filename="modul-ajar-kelas-3.docx"'}
    assert guess_filename("https://example.com/download", headers) == "modul-ajar-kelas-3.docx"


def test_extract_drive_confirm_request() -> None:
    html = """
    <form id="download-form" action="https://drive.usercontent.google.com/download" method="get">
      <input type="hidden" name="id" value="abc123">
      <input type="hidden" name="export" value="download">
      <input type="hidden" name="confirm" value="t">
      <input type="hidden" name="uuid" value="u-1">
    </form>
    """
    action, params = _extract_drive_confirm_request(html) or ("", {})

    assert action == "https://drive.usercontent.google.com/download"
    assert params["id"] == "abc123"
    assert params["confirm"] == "t"
