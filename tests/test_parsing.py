from syncbox.xmlprocessing import parse_xml_data
from pathlib import Path
from inline_snapshot import snapshot
import pytest


@pytest.fixture
def expected_lib():
    return snapshot(
        {
            "tracks": [
                {
                    "id": None,
                    "name": "Thank You (MPH Remix)",
                    "artist": "Todd Edwards",
                    "album": "Thank You (MPH Remix)",
                },
                {
                    "id": None,
                    "name": "Smooth Operator (House Remix - Sped Up)",
                    "artist": "Stutter",
                    "album": "Smooth Operator (House Remix - Sped Up)",
                },
                {
                    "id": None,
                    "name": "Waiting",
                    "artist": "MPH/Katie Bosworth",
                    "album": "Waiting",
                },
                {"id": None, "name": "Useless", "artist": "MPH", "album": "Nova"},
                {
                    "id": None,
                    "name": "Work (Original Mix)",
                    "artist": "Higgo",
                    "album": "'95",
                },
            ],
            "playlist": {
                "track_ids": [],
                "name": "ROOT",
                "leaves": [
                    {"track_ids": ["61120378"], "name": "playlist 1", "leaves": []},
                    {
                        "track_ids": [],
                        "name": "group 1",
                        "leaves": [
                            {
                                "track_ids": ["109098778"],
                                "name": "playlist 2",
                                "leaves": [],
                            },
                            {
                                "track_ids": ["55909356", "127122428", "61120378"],
                                "name": "playlist 3",
                                "leaves": [],
                            },
                        ],
                    },
                ],
            },
        }
    )


def test_libgen(expected_lib):
    path = Path("tests/testxmls")
    lib = parse_xml_data(folder=path)
    assert lib.model_dump() == expected_lib
