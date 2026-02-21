from webdl.extractor import extract_links


def test_extract_modul_pages_and_download_forms_from_listing() -> None:
    html = """
    <html>
      <body>
        <a href="/modul-ajar-pai-kelas-3.html">PAI</a>
        <a href="https://www.websiteedukasi.com/modul-ajar-ipas-kelas-3.html">IPAS</a>
        <form action="https://www.websiteedukasi.com/download/modul-ajar-pai-kelas-3" method="post"></form>
      </body>
    </html>
    """

    links = extract_links(html, "https://www.websiteedukasi.com/modul-ajar-kelas-3.html")

    assert "https://www.websiteedukasi.com/modul-ajar-pai-kelas-3.html" in links.modul_pages
    assert "https://www.websiteedukasi.com/modul-ajar-ipas-kelas-3.html" in links.modul_pages
    assert "https://www.websiteedukasi.com/download/modul-ajar-pai-kelas-3" in links.download_pages


def test_extract_direct_files_from_download_page() -> None:
    html = """
    <html>
      <body>
        <a href="https://drive.google.com/uc?export=download&amp;id=abc123">Download</a>
      </body>
    </html>
    """

    links = extract_links(html, "https://www.websiteedukasi.com/download/modul-ajar-pai-kelas-3")

    assert links.direct_files == ["https://drive.google.com/uc?export=download&id=abc123"]
