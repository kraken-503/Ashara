"""playback wrapper around python-mpv (libmpv bindings)."""

import mpv


class Player:
    def __init__(self):
        # video=False keeps this audio-only; ytdl=False avoids trying
        # to resolve local paths as streaming URLs.
        self._mpv = mpv.MPV(video=False, ytdl=False)
        self._playlist = []
        self._index = -1

    def load_playlist(self, tracks):
        self._playlist = tracks
        self._index = -1

    @property
    def current_track(self):
        if 0 <= self._index < len(self._playlist):
            return self._playlist[self._index]
        return None

    def play_index(self, index: int):
        if not (0 <= index < len(self._playlist)):
            return
        self._index = index
        track = self._playlist[index]
        self._mpv.play(str(track.path))
        self._mpv.pause = False

    def play_next(self):
        if self._playlist:
            self.play_index((self._index + 1) % len(self._playlist))

    def play_prev(self):
        if self._playlist:
            self.play_index((self._index - 1) % len(self._playlist))

    def toggle_pause(self):
        self._mpv.pause = not self._mpv.pause

    @property
    def paused(self) -> bool:
        return bool(self._mpv.pause)

    def seek(self, seconds: float):
        try:
            self._mpv.seek(seconds, reference="relative")
        except Exception:
            # Seeking can fail momentarily right after a track loads;
            # ignore rather than crash the UI loop.
            pass

    @property
    def position(self) -> float:
        return self._mpv.time_pos or 0.0

    @property
    def duration(self) -> float:
        return self._mpv.duration or 0.0

    def set_volume(self, volume: int):
        self._mpv.volume = max(0, min(100, volume))

    @property
    def volume(self) -> int:
        return int(self._mpv.volume or 0)

    def shutdown(self):
        self._mpv.terminate()
