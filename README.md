Twitchvod (v0.1.0) [![Build Status](https://travis-ci.com/nomadmtb/twitchvod.svg?branch=master)](https://travis-ci.com/nomadmtb/twitchvod)
=========

##### Installation
`pip install twitchvod`

---

##### Compatibility
This package is python3 compatible. There is no support for python2 currently.

`>= python 3.5.2`

---

**Please note that this library is to be used at your own risk. Using undocumented api interfaces is against the Twitch terms of service. I take no responsibility if your developer tokens get
revoked etc. However, if you would like to learn how this library works, please feel free to read through the source.**

Okay now for the more interesting stuff.

---

This API client will use your provided Twitch developer client_id to make several requests to Twitch API endpoints to fetch information related to a particular VOD. You can even query for all of the MPEG-2 Transport Stream files to which you can download however you wish. For this example, let's say you want to download VOD [372739399](https://www.twitch.tv/videos/372739399).

```
>>> from twitchvod import Client

# Create client...
>>> client = Client("TWITCH-DEV-APP-CLIENT-ID")
>>> client
<Client>

# Generate access token for VOD 372739399...
>>> token = client.get_access_token(372739399)
>>> token
<AccessToken [372739399-vod_id]>

# Fetch the different vod qualities w/ token...
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

# Get VOD chunks... There are 364 of them...
>>> vod_chunk = client.get_chunks(vods[0])
>>> vod_chunk
<VodChunk [364-chunks]>

# Get the MPEG-2 transport stream files... Boom!
>>> mpeg2_ts_chunks = [c for c in vod_chunks.chunks()]
>>> mpeg2_ts_chunks[:3]
[
    ('1988.ts', 'https://vod-metro.twitch.tv/.../chunked/1988.ts'),
    ('1989.ts', 'https://vod-metro.twitch.tv/.../chunked/1989.ts'),
    ('1990.ts', 'https://vod-metro.twitch.tv/.../chunked/1990.ts')
]
```

---

##### Development Environment / Setup
This package is early in development, so if anyone has any questions or concerns you can raise a PR or Issue on the github repo.

[nomadmtb/twitchvod on GitHub](https://github.com/nomadmtb/twitchvod)

1. Git clone the above repo.
`git clone git@github.com:nomadmtb/twitchvod.git`
2. Move into the project.
`cd twitchvod`
3. Create virtualenv (assuming your have 3.7)
`python3.7 -m venv .env`
4. Activate virtualenv.
`source .env/bin/activate`
5. Install dev requirements.
`pip install -r requirements.txt`

With the above set-up you can perform the following to get started.

1. Run the unittests w/ pytest.
`make test`
2. Run the unittests w/ coverage + pytest.
`make coverage`
3. Install a local copy of the package.
`python setup.py install`
4. Remove the local copy of the package.
`pip uninstall twitchvod`
