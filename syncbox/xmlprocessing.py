from pydantic import BaseModel
import inspect
from typing import Type
import xml.etree.ElementTree as ET
from pathlib import Path

XMLDIR = Path("xml_here")
ARGMAP = {"trackid": "id"}


def classdict(data: dict[str, str], class_: Type, mapping=ARGMAP) -> dict:
    valid_keys = set(inspect.signature(class_).parameters.keys())
    cleandict = {}
    for K, v in data.items():
        k = K.lower()
        if k in mapping:
            k = mapping[k]
        if k in valid_keys:
            cleandict[k] = v
    return cleandict


class Track(BaseModel):
    id: int | None = None
    name: str | None = None
    artist: str | None = None
    album: str | None = None


class Playlistbranch(BaseModel):
    name: str
    track_ids: list[int] | None = []
    leaves: list["Playlistbranch"] = []
    def get_cumulated_leaves_id(self):
        self.leaves_ids = self.track_ids
        if not self.leaves:
            return
        for leaf in self.leaves:
            self.get_cumulated_leaves_id(leaf)
            self.leaves_ids.extend(leaf.leaves_ids)


class Lib(BaseModel):
    tracks: list[Track] | None = None
    playlist: Playlistbranch | None = None
    mapping: dict | None = None
    model_config = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context=None):
        self.mapping = {track.id: track for track in self.tracks}


def xml_to_dict(elem):
    node = {}
    if elem.attrib:
        node["@attributes"] = elem.attrib
    children = list(elem)
    if children:
        child_dict = {}
        for child in children:
            child_data = xml_to_dict(child)
            tag = child.tag
            if tag not in child_dict:
                child_dict[tag] = (
                    child_data if not isinstance(child_data, list) else child_data
                )
            else:
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_data)
        node.update(child_dict)
    else:
        node = elem.text.strip() if elem.text else None
        if elem.attrib:
            node = {"@attributes": elem.attrib, "#text": node}
    return node


def build_playlist_tree(playlistdict: dict) -> Playlistbranch:
    if "@attributes" not in playlistdict:
        return build_playlist_tree(playlistdict["NODE"])
    branch = Playlistbranch(name=playlistdict["@attributes"]["Name"])

    if "NODE" in playlistdict:  # iterate per sub playlist
        if not isinstance(playlistdict["NODE"], list):
            playlistdict["NODE"] = [playlistdict["NODE"]]
        for leavedict in playlistdict["NODE"]:
            branch.leaves.append(build_playlist_tree(leavedict))

    if "TRACK" in playlistdict:
        if not isinstance(playlistdict["TRACK"], list):
            playlistdict["TRACK"] = [playlistdict["TRACK"]]
        for track in playlistdict["TRACK"]:
            branch.track_ids.append(track["@attributes"]["Key"])

    return branch


def parse_xml_data(folder=XMLDIR) -> Lib:
    files = [f for f in folder.glob("*.xml")]
    if len(files) != 1:
        raise ValueError(f"{len(files)} xml files found in xml_here folder, expected 1")
    tree = ET.parse(str(files[0]))
    root = tree.getroot()
    data = {root.tag: xml_to_dict(root)}
    trackdicts = [
        track["@attributes"] for track in data["DJ_PLAYLISTS"]["COLLECTION"]["TRACK"]
    ]
    playlist = build_playlist_tree(data["DJ_PLAYLISTS"]["PLAYLISTS"])
    lib = Lib(
        tracks=[Track(**classdict(track, Track)) for track in trackdicts],
        playlist=playlist,
    )
    return lib
