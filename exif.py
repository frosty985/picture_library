import os
import exifread
from fractions import Fraction


def _get_if_exist(data, key):
    """
    Checks key has data
    :param data:
    :param key:
    :return value:
    """
    if key in data:
        return data[key]
    return None


def _convert_to_degress(value):
    """
    Takes lon/lat as Deg, Min, Sec and turns to decimal
    :param value:
    :return lon/lat.dec:
    """
    d = float(Fraction(str(value.values[0])))
    m = float(Fraction(str(value.values[1])))
    s = float(Fraction(str(value.values[2])))
    return round(d + (m / 60.0) + (s / 3600.0),7)


def get_lat_lon(file_to_process):
    """
    Gets lat,lon from exif
    :param file_to_process:
    :return lat,lon:
    """
    lat = None
    lon = None
    gps_latitude = _get_if_exist(file_to_process, "GPS GPSLatitude")
    if gps_latitude is not None:
        gps_latitude_ref = _get_if_exist(file_to_process, 'GPS GPSLatitudeRef').values
    gps_longitude = _get_if_exist(file_to_process, 'GPS GPSLongitude')
    if gps_longitude is not None:
        gps_longitude_ref = _get_if_exist(file_to_process, 'GPS GPSLongitudeRef').values

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        lon = _convert_to_degress(gps_longitude)

        if gps_latitude_ref != "N":
            lat = 0 - lat
        if gps_longitude_ref != "E":
            lon = 0 - lon
    return lat, lon

def get_lat(file_to_process):
    """
    Gets lat,lon from exif
    :param file_to_process:
    :return lat,lon:
    """
    lat = None
    lon = None
    gps_latitude = _get_if_exist(file_to_process, "GPS GPSLatitude")
    gps_latitude_ref = _get_if_exist(file_to_process, 'GPS GPSLatitudeRef').values
    gps_longitude = _get_if_exist(file_to_process, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(file_to_process, 'GPS GPSLongitudeRef').values

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        lon = _convert_to_degress(gps_longitude)

        if gps_latitude_ref != "N":
            lat = 0 - lat
        if gps_longitude_ref != "E":
            lon = 0 - lon
    return lat

def get_lon(file_to_process):
    """
    Gets lat,lon from exif
    :param file_to_process:
    :return lat,lon:
    """
    lat = None
    lon = None
    gps_latitude = _get_if_exist(file_to_process, "GPS GPSLatitude")
    gps_latitude_ref = _get_if_exist(file_to_process, 'GPS GPSLatitudeRef').values
    gps_longitude = _get_if_exist(file_to_process, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(file_to_process, 'GPS GPSLongitudeRef').values

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        lon = _convert_to_degress(gps_longitude)

        if gps_latitude_ref != "N":
            lat = 0 - lat
        if gps_longitude_ref != "E":
            lon = 0 - lon
    return lon

def make_model(file_to_process):
    """
    Finds make and model of camera that took the picture
    :param file_to_process:
    :return make and model:
    """
    make = _get_if_exist(file_to_process, "Image Make")
    model = _get_if_exist(file_to_process, "Image Model")
    return "%s, %s" % (make, model)


def make(file_to_process):
    """
    Finds make and model of camera that took the picture
    :param file_to_process:
    :return make and model:
    """
    make = _get_if_exist(file_to_process, "Image Make")
    return make

def model(file_to_process):
    """
    Finds make and model of camera that took the picture
    :param file_to_process:
    :return make and model:
    """
    model = _get_if_exist(file_to_process, "Image Model")
    return model

def timestamp(file_to_process):
    """
    Get timestamp from image
    :param file_to_process:
    :return timestamp:
    """
    stamp = _get_if_exist(file_to_process, "EXIF DateTimeOriginal")
    stamp = str(stamp).replace(':', '-', 2)
    return "%s" % (stamp)


def imgDetails(imgName):
    """

    :param imgName:
    :return timestamp, resolution, lat/lon, make/model:
    """
    if (os.path.exists(imgName) == False):
        print("\nFile " + imgName + " does not exist")
        exit()
    try:
        file = open(imgName, 'rb')
        tags = exifread.process_file(file)
    except Exception as e:
        print("\nThere has been an error processing file: " + imgName)
        exit()

    """for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print("Key: %s, value %s" % (tag, tags[tag]))"""

    if str(_get_if_exist(tags, "Image Orientation"))[:10] == "Horizontal":
        resolution = str(_get_if_exist(tags, "EXIF ExifImageWidth")) + "," + str(_get_if_exist(tags, "EXIF ExifImageLength"))
    else:
        resolution = str(_get_if_exist(tags, "EXIF ExifImageLength")) + "," + str(_get_if_exist(tags, "EXIF ExifImageWidth"))

    return timestamp(tags), resolution, get_lat(tags), get_lon(tags), make(tags), model(tags)
