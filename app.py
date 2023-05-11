#!/usr/bin/env python3

from pathlib import Path

import shutil
import os
import struct
import json
import random
import datetime
import re
import requests
import imutils
import cv2
import numpy
import unidecode


def swap32(i):
    return struct.unpack('<I', struct.pack('>I', i))[0]


def swap16(i):
    return struct.unpack('<H', struct.pack('>H', i))[0]


def image_resize(image, width):
    arr = numpy.asarray(bytearray(image), dtype=numpy.uint8)
    img = cv2.imdecode(arr, -1)
    img = imutils.resize(img, width=width)
    result, img = cv2.imencode('.png', img)

    if result is True:
        return img

    return image


def normalize(name):
    name = unidecode.unidecode(name)
    name = re.sub(r'\.', '', name)
    return name


def get_amiibos():
    url = 'https://www.amiiboapi.com/api/amiibo'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['amiibo']

    return None


def get_amiibo_duplicates(amiibos, amiibo):
    duplicates = []
    for i in amiibos:
        if amiibo['head'] + amiibo['tail'] != i['head'] + i['tail']:
            if amiibo['name'] == i['name'] and amiibo['amiiboSeries'] == i['amiiboSeries']:
                duplicates.append(i)
    return duplicates


def move_areas():
    # Set paths
    source_path = "areas/0x1019C800.bin"
    destination_path = "data/Legend Of Zelda/Midna & Wolf Link/areas"

    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Copy file to destination directory
    shutil.copy(source_path, destination_path)


def main():
    date = datetime.datetime.today()
    amiibos = get_amiibos()

    move_areas()

    for index, amiibo in enumerate(amiibos):
        amiibo_id = amiibo['head'] + amiibo['tail']
        amiibo_name = normalize(amiibo['name'])
        amiibo_series = normalize(amiibo['amiiboSeries'])
        amiibo_data = {
            'name': amiibo_name,
            'write_counter': 0,
            'version': 0,
            'mii_charinfo_file': 'mii-charinfo.bin',
            'first_write_date': {
                'y': int(date.strftime('%Y')),
                'm': int(date.strftime('%m')),
                'd': int(date.strftime('%d'))
            },
            'last_write_date': {
                'y': int(date.strftime('%Y')),
                'm': int(date.strftime('%m')),
                'd': int(date.strftime('%d'))
            },
            'id': {
                'game_character_id': swap16(int(amiibo_id[0:4], base=16)),
                'character_variant': int(amiibo_id[4:6], base=16),
                'figure_type': int(amiibo_id[6:8], base=16),
                'series': int(amiibo_id[12:14], base=16),
                'model_number': int(amiibo_id[8:12], base=16)
            },
            "uuid": [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                0,
                0,
                0
            ]
        }

        print(f"Creating {amiibo_name} ({index+1}/{len(amiibos)})")

        if len(get_amiibo_duplicates(amiibos, amiibo)) > 0:
            filename = f'data/{amiibo_series}/{amiibo_name} ({amiibo["release"]["jp"]})'
        else:
            filename = f'data/{amiibo_series}/{amiibo_name}'

        path = Path(filename)
        path.mkdir(parents=True, exist_ok=True)

        # Json
        with Path(path / 'amiibo.json').open('w', encoding='UTF-8') as output:
            json.dump(amiibo_data, output, sort_keys=False,
                      ensure_ascii=False, indent=2)

        # Flag
        Path(path / 'amiibo.flag').touch()

        # Image
        image = requests.get(amiibo['image'])

        if image.status_code == 200:

            with Path(path / 'amiibo.png').open('wb') as output:
                # output.write(image.content)
                output.write(image_resize(image.content, width=200).tobytes())


if __name__ == '__main__':
    main()
