# Ashara — a terminal music player (v1)

A terminal-based music player built with:
- **mpv/libmpv** (via `python-mpv`) for actual audio playback
- **Textual** for the terminal UI
- **mutagen** for reading track metadata (title/artist/duration)

## What Ashara includes
- Recursive scan of a directory for `.mp3 .flac .wav .ogg .m4a .opus`
- Track list with title/artist/duration
- Play / pause / seek / next / previous
- Live elapsed/remaining timestamps + progress bar
- A minimal animated bar visualizer

## Setup

You need `libmpv` installed at the OS level (this is what `python-mpv`
binds to via ctypes — pip alone won't provide the actual audio engine).

On Arch:
```bash
sudo pacman -S mpv
```

Then install Python dependencies:
```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py /path/to/your/music
```

## Keybindings

| Key      | Action        |
|----------|---------------|
| `Space`  | Play / Pause  |
| `n`      | Next track    |
| `p`      | Previous track|
| `←`      | Seek -5s      |
| `→`      | Seek +5s      |
| `↑ / ↓`  | Move track selection (built into DataTable) |
| `Enter`  | Play selected track |
| `q`      | Quit          |

