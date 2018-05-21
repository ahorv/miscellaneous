import os
import numpy as np
import sqlite3
import cv2
from glob import glob
from os.path import isfile, join

######################################################################
## Hoa: 21.05.2018 Version 2 : images2DB.py
######################################################################
# Quelle:  https://miguelaragon.wordpress.com/2017/12/03/storing-compressed-images-in-sqlite-with-python/
# Takes all the jpg files in a folder and stores them in a SQLite database
# as encoded (raw) images (binary blobs).
#
# New /Changes:
# ----------------------------------------------------------------------
# - 18.05.2018 first implemented
#
######################################################################

global PATH_IMAGES
PATH_IMAGES = r'E:\SkyCam\camera_1\20180429_raw_cam1\imgs5'

# Check weather path exists
if not os.path.exists(PATH_IMAGES):
    print('Path to images does not exist!')




def getDirectories(pathToImgs5):
    try:
        global PATH_IMAGES
        allDirs = []
        allDirs = sorted(glob(join(pathToImgs5, "*.jpg")))

        print('Fetched {} images from {} '.format(len(allDirs),PATH_IMAGES))

        return allDirs

    except Exception as e:
        print('getDirectories: Error: ' + str(e))


# --- Simple database creator
def create_db(filename):
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Images")
    cursor.execute("CREATE TABLE Images(ObjId INT, img BLOB, size INT)")
    db.commit()
    db.close()



# --- Open database and loop over files to insert in database
def insertToDB(db_name,files):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    for i, file_i in enumerate(files):

        # --- Read image as a binary blob
        with open(file_i, 'rb') as f:
            image_bytes = f.read()
        f.close()

        # --- Decode raw bytes to get image size
        nparr = np.fromstring(image_bytes, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_size = img_np.shape[1]

        # --- Extract file name without extension
        filename = os.path.relpath(file_i, PATH_IMAGES)
        objid = int(os.path.splitext(filename)[0])

          # --- Insert image and data into table
        cur.execute("insert into Images VALUES(?,?,?)", (objid, sqlite3.Binary(image_bytes), image_size))
        con.commit()

    print('Loaded {} images to DB'.format(i))
    cur.close()
    con.close()

def fetchOneImgFromDB(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    row = cur.execute("SELECT ObjId, img from Images")
    for ObjId, item in row:

        # --- Decode blob
        nparr = np.fromstring(item, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # --- Display image
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', img_np)
        cv2.resizeWindow('image', 300, 300)
        k = cv2.waitKey(0)
        if k == 27:  # wait for ESC key to exit
            cv2.destroyAllWindows()
            break

    cur.close()
    con.close()

def main():
    try:
        global PATH_IMAGES

        # --- Extract files from folder following pattern
        print("Path to directory: {}".format(PATH_IMAGES))
        files = getDirectories(PATH_IMAGES)

        # --- Create test DB
        filename_db = 'testdb_0.db'
        create_db(filename_db)

        # --- insert img's to DB
        insertToDB(filename_db,files)

        # --- test DB
        fetchOneImgFromDB(filename_db)

        print('imagees2DB.py done')

    except Exception as e:
        print('MAIN: Error in main: ' + str(e))


if __name__ == '__main__':
    main()