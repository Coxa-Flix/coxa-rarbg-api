import dataclasses
import urllib.parse

trackers = [
    "http://tracker.trackerfix.com:80/announce",
    "udp://9.rarbg.me:2740",
    "udp://9.rarbg.to:2780",
    "udp://tracker.fatkhoala.org:13720",
    "udp://tracker.tallpenguin.org:15730",
    "udp://tracker.coppersurfer.tk:80",
    "udp://glotorrents.pw:6969/announce",
    "udp://tracker.leechers-paradise.org:6969",
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://exodus.desync.com:6969"
]

@dataclasses.dataclass
class Torrent:
    title: str
    hash_code: str
    time: str
    size: str
    imdb: str | None

    def build_magnet_link(self) -> str:
        base = f"magnet:?xt=urn:btih:{self.hash_code}&dn={urllib.parse.quote(self.title)}"
        tracker_links = "".join(f"&tr={urllib.parse.quote(tr)}" for tr in trackers)
        return base + tracker_links

def torrent_row_factory(_cursor, row):
    return Torrent(*row)
