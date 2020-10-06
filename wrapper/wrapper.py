import os
import shutil
from pathlib import Path

from mp3_tagger import MP3File, VERSION_2

from wrapper.result import Summary


def on_walk_error(error):
    print(error)


def check_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def parse_files(source, sink, recursive=False):
    source = Path(source)
    sink = Path(sink)
    check_dir(sink)
    result = Summary()
    # source_walk = os.walk(source, onerror=on_walk_error)
    file_list = []

    # source_dirpath, source_dir_names, source_file_names = source_walk.__next__()
    # for mp3_file_name in source_file_names:
    for mp3_file_name in source.iterdir():
        file_list.append(mp3_file_name.resolve())
        pass

    print(file_list)
    # if recursive:
    #     for source_dirpath, source_dir_names, source_file_names in source_walk:
    #         for mp3_file_name in source_file_names:
    #             file_list.append(os.path.join(source_dirpath, mp3_file_name))
    #
    # for mp3_file_name in file_list:
    #     result = process_file(mp3_file_name, sink, result)

    print(result)


def process_file(mp3_file_name: str, sink: Path, result: Summary, copy: bool = False) -> Summary:
    """
    Process a file as a MP3 file and move it to the corresponding folder.

    :param copy: bool
    :param mp3_file_name:
    :param sink:
    :param result:
    :return: Summary
    """
    try:
        file = MP3File(mp3_file_name)
        file.set_version(VERSION_2)
    except Exception as e:
        result.add_error({
            'file': mp3_file_name,
            'error': e,
        })
        return result
    track = ('00', file.track)[bool(file.track)]
    song = ('unknown', file.song)[bool(file.song)]
    album = ('unknown', file.album)[bool(file.album)]
    artist = ('unknown', file.artist)[bool(file.artist)]
    file_name = mp3_file_name.split(os.path.sep)[-1]
    sink_path = sink / artist / album
    try:
        check_dir(sink_path)
        if copy:
            shutil.copy(file.path, os.path.join(sink_path, file_name))
        else:
            os.rename(file.path, os.path.join(sink_path, file_name))
    except Exception as e:
        result.add_error({
            'file': mp3_file_name,
            'error': e,
        })
        return result

    processed = {
        'title': song,
        'track': track,
        'artist': artist,
        'album': album,
    }
    result.add_processed(processed)
    return result
