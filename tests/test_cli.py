from pathlib import Path

from webdl.cli import _build_class_urls, cmd_download_classes
from webdl.models import AnalysisReport


class DummyArgs:
    classes = "1-6"
    exclude = "3"
    max_pages = 10
    limit = None
    out = "downloads"


def test_build_class_urls_excludes_grade_3() -> None:
    urls = _build_class_urls("1-6", "3")

    assert urls == [
        "https://www.websiteedukasi.com/modul-ajar-kelas-1.html",
        "https://www.websiteedukasi.com/modul-ajar-kelas-2.html",
        "https://www.websiteedukasi.com/modul-ajar-kelas-4.html",
        "https://www.websiteedukasi.com/modul-ajar-kelas-5.html",
        "https://www.websiteedukasi.com/modul-ajar-kelas-6.html",
    ]


def test_cmd_download_classes_downloads_for_selected_grades(monkeypatch) -> None:
    calls: list[tuple[str, Path]] = []

    def fake_analyze_site(url: str, max_pages: int = 30) -> AnalysisReport:
        return AnalysisReport(start_url=url, direct_files=[f"{url}?file=1"])

    def fake_download_file(session, link: str, out_dir: Path) -> Path:  # noqa: ANN001
        calls.append((link, out_dir))
        return out_dir / "ok.bin"

    monkeypatch.setattr("webdl.cli.analyze_site", fake_analyze_site)
    monkeypatch.setattr("webdl.cli.download_file", fake_download_file)

    result = cmd_download_classes(DummyArgs())

    assert result == 0
    assert len(calls) == 5
    assert all("kelas-3" not in link for link, _ in calls)
    assert {str(out_dir) for _, out_dir in calls} == {
        "downloads/kelas-1",
        "downloads/kelas-2",
        "downloads/kelas-4",
        "downloads/kelas-5",
        "downloads/kelas-6",
    }
