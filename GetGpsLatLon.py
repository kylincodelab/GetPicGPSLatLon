#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-24 15:10:34
# @Author  : lazynms (admin@gxhc520.cn)
# @Link    : https://admin.gxhc520.cn
# @Version : $Id$

import os
import optparse
import json
import PIL.Image
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()

    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon


def getForExif(src):
	'''
	walk the src 
	'''
	for rootdir,dirnames,filenames in os.walk(src):
		for filename in filenames:
			srcfilename = os.path.join(rootdir,filename)
			savesrcfilename = os.path.join(os.path.dirname(srcfilename),filename+".txt")
			try:
				image = Image.open(srcfilename)
				exif_data = get_exif_data(image)
				lat_lon_str = str(get_lat_lon(exif_data))
				# print str(get_lat_lon(exif_data))
				with open(savesrcfilename,"w") as wfp:
					wfp.writelines( lat_lon_str + "\n")
					pass
			except Exception as e:
				'''Pass'''
				pass
			
def main():
	parser=optparse.OptionParser("usage:%prog -s <src filename dir>")
	parser.add_option("-s",dest="Src",type="string",help="specify a src filename dirname")

	(options,args)=parser.parse_args()

	src=options.Src

	if src==None:
		print "[-] "+parser.usage
		exit(0)

	print "[-] "+"Reading start..."
	#execute the function
	getForExif(src)
	print "[+] "+"Handling end..."

if __name__ == '__main__':
	main()
