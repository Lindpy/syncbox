from xmlprocessing import Lib


def selected_to_deezer(library: Lib, selected: list[str]):
    folders = [
        folder
        for folder in library.playlistdb.iloc[[int(i) - 1 for i in selected]]["folder"]
    ]

    return folders


def read_playlist():
    return


def fill_playlist():
    return


def complete_playlist():
    return
