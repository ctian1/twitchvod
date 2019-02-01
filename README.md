Twitchvod [![Build Status](https://travis-ci.com/nomadmtb/twitchvod.svg?branch=master)](https://travis-ci.com/nomadmtb/twitchvod)
=========

**Please note that this library is to be used at your own risk. Using undocumented api interfaces is against the Twitch terms of service. I take no responsibility if your developer tokens get
revoked etc. However, if you would like to learn how this library works, please feel free to read through the source.**

Okay now for the more interesting stuff.

This API client will use your provided Twitch developer client_id to make several requests to Twitch API endpoints to fetch information related to a particular VOD. You can even query for all of the MPEG-2 Transport Stream files to which you can download however you wish. For this example, let's say you want to download VOD [372739399](https://www.twitch.tv/videos/372739399).

```
>>> from twitchvod import Client

>>> client = Client("YOUR-TWITCH-DEV-CLIENT-ID")

>>> token = client.get_access_token()
>>> token
<AccessToken [372739399-vod_id]>

>>> vods = client.get_vods(token)
>>> vods
[
    <Vod [chunked,1920x1080]>,
    <Vod [720p60,1280x720]>,
    <Vod [720p30,1280x720]>,
    <Vod [480p30,852x480]>,
    <Vod [audio_only]>,
    <Vod [360p30,640x360]>,
    <Vod [160p30,284x160]>
]

>>> vod = client.get_chunks(vods[0])
>>> vod
<Vod [chunked,1920x1080]>

>>> mpeg2_ts_chunks = [c for c in vod.chunks()]
>>> mpeg2_ts_chunks[:3]
[
    ('1988.ts', 'https://vod-metro.twitch.tv/.../chunked/1988.ts'),
    ('1989.ts', 'https://vod-metro.twitch.tv/.../chunked/1989.ts'),
    ('1990.ts', 'https://vod-metro.twitch.tv/.../chunked/1990.ts')
]
```
