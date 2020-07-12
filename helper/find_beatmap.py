from struct import unpack_from
import osrparse
import logging


def parseNum(db, offset, length):
    typeMap = {1:'B', 2:'H', 4:'I', 8:'Q'}
    numType = typeMap[length]
    val = unpack_from(numType, db, offset)[0]
    return (val, offset+length)

def parseDate(db, offset):
    val = unpack_from('Q', db, offset)[0]
    return ((val / 10000) - 62135769600000, offset+8)

def parseFloat(db, offset, length):
    typeMap = {4:'f', 8:'d'}
    numType = typeMap[length]
    val = unpack_from(numType, db, offset)[0]
    return (val, offset+length)

def parseBool(db, offset):
    val = unpack_from('b', db, offset)[0]
    if val == 0x00:
        return (False, offset+1)
    else:
        return (True, offset+1)

def parseString(db, offset):
    existence = unpack_from('b', db, offset)[0]
    if existence == 0x00:
        return ("", offset+1)
    elif existence == 0x0b:
        # decode ULEB128
        length = 0
        shift = 0
        offset += 1
        while True:
            val = unpack_from('B', db, offset)[0]
            length |= ((val & 0x7F) << shift)
            offset += 1
            if (val & (1 << 7)) == 0:
                break
            shift += 7

        string = unpack_from(str(length)+'s', db, offset)[0]
        offset += length

        unic = u''
        try:
            unic = str(string, 'utf-8')
        except UnicodeDecodeError:
            print("Could not parse UTF-8 string, returning empty string.")

        return (unic, offset)

def parseFastBeatmap(db, offset):
    beatmap = {}
    beatmap['artist_name'], offset = parseString(db, offset)
    beatmap['artist_uname'], offset = parseString(db, offset)
    beatmap['song_title'], offset = parseString(db, offset)
    beatmap['song_utitle'], offset = parseString(db, offset)
    beatmap['creator_name'], offset = parseString(db, offset)
    beatmap['version'], offset = parseString(db, offset)
    beatmap['audio_file'], offset = parseString(db, offset)
    beatmap['file_md5'], offset = parseString(db, offset)
    beatmap['osu_file'], offset = parseString(db, offset)
    # offset += 1
    # offset += 2
    # offset += 2
    # offset += 2
    # offset += 8
    # offset += 4
    # offset += 4
    # offset += 4
    # offset += 4
    # offset += 8

    offset += 39

    # pre-computed difficulties for various mod combinations
    for i in range(0, 4):
        numPairs, offset = parseNum(db, offset, 4)
        offset += 14 * numPairs
        # for j in range(0, numPairs):
        #     # offset += 1
        #     # offset += 4
        #     # offset += 1
        #     # offset += 8
        #     offset += 14



    offset += 4
    offset += 4
    offset += 4

    numPoints, offset = parseNum(db, offset, 4)
    offset += 17 * numPoints
    # for i in range(0, numPoints):
    #     # tp, offset = parseTimingPoint(db, offset)
    #     # offset += 17

    beatmap['beatmap_id'], offset = parseNum(db, offset, 4)
    beatmap['set_id'], offset = parseNum(db, offset, 4)
    beatmap['thread_id'], offset = parseNum(db, offset, 4)

    # 4 unknown bytes
    # offset += 4

    # offset += 2
    # offset += 4
    # offset += 1
    offset += 11
    beatmap['source'], offset = parseString(db, offset)
    beatmap['tags'], offset = parseString(db, offset)
    offset += 2
    beatmap['title_font'], offset = parseString(db, offset)
    # offset += 1
    # offset += 8
    # offset += 1
    offset += 10
    beatmap['folder_name'], offset = parseString(db, offset)
    beatmap['last_checked'], offset = parseDate(db, offset)
    beatmap['ignore_sounds'], offset = parseBool(db, offset)
    beatmap['ignore_skin'], offset = parseBool(db, offset)
    beatmap['disable_storyboard'], offset = parseBool(db, offset)
    beatmap['disable_video'], offset = parseBool(db, offset)
    beatmap['visual_override'], offset = parseBool(db, offset)
    # offset += 4
    # offset += 1

    offset += 5

    return (beatmap, offset)

def parseTimingPoint(db, offset):
    tp = {}
    mpb, offset = parseFloat(db, offset, 8)
    tp['bpm'] = round(1.0 / mpb * 1000 * 60, 3)
    tp['offset'], offset = parseFloat(db, offset, 8)
    tp['inherited'], offset = parseBool(db, offset)

    tp['inherited'] = not tp['inherited']

    return (tp, offset)


# parses the osu!.db file
def getMapInfo(db, hash):
    offset = 0
    data = {}
    data['version'], offset = parseNum(db, offset, 4)
    data['folder_count'], offset = parseNum(db, offset, 4)
    data['account_unlocked'], offset = parseBool(db, offset)

    data['unlock_date'], offset = parseNum(db, offset, 8)
    data['name'], offset = parseString(db, offset)
    data['num_beatmaps'], offset = parseNum(db, offset, 4)

    data['beatmaps'] = {}
    for i in range(0, data['num_beatmaps']):
        beatmap, offset = parseFastBeatmap(db, offset)
        if beatmap['file_md5'] == hash:
            return beatmap

    return None

def find_beatmap_(replay_path,osu_path):
    replayfile = osrparse.parse_replay_file(replay_path)
    osuDb = open(osu_path + '/osu!.db', "rb")
    beatmap = getMapInfo(osuDb.read(), replayfile.beatmap_hash)
    osuDb.close()
    try:
        logging.info("Loaded beatmap folder {}".format(beatmap["folder_name"]))
        return beatmap["folder_name"]
    except Exception as e:
        logging.error(repr(e))
