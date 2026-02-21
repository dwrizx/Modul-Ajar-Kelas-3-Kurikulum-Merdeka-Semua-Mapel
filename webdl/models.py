from dataclasses import dataclass, field


@dataclass
class ExtractedLinks:
    modul_pages: list[str] = field(default_factory=list)
    download_pages: list[str] = field(default_factory=list)
    direct_files: list[str] = field(default_factory=list)


@dataclass
class AnalysisReport:
    start_url: str
    pages_scanned: list[str] = field(default_factory=list)
    modul_pages: list[str] = field(default_factory=list)
    download_pages: list[str] = field(default_factory=list)
    direct_files: list[str] = field(default_factory=list)
