from pydantic import BaseModel
import pandas as pd



class TRACK(BaseModel):
    id:int|None = None
    name:str|None = None
    artist:str|None = None
    album:int|None = None
    initdict:dict[str,str]|None = None
    def __post_init__(self):
        if self.initdict:
            self.id=self.initdict['TrackID']
            self.name=self.initdict['Name']
            self.artist=self.initdict['Artist']
            self.album=self.initdict['Album']


class PLAYLIST(BaseModel):
    i:int


class LIB(BaseModel):
    tracks:list[TRACK]|None = None
    playlists:list[PLAYLIST]|None = None

    def __post_init__(self):
        self.mapping=pd.DataFrame([{int(track.id):track} for track in self.tracks])