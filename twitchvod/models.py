from urllib.parse import urlparse
from enum import Enum
from typing import List, Tuple
from utils import locate_with_default


STREAM_EXT_MEDIA_STARTS_WITH = "#EXT-X-STREAM-INF:"

class HttpMethod(Enum):
    """Enum to describe an HTTP method and the corresponding value.
    """

    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"
    PUT = "PUT"


def get_ext_media_indexes(m3u8_data: List[str]) -> List[Tuple[int,int]]:
    """
    """

    rows_to_extract = []

    for rec_num, record in enumerate(m3u8_data):
        if record.startswith(STREAM_EXT_MEDIA_STARTS_WITH):
            rows_to_extract.append((rec_num, rec_num+1,))

    return rows_to_extract


def parse_stream_info_from_response(raw_m3u8_response: str):
    """
    """

    records = raw_m3u8_response.splitlines()
    indexes = get_ext_media_indexes(records)
    infos = []

    for a, b in indexes:
        inf_record = records[a]
        url = records[b]
        infos.append(stream_version_info_from_raw(inf_record, url))

    return infos


def stream_version_info_from_raw(raw_stream_data: str, stream_url: str):
    """Build a models.StreamVersionInfo object from raw data that comes from
    the Twitch stream information.

    :param raw_stream_data: a string of chararacters to be parsed.
    :param stream_url: a string of characters representing the url of the
                       vod stream.
    :return: A StreamVersionInfo object.
    :rtype: StreamVersionInfo.
    """

    prog_id = locate_with_default(r"PROGRAM-ID=(\d*?),", raw_stream_data)
    program_id = int(prog_id) if prog_id is not None else None

    bandw = locate_with_default(r"BANDWIDTH=(\d*?),", raw_stream_data)
    bandwidth = int(bandw) if bandw is not None else None

    cdcs = locate_with_default(r"CODECS=\"(\S*?)\",", raw_stream_data)
    codecs = cdcs.split(",") if cdcs is not None else None

    video = locate_with_default(r"VIDEO=\"(\S*?)\"", raw_stream_data)
    resolution = locate_with_default(r"RESOLUTION=\"(\S*?)\"", raw_stream_data)

    return StreamVersionInfo(
        program_id=program_id,
        bandwidth=bandwidth,
        codecs=codecs,
        resolution=resolution,
        video=video,
        url=stream_url
    )


class StreamVersionInfo:
    """Class that represents the information regarding a particular stream
    version.
    """

    def __init__(
        self,
        program_id: int = None,
        bandwidth: int = None,
        codecs: str = None,
        resolution: str = None,
        video: str = None,
        url: str = None
    ):
        """
        """

        self.program_id = program_id
        self.bandwidth = bandwidth
        self.codecs = codecs if codecs is not None else []
        self.resolution = resolution
        self.video = video
        self.url = url


def strip_last_filename_from_url(url: str) -> str:
    """
    """

    path = "".join(reversed(url))
    index = path.find("/")

    if index == -1:
        return url
    else:
        return "".join(reversed(path[index:]))


def parse_stream_indexes_from_response(raw_index_response: str):
    """
    """

    indexes = []

    for row in raw_index_response.splitlines():
        ts_filename = locate_with_default(r"^(\d*.ts)$", row)
        if ts_filename:
            indexes.append(ts_filename)

    return indexes



class StreamIndexInfo:

    def __init__(self, base_url: str):
        self._base_url = base_url
        self.index_files = []

    def add_index(self, index_filename: str):
        self.index_files.append(index_filename)

    def index_paths(self):
        for index in self.index_files:
            yield (index, self._base_url + index,)
