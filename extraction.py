from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import csv
import os

def get_exif_data(image):
    
    """
    Input: path to image
    
    Returns a list for each image with the image metadata/exif data. 
        List structure is [pictureID, Latitude, Longitude, DateTime]
        Latitude and Longitude format = (degrees, minutes, seconds)
        DateTime format = 'year:month:day hour:minute:second'
    """

    # list = [pictureID, Latitude, Longitude, DateTime]
    exif_data_list = []
    
    # extract image name from path & add to list
    image_name = os.path.basename(image)
    exif_data_list.append(str(image_name))
   
    # open the image (getexif can open both .HEIC and .jpeg pictures that have embedded metadata
    pic = Image.open(image)
    exifdata = pic._getexif()
       
    #exifdata is a dictionary, looping throught the pairs of the dictionary using dict.items() and get the exifdata
    for exif_tag, exif_value in exifdata.items():

        # getting the tag name instead of tag id
        tagname = TAGS.get(exif_tag, exif_tag)
        print(f"Decoded {tagname}, tag {exif_tag} and {exif_value}")
        
        if tagname == "DateTime":
            print (f"{tagname} = {exif_value}")
            exif_data_list.append(exif_value)
        
        if tagname == "GPSInfo":
            print (f"This is the {exif_value}")
            
            # value under GPS info is a dictionary, looping throught the pairs of the gps dictionary using dict.items()
            for gps_tag, gps_value in exif_value.items():
                
                print (f"This is the {gps_tag} and its {gps_value}")

                # getting the gps tag name instead of tag id
                gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                print(f"GPS Tagname: {gps_tag_name}, GPS Tag ID: {gps_tag} and GPS Tag Value: {gps_value}")

                if gps_tag_name == "GPSLatitude":
                    exif_data_list.append(gps_value)
                if gps_tag_name == "GPSLongitude":
                    exif_data_list.append(gps_value)          
                          
    return exif_data_list

def convert_dms_to_dd (pic_data):
    """
    input list structure = List structure is [pictureID, Latitude, Longitude, DateTime]
    Latitude and longitude format in this input list is (degrees, minutes,seconds)

    Returns list where latitude and longitude is converted to decimal degrees
        """
    for index in [1,2]:

        #access coordinate tuple (d,m,s)
        element = pic_data[index]
    
        #converstion formula for dms to dd: d + (m / 60.0) + (s / 3600.0)
        dd = element[0] + (element[1] / 60.0) + (element[2] / 3600.0)
        print (dd)

        # put converted value back in list
        pic_data[index] = dd
        
    return pic_data

def add_csv (dd_list):

    csv_name = 'writing.csv'

    header = ["image_name", "latittude_dd", "longitude_dd", "datetime"]

    # Check if the file exists
    file_exists = os.path.isfile(csv_name)
    
    # Open the CSV file in append mode
    with open(csv_name, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file does not exist
        if not file_exists:
            writer.writerow(header)
        
        # Write the new line to the CSV file
        writer.writerow(dd_list)


#######################################################################################################################
working_directory = os.getcwd()
folder_name = 'pics'
relative_pathname = os.path.join(working_directory,folder_name)

for root, dirs, files in os.walk(relative_pathname):
    for file in files:
        exif_data = get_exif_data(os.path.join(relative_pathname,file))
        conversion = convert_dms_to_dd(exif_data)
        add_csv(conversion)

      
      #TEST VARIABLES FOR EACH FUNCTION
#get_exif_data("IMG_0227.HEIC")
#convert_dms_to_dd (['IMG_0227.HEIC', (29.0, 59.0, 40.23), (31.0, 7.0, 12.66), '2024:11:19 14:07:54'])
#add_csv (['IMG_0227.HEIC', 29.994508333333336, 31.120183333333333, '2024:11:19 14:07:54'])
