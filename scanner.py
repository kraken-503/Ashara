"""Directory scanning and metadata extraction."""

from pathlib import Path
from mutagen import File as MutagenFile

AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".opus"}


class Track:
    def __init__(self, path: Path):
        self.path = path
        self.title = path.stem
        self.artist = "Unknown Artist"
        self.duration = 0.0
        self._read_tags()

    def _read_tags(self):
        try:
            audio = MutagenFile(self.path, easy=True)
            if audio is None:
                return
            if audio.tags:
                title = audio.tags.get("title")
                artist = audio.tags.get("artist")
                if title:
                    self.title = title[0]
                if artist:
                    self.artist = artist[0]
            if audio.info is not None and hasattr(audio.info, "length"):
                self.duration = float(audio.info.length)
        except Exception:
            # Tag reading failed for this file; fall back to filename defaults
            # rather than crashing the whole scan.
            pass


def scan_directory(root: str) -> list[Track]:
    root_path = Path(root).expanduser().resolve()
    if not root_path.is_dir():
        raise NotADirectoryError(f"{root_path} is not a directory")

    tracks = []
    for path in sorted(root_path.rglob("*")):
        if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
            tracks.append(Track(path))
    return tracks
