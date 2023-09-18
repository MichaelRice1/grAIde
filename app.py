import streamlit as st
from PIL import Image
import sqlite3
from io import BytesIO
import base64


st.set_page_config(page_title="grAIde", page_icon=":camera:", layout = "wide")

before1 = Image.open("images/before1.png")
target1 = Image.open("images/target1.png")
after1 = Image.open("images/after1.png")

before2 = Image.open("images/before1.gif")
target2 = Image.open("images/target2.png")
after2 = Image.open("images/after2.gif")


img_cam = Image.open("images/camera.png")  

conn = sqlite3.connect('images_db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        image_data BLOB
    )
''')
conn.commit()

def clear_database():
    cursor.execute("DELETE FROM images")
    conn.commit()
    # Close the database connection
    

       
       


with st.container():
        st.header("grAIde")
        st.subheader("Hello, this is a colour grading engine that uses AI to match the colour grade of any picture or video :) :camera:")
        st.write("[Learn More > ] (https://github.com/MichaelRice1)")

with st.container():
        st.write("-----")
        files_column, imgs_column, button_column = st.columns(3)
        with files_column:
            st.header("Upload files for Colour Grading Here")
            uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg","mp4"])
        with button_column:
            imgs_button = st.button("Press to display images from database")
            clear_button = st.button("Press to clear all images from database ")
            if clear_button:
                  clear_database 
        with imgs_column:
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption='Uploaded Image', use_column_width=True)
                img_bytes = BytesIO()
                image.save(img_bytes, format="PNG")
                img_data = img_bytes.getvalue()
                cursor.execute("INSERT INTO images (image_data) VALUES (?)", (img_data,))
                conn.commit()
                st.success('Image uploaded and stored in the database!')
            if imgs_button:     
                st.header('Images Stored in the Database')
                cursor.execute("SELECT id, image_data FROM images")
                images = cursor.fetchall()
                for image_id, img_data in images:
    # Display images by converting bytes data back to image
                    img = Image.open(BytesIO(img_data))
                    st.image(img, caption=f"Image ID: {image_id}", use_column_width=True)
                
                
            


with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("What The Engine Can Do ")
            st.write("##")
            st.write(
                """
                - Match the colour grade of any video or image and apply it to any provided image.
                - Take text input and apply the instructions to the provided image.
                - Give you the altered image back.

                """
            )
with right_column:
            st.image(img_cam)

with st.container():
            st.write("---")
            st.header("Examples")
            st.write("##")
            before_column, target_column, after_column = st.columns(3)
            with before_column:
                   st.markdown("<h1 style='text-align: center;'>Before</h1>", unsafe_allow_html=True)
                   st.image(before1)
                   resized_image1 = before2.resize(before1.size)
                   st.image(resized_image1)
            with target_column:
                   st.markdown("<h1 style='text-align: center;'>Target</h1>", unsafe_allow_html=True)
                   st.image(target1)
                   resized_image2 = target2.resize(before1.size)
                   st.image(resized_image2)
            with after_column:
                   st.markdown("<h1 style='text-align: center;'>After</h1>", unsafe_allow_html=True)
                   st.image(after1)
                   resized_image3 = after2.resize(after1.size)
                   st.image(resized_image3)
                   


