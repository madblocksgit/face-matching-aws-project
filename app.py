import streamlit as st
from PIL import Image
import os
import boto3

col1, col2 = st.columns(2)

col1.subheader("Enter Image Source")
src_image_file = col1.file_uploader("Upload Images",type=["png","jpg","jpeg"],key=1)

col2.subheader("Enter Image Target")
src_image_file2 = col2.file_uploader("Upload Images",type=["png","jpg","jpeg"],key=2)

a=0
b=0

def load_image(image_file):
	img = Image.open(image_file)
	return img

if src_image_file is not None:
    b=1
	# TO See details
    file_details = {"filename":src_image_file.name, "filetype":src_image_file.type,"filesize":src_image_file.size}
    col1.write(file_details)
    col1.image(load_image(src_image_file), width=250)
 
			  
	#Saving upload
    with open(os.path.join("uploads","person1.jpg"),"wb") as f:
        f.write((src_image_file).getbuffer())
        col1.success("File Saved")

if src_image_file2 is not None:
    a=1
	# TO See details
    file_details = {"filename":src_image_file2.name, "filetype":src_image_file2.type,"filesize":src_image_file2.size}
    col2.write(file_details)
    col2.image(load_image(src_image_file2), width=250)
			  
	#Saving upload
    with open(os.path.join("uploads",'person2.jpg'),"wb") as f:
        f.write((src_image_file2).getbuffer())
        col2.success("File Saved")

if st.button("Compare Faces"):
    try:
        if(a==0 or b==0):
            raise FileNotFoundError
    except FileNotFoundError:
        st.error('Upload images first')
    
    if(a==1 and b==1):
        imageSource=open('uploads/person1.jpg','rb')
        imageTarget=open('uploads/person2.jpg','rb')

        client=boto3.client('rekognition')
        response=client.compare_faces(SimilarityThreshold=70,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
        print(response['FaceMatches'])
        a=0
        b=0
        try:
            print(response['FaceMatches'][0])
            st.success("Faces Matched")
        except:
            st.success("Faces Not Matched")