import os
import shutil

from mp3_tagger import MP3File, VERSION_2, MP3OpenFileError

from wrapper.result import Summary


def on_walk_error(error):
    print(error)


def check_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def parse_files(source, sink, recursive=False):
    check_dir(sink)
    result = Summary()
    source_walk = os.walk(source, onerror=on_walk_error)

    source_dirpath, source_dir_names, source_file_names = source_walk.__next__()
    print(f'source_dirpath={source_dirpath}')
    print(f'source_dir_names={source_dir_names}')
    print(f'source_file_names={source_file_names}')
    for mp3_file_name in source_file_names:
        process_file(os.path.join(source_dirpath, mp3_file_name), sink, result)

    if recursive:
        for source_dirpath, source_dir_names, source_file_names in source_walk:
            print(f'source_dirpath={source_dirpath}')
            print(f'source_dir_names={source_dir_names}')
            print(f'source_file_names={source_file_names}')
            for mp3_file_name in source_file_names:
                process_file(os.path.join(source_dirpath, mp3_file_name), sink, result)

    print(result)


def process_file(mp3_file_name: str, sink: str, result: Summary):
    """
    Process a file as a MP3 file and move it to the corresponding folder.
    :param mp3_file_name:
    :param sink:
    :param result:
    :return:
    """
    try:
        file = MP3File(mp3_file_name)
        file.set_version(VERSION_2)
    except MP3OpenFileError as e:
        result.add_error(mp3_file_name)
        return
    track = ('00', file.track)[bool(file.track)]
    print(f'track: {track}')
    song = ('unknown', file.song)[bool(file.song)]
    print(f'song: {song}')
    album = ('unknown', file.album)[bool(file.album)]
    print(f'album: {album}')
    artist = ('unknown', file.artist)[bool(file.artist)]
    print(f'artist: {artist}')
    sink_path = os.path.join(sink, album, artist)
    check_dir(sink_path)
    # os.rename(file.path, os.path.join(sink_path, f'{song}.mp3'))
    shutil.copy(file.path, os.path.join(sink_path, f'{song}.mp3'))
    result.add_moved(mp3_file_name)
