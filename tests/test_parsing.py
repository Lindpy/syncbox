from pathlib import Path

import pytest
from inline_snapshot import snapshot

from syncbox.xmlprocessing import parse_xml_data


@pytest.fixture
def expected_lib():
    return snapshot(
        {
            "tracks": [
                {
                    "id": 55909356,
                    "name": "Thank You (MPH Remix)",
                    "artist": "Todd Edwards",
                    "album": "Thank You (MPH Remix)",
                },
                {
                    "id": 127122428,
                    "name": "Smooth Operator (House Remix - Sped Up)",
                    "artist": "Stutter",
                    "album": "Smooth Operator (House Remix - Sped Up)",
                },
                {
                    "id": 152468503,
                    "name": "Waiting",
                    "artist": "MPH/Katie Bosworth",
                    "album": "Waiting",
                },
                {"id": 61120378, "name": "Useless", "artist": "MPH", "album": "Nova"},
                {
                    "id": 109098778,
                    "name": "Work (Original Mix)",
                    "artist": "Higgo",
                    "album": "'95",
                },
            ],
            "playlist": {
                "name": "ROOT",
                "track_ids": [],
                "leaves": [
                    {"name": "playlist 1", "track_ids": ["61120378"], "leaves": []},
                    {
                        "name": "group 1",
                        "track_ids": [],
                        "leaves": [
                            {
                                "name": "playlist 2",
                                "track_ids": ["109098778"],
                                "leaves": [],
                            },
                            {
                                "name": "playlist 3",
                                "track_ids": ["55909356", "127122428", "61120378"],
                                "leaves": [],
                            },
                        ],
                    },
                ],
            },
            "mapping": {
                55909356: {
                    "id": 55909356,
                    "name": "Thank You (MPH Remix)",
                    "artist": "Todd Edwards",
                    "album": "Thank You (MPH Remix)",
                },
                127122428: {
                    "id": 127122428,
                    "name": "Smooth Operator (House Remix - Sped Up)",
                    "artist": "Stutter",
                    "album": "Smooth Operator (House Remix - Sped Up)",
                },
                152468503: {
                    "id": 152468503,
                    "name": "Waiting",
                    "artist": "MPH/Katie Bosworth",
                    "album": "Waiting",
                },
                61120378: {
                    "id": 61120378,
                    "name": "Useless",
                    "artist": "MPH",
                    "album": "Nova",
                },
                109098778: {
                    "id": 109098778,
                    "name": "Work (Original Mix)",
                    "artist": "Higgo",
                    "album": "'95",
                },
            },
        }
    )


def test_libgen(expected_lib):
    path = Path("tests/testxmls")
    lib = parse_xml_data(folder=path)
    assert lib.model_dump() == expected_lib
