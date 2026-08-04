import sys
import random

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, DataTable, Static, ProgressBar
from textual.reactive import reactive

from scanner import scan_directory
from player import Player


def format_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


class Visualizer(Static):
    """Placeholder bar visualizer.

    """

    bars = reactive([1] * 24)

    def on_mount(self) -> None:
        self.set_interval(0.15, self.tick)

    def tick(self) -> None:
        app: "Ashara" = self.app  # type: ignore[assignment]
        if app.player.paused or app.player.current_track is None:
            self.bars = [1] * 24
        else:
            self.bars = [random.randint(1, 8) for _ in range(24)]

    def render(self) -> str:
        levels = " ▁▂▃▄▅▆▇█"
        return "".join(levels[min(b, 8)] for b in self.bars)


class Ashara(App):
    CSS = """
    Screen {
        background: #10121a;
    }
    #now-playing {
        height: 4;
        padding: 1 2;
        border: round #6c5ce7;
        color: #dfe6e9;
    }
    #visualizer {
        height: 3;
        content-align: center middle;
        color: #a29bfe;
    }
    #progress-row {
        height: 1;
        padding: 0 2;
    }
    #elapsed, #remaining {
        width: 6;
        color: #b2bec3;
    }
    DataTable {
        height: 1fr;
    }
    """

    BINDINGS = [
        ("space", "toggle_pause", "Play/Pause"),
        ("n", "next_track", "Next"),
        ("p", "prev_track", "Prev"),
        ("left", "seek_back", "Seek -5s"),
        ("right", "seek_forward", "Seek +5s"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, directory: str):
        super().__init__()
        self.directory = directory
        self.player = Player()
        self.tracks = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Static("No track loaded", id="now-playing")
            yield Visualizer(id="visualizer")
            with Horizontal(id="progress-row"):
                yield Static("00:00", id="elapsed")
                yield ProgressBar(total=100, id="progress", show_eta=False)
                yield Static("00:00", id="remaining")
            yield DataTable(id="track-table")
        yield Footer()

    def on_mount(self) -> None:
        try:
            self.tracks = scan_directory(self.directory)
        except NotADirectoryError as exc:
            self.exit(message=str(exc))
            return

        self.player.load_playlist(self.tracks)

        table = self.query_one("#track-table", DataTable)
        table.add_columns("#", "Title", "Artist", "Duration")
        for i, track in enumerate(self.tracks, start=1):
            table.add_row(str(i), track.title, track.artist, format_time(track.duration))
        table.cursor_type = "row"

        if not self.tracks:
            self.query_one("#now-playing", Static).update(
                f"No audio files found under {self.directory}"
            )

        self.set_interval(0.5, self.refresh_now_playing)

    def update_now_playing(self) -> None:
        panel = self.query_one("#now-playing", Static)
        track = self.player.current_track
        if track is None:
            panel.update("No track loaded — select one below and press Enter")
        else:
            status = "⏸ Paused" if self.player.paused else "▶ Playing"
            panel.update(f"{status}\n[b]{track.title}[/b] — {track.artist}")

    def refresh_now_playing(self) -> None:
        self.update_now_playing()
        progress = self.query_one("#progress", ProgressBar)
        elapsed = self.query_one("#elapsed", Static)
        remaining = self.query_one("#remaining", Static)

        duration = self.player.duration
        position = self.player.position
        if duration > 0:
            progress.update(total=100, progress=(position / duration) * 100)
        else:
            progress.update(total=100, progress=0)

        elapsed.update(format_time(position))
        remaining.update("-" + format_time(max(0, duration - position)))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.player.play_index(event.cursor_row)
        self.update_now_playing()

    def action_toggle_pause(self) -> None:
        if self.player.current_track is None and self.tracks:
            self.player.play_index(0)
        else:
            self.player.toggle_pause()
        self.update_now_playing()

    def action_next_track(self) -> None:
        self.player.play_next()
        self.update_now_playing()

    def action_prev_track(self) -> None:
        self.player.play_prev()
        self.update_now_playing()

    def action_seek_back(self) -> None:
        self.player.seek(-5)

    def action_seek_forward(self) -> None:
        self.player.seek(5)

    def action_quit(self) -> None:
        self.player.shutdown()
        self.exit()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <music-directory>")
        sys.exit(1)
    app = Ashara(sys.argv[1])
    app.run()


if __name__ == "__main__":
    main()
