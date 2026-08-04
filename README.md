# Showcase
<img width="1906" height="1016" alt="ashara screenshot" src="https://github.com/user-attachments/assets/072fbf24-34e3-496d-8cc6-d819f7d668ba" />

[![Showcase](Showcase)](https://github.com/user-attachments/assets/c0161b9e-a61f-4d57-9b5b-f647cb4bbb10)

<br>

# Ashara — a terminal music player

A terminal-based music player built with:
- **mpv/libmpv** (via `python-mpv`) for actual audio playback
- **Textual** for the terminal UI
- **mutagen** for reading track metadata (title/artist/duration)

<br>

## Features
- Recursive scan of a directory for `.mp3 .flac .wav .ogg .m4a .opus`
- Track list with title/artist/duration
- Play / pause / seek / next / previous
- Live elapsed/remaining timestamps + progress bar
- A minimal animated bar visualizer

<br>

## Setup
>[!Note]
>You need `libmpv` installed at the OS level (this is what `python-mpv`
binds to via ctypes — pip alone won't provide the actual audio engine).


On Arch :
```bash
sudo pacman -S mpv
```

On Debian :
```bash
sudo apt install mpv -y
```

<br>

<b>Then clone this repo :</b>
```bash
git clone --depth 1 https://www.github.com/kraken-503/Ashara.git && cd Ashara/
```

after cloning, install Python dependencies:
```bash
pip install -r requirements.txt
```

<br>

## Run

```bash
python3 main.py /path/to/your/music
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

<br>

<p align="center">
  <em>Made with ❤️ by kraken-503</em>
</p>
