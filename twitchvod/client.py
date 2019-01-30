from typing import Optional, Mapping
import requests
from models import HttpMethod, parse_stream_info_from_response, \
    StreamVersionInfo, parse_stream_indexes_from_response, \
    strip_last_filename_from_url, StreamIndexInfo
from exceptions import HTTPClientError, HTTPServerError, HTTPGenericError


class Client:
    """HTTP Client to interact with the Twitch API to fetch VOD information.
    """

    TOKEN_PATTERN = "https://api.twitch.tv/api/vods/{vod_id}/access_token"
    VOD_M3U8_PATTERN = "https://usher.ttvnw.net/vod/{vod_id}.m3u8"

    USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Ubuntu Chromium/71.0.3578.98 " +
        "Chrome/71.0.3578.98 Safari/537.36"
    )

    def __init__(self, client_id: str):
        self._client_id = client_id

    def _send_request(
            self,
            method: HttpMethod,
            path: str,
            params=None
    ) -> requests.Response:
        """Send a request to the specified HTTP/API endpoint.
        """

        if headers is not None:
            headers = self._apply_useragent(headers)

        http_response = requests.request(
            method.value,
            path,
            params=params,
        )

        self._raise_on_status(http_response)

        return http_response

    def _apply_useragent(self, headers: dict) -> dict:
        """Apply a default useragent to the headers param.
        """

        if "user-agent" not in headers:
            headers["User-Agent"] = self.USER_AGENT

        return headers

    def _raise_on_status(self, response: requests.Response) -> None:
        """Inspect the status on the response parameter and raise the matching
        client exception.
        """

        stat = response.status_code

        if stat in range(400, 500):
            raise HTTPClientError(
                "Client HTTP error code. Status={0}".format(stat)
            )
        elif stat in range(500, 600):
            raise HTTPServerError(
                "Server HTTP error code. Status={0}".format(stat)
            )
        elif stat not in range(200, 300):
            raise HTTPGenericError(
                "Generic HTTP error code. Status={0}".format(stat)
            )

    def get_vod_access_token(self, vod_id: str) -> dict:
        """
        """

        response = self._send_request(
            HttpMethod.GET,
            self.TOKEN_PATTERN.format(vod_id=vod_id),
            params={"client_id": self._client_id}
        )

        return response.json()

    def _get_vod_m3u8_refs(
        self,
        access_token: dict,
        vod_id: str
    ):
        """
        """

        req_params = {
            "client_id": self._client_id,
            "token": access_token["token"],
            "sig": access_token["sig"],
            "allow_source": "true",
            "allow_audio_only": "true"
        }

        raw_resp = self._send_request(
            HttpMethod.GET,
            self.VOD_M3U8_PATTERN.format(vod_id=vod_id),
            params=req_params
        )

        return raw_resp.text

    def get_stream_info(self, vod_access_token: dict, vod_id):
        """
        """

        return parse_stream_info_from_response(
            self._get_vod_m3u8_refs(vod_access_token, vod_id)
        )

    def get_stream_indexes(self, stream_version: StreamVersionInfo):
        """
        """

        index_resp = self._send_request(
            HttpMethod.GET,
            stream_version.url
        )

        base_url = strip_last_filename_from_url(stream_version.url)
        index_names = parse_stream_indexes_from_response(index_resp.text)

        indexes = StreamIndexInfo(base_url)

        for index in index_names:
            indexes.add_index(index)

        return indexes
