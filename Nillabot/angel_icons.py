from PIL import Image
import os
import sqlite3

face_dir = r"E:\GitHub\IA\ia_dump\EN\ASSETS\icon\face"
frame_dir = r"E:\GitHub\IA\ia_dump\EN\ASSETS\heroqualitylevel"
destination = r'E:\GitHub\IA\ia_dump\bot_assets'

connection = sqlite3.connect('ia.db')
cursor = connection.cursor()

base_face_query = cursor.execute("SELECT quality_level, avatar_path \
                            FROM angel WHERE NOT name = 'Player'").fetchall()
ur_face_query = cursor.execute("SELECT icon FROM ur_shards INNER JOIN ur_angel ON ur_angel.cid = ur_shards.cfg_id").fetchall()
urp_face_query = cursor.execute("SELECT icon FROM urp_shards").fetchall()
mr_face_query = cursor.execute("SELECT icon FROM mr_shards").fetchall()
                               
cursor.close()
connection.close()  

for item in base_face_query:
    qual = item[0]
    icon_name = item[1]
    face = face_dir + "\\" +icon_name
    frame = f"{frame_dir}\\icon_quality_level_{qual}.png"
    try:
        im1 = Image.open(face)
        im2_size = Image.open(frame).size
        box1 = 0
        box2 = round(im2_size[0] / im2_size[1] * 256 - 256)
        box3 = 256
        box4 = 256 + box2
        crop_by = round((im2_size[0] / im2_size[1]) * 256)
        box = (box1, box2, box3, box4)
        
        im2 = Image.open(frame).resize((256,256))
        im1.paste(im2, box, mask=im2)
        im1.save(r'temp\framed_face.png')

        merged = Image.open(r'temp\framed_face.png')
        merged.crop((0,0,256,crop_by)).save(f"E:\\GitHub\\IA\\ia_dump\\bot_assets\\{icon_name}")
    except:
        print(f"{icon_name} for quality {qual} failed.")

for item in ur_face_query:
    qual = 8
    icon_name = item[0]
    face = face_dir + "\\" +icon_name
    frame = f"{frame_dir}\\icon_quality_level_{qual}.png"
    try:
        im1 = Image.open(face)
        im2_size = Image.open(frame).size
        box1 = 0
        box2 = round(im2_size[0] / im2_size[1] * 256 - 256)
        box3 = 256
        box4 = 256 + box2
        crop_by = round((im2_size[0] / im2_size[1]) * 256)
        box = (box1, box2, box3, box4)
        
        im2 = Image.open(frame).resize((256,256))
        im1.paste(im2, box, mask=im2)
        im1.save(r'temp\framed_face.png')

        merged = Image.open(r'temp\framed_face.png')
        merged.crop((0,0,256,crop_by)).save(f"E:\\GitHub\\IA\\ia_dump\\bot_assets\\{icon_name}")
    except:
        print(f"{icon_name} for quality {qual} failed.")

for item in urp_face_query:
    qual = 9
    icon_name = item[0]
    face = face_dir + "\\" +icon_name
    frame = f"{frame_dir}\\icon_quality_level_{qual}.png"
    try:
        im1 = Image.open(face)
        im2_size = Image.open(frame).size
        box1 = 0
        box2 = round(im2_size[0] / im2_size[1] * 256 - 256)
        box3 = 256
        box4 = 256 + box2
        crop_by = round((im2_size[0] / im2_size[1]) * 256)
        box = (box1, box2, box3, box4)
        
        im2 = Image.open(frame).resize((256,256))
        im1.paste(im2, box, mask=im2)
        im1.save(r'temp\framed_face.png')

        merged = Image.open(r'temp\framed_face.png')
        merged.crop((0,0,256,crop_by)).save(f"E:\\GitHub\\IA\\ia_dump\\bot_assets\\{icon_name}")
    except:
        print(f"{icon_name} for quality {qual} failed.")

for item in mr_face_query:
    qual = 15
    icon_name = item[0]
    face = face_dir + "\\" +icon_name
    frame = f"{frame_dir}\\icon_quality_level_{qual}.png"
    try:
        im1 = Image.open(face)
        im2_size = Image.open(frame).size
        box1 = 0
        box2 = round(im2_size[0] / im2_size[1] * 256 - 256)
        box3 = 256
        box4 = 256 + box2
        crop_by = round((im2_size[0] / im2_size[1]) * 256)
        box = (box1, box2, box3, box4)
        
        im2 = Image.open(frame).resize((256,256))
        im1.paste(im2, box, mask=im2)
        im1.save(r'temp\framed_face.png')

        merged = Image.open(r'temp\framed_face.png')
        merged.crop((0,0,256,crop_by)).save(f"E:\\GitHub\\IA\\ia_dump\\bot_assets\\{icon_name}")
    except:
        print(f"{icon_name} for quality {qual} failed.")

print('Angel icons created! Ready to push to github.')

