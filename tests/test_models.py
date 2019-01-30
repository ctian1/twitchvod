"""test_models.py"""

import unittest
from twitchvod import models
from . import mocks


class TestModels(unittest.TestCase):
    """Test twitchvod.models"""

    def test_httpmethod_enum(self):
        """Test to make sure the correct strings are getting used as values
        for the HttpMethod enum.
        """

        method = models.HttpMethod

        self.assertEqual(method.GET.value, "GET")
        self.assertEqual(method.POST.value, "POST")
        self.assertEqual(method.HEAD.value, "HEAD")
        self.assertEqual(method.PUT.value, "PUT")

    def test_get_ext_media_indexes(self):
        """Test to make sure that the correct indexes are returned based on
        the provided sample records.
        """

        expected = [(2, 3,), (6, 7,)]
        actual = models.get_ext_media_indexes(
            mocks.MOCK_STREAM_VARIATION_RECORDS
        )
        self.assertEqual(actual, expected)

    def test_parse_stream_info_from_response(self):
        """Test to make sure correct list of Vod objects are
        returned for the specified sample input.
        """

        mock_m3u8_data = "\n".join(mocks.MOCK_STREAM_VARIATION_RECORDS)

        exp_f = models.Vod(
            program_id=1,
            bandwidth=286082,
            codecs=["avc1.4D400C", "mp4a.40.2"],
            resolution="284x160",
            video="160p30",
            url=("https://vod-metro.twitch.tv/bccf6e16a67fe2619f56"
                 "_channel_32415582688_1094599349/160p30/index-dvr.m3u8")
        )

        exp_s = models.Vod(
            program_id=1,
            bandwidth=3297816,
            codecs=["avc1.64002A", "mp4a.40.2"],
            resolution="1920x1080",
            video="chunked",
            url=("https://vod-metro.twitch.tv/bccf6e16a67fe2619f56"
                 "_channel_32415582688_1094599349/chunked/index-dvr.m3u8")
        )

        actual = models.parse_stream_info_from_response(mock_m3u8_data)
        self.assertEqual(actual[0], exp_f)
        self.assertEqual(actual[1], exp_s)

    def test_stream_version_info_from_raw(self):
        """Test to make sure the correct Vod object is returned
        from the method for the specified info and url.
        """

        mock_record = mocks.MOCK_STREAM_INFO_RECORD

        url = ("https://vod-metro.twitch.tv/bccf6e16a67fe2619f56"
               "_channel_32415582688_1094599349/160p30/index-dvr.m3u8")

        exp = models.Vod(
            program_id=1,
            bandwidth=286082,
            codecs=["avc1.4D400C", "mp4a.40.2"],
            resolution="284x160",
            video="160p30",
            url=url
        )

        actual = models.parse_stream_version_info_from_raw(mock_record, url)
        self.assertEqual(actual, exp)

    def test_strip_last_filename_from_url(self):
        """Test to make sure the correct url segment is returned with a given
        input url that contains a trailing filename.
        """

        url = "https://utldr.co/a/robots.txt"

        expected = "https://utldr.co/a/"
        actual = models.strip_last_filename_from_url(url)
        self.assertEqual(actual, expected)

    def test_strip_last_filename_from_url_with_no_seperator(self):
        """Test to make sure the original url segment is returned with a given
        input url that does not contain the seperator.
        """

        url = "google.com"

        actual = models.strip_last_filename_from_url(url)
        self.assertEqual(actual, url)

    def test_strip_last_filename_from_url_with_custom_seperator(self):
        """Test to make sure the correct url segment is returned with a given
        input url and custom seperator character.
        """

        url = "http:||utldr.co|a|b|robots.txt"

        expected = "http:||utldr.co|a|b|"
        actual = models.strip_last_filename_from_url(url, sep="|")
        self.assertEqual(actual, expected)

    def test_parse_stream_indexes_from_response(self):
        """Test to make sure the correct MPEG-2 index files are extracted from
        the HTTP response content.
        """

        expected = ["{}.ts".format(i) for i in range(11)]
        actual = models.parse_stream_indexes_from_response(
            mocks.MOCK_STREAM_INDEX_DATA
        )
        self.assertEqual(actual, expected)

    def test_streamindexinfo_chunks(self):
        """Test to make sure that the VodChunk class generates the
        correct MPEG-2 transport filepaths for a given input.
        """

        base_url = "https://utldr.co/ts/"
        stream_indexes = models.VodChunk(base_url)

        ts_files = ["{}.ts".format(i) for i in range(10)]
        for ts_name in ts_files:
            stream_indexes.add_chunk(ts_name)

        actual = [i for i in stream_indexes.chunks()]
        expected = [(filename, base_url+filename,) for filename in ts_files]
        self.assertEqual(actual, expected)

    def test_streamindexinfo_add_chunk(self):
        """Probably not needed, but testing that the add_chunk method works
        correctly when a user attempts to add an index file.
        """

        base_url = "https://utldr.co/ts/"
        stream_indexes = models.VodChunk(base_url)

        ts_files = ["{}.ts".format(i) for i in range(10)]
        for ts_name in ts_files:
            stream_indexes.add_chunk(ts_name)

        #pylint: disable=protected-access
        self.assertEqual(stream_indexes._index_files, ts_files)
