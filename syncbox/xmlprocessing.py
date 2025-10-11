import inspect
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Type

import pandas as pd
from pydantic import BaseModel

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XMLDIR = Path("xml_here")
ARCHIVEDIR = Path("syncbox/archive_xml/")
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
    db_id: int
    track_ids: list[int] | None = []
    leaves: list["Playlistbranch"] = []
    fullname: str

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
    playlistdb: pd.DataFrame | None = None
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


def build_playlist_tree(
    playlistdict: dict,
    playlistdb: pd.DataFrame | None = None,
    rootname: str | None = None,
) -> Playlistbranch:
    if playlistdb is None:
        playlistdb = pd.DataFrame(columns=["folder"])

    if "@attributes" not in playlistdict:
        return build_playlist_tree(playlistdict["NODE"], playlistdb)

    id = playlistdb.shape[0] + 1
    folder = playlistdict["@attributes"]["Name"]
    fullpath = rootname + "-" + folder if rootname else folder
    branch = Playlistbranch(name=folder, fullname=fullpath, db_id=id)
    playlistdb.loc[id] = [branch]  # inplace modification

    if "NODE" in playlistdict:  # iterate per sub playlist
        if not isinstance(playlistdict["NODE"], list):
            playlistdict["NODE"] = [playlistdict["NODE"]]
        for leavedict in playlistdict["NODE"]:
            branch.leaves.append(
                build_playlist_tree(leavedict, rootname=fullpath, playlistdb=playlistdb)
            )

    if "TRACK" in playlistdict:
        if not isinstance(playlistdict["TRACK"], list):
            playlistdict["TRACK"] = [playlistdict["TRACK"]]
        for track in playlistdict["TRACK"]:
            branch.track_ids.append(track["@attributes"]["Key"])

    return branch


def parse_xml_data(
    folder: Path = Path(os.path.join(ROOT, XMLDIR)),
    archivefolder: Path = Path(os.path.join(ROOT, ARCHIVEDIR)),
) -> Lib:
    files = [f for f in folder.glob("*.xml")]
    ctimes = [(os.path.getctime(file)) for file in files]
    pairs = [[ctime, file] for ctime, file in zip(ctimes, files)]
    pairs.sort()
    if len(pairs) > 1:
        for pair in pairs[:-1]:
            oldfn = pair[1]
            new_fn = "rblib-" + str(datetime.fromtimestamp(pair[0]).date()) + ".xml"
            os.rename(
                oldfn, os.path.join(archivefolder, new_fn)
            )  # moving files to archive

    tree = ET.parse(str(pairs[-1][1]))  # oldest one
    root = tree.getroot()
    data = {root.tag: xml_to_dict(root)}
    trackdicts = [
        track["@attributes"] for track in data["DJ_PLAYLISTS"]["COLLECTION"]["TRACK"]
    ]
    playlistdb = pd.DataFrame(columns=["folder"])
    playlist = build_playlist_tree(
        data["DJ_PLAYLISTS"]["PLAYLISTS"], playlistdb=playlistdb
    )
    lib = Lib(
        tracks=[Track(**classdict(track, Track)) for track in trackdicts],
        playlist=playlist,
        playlistdb=playlistdb,
    )
    return lib


# def scan_xml():

parse_xml_data()
