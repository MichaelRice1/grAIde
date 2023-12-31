import streamlit as st
from PIL import Image
import sqlite3
from io import BytesIO
import color_matcher as cm
import tensorflow as tf
import os



os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'


st.set_page_config(page_title="grAIde", page_icon=":camera:", layout = "wide")
vgg19 = tf.keras.applications.VGG19(include_top=False, weights='imagenet')



before1 = Image.open("images/before1.png")
target1 = Image.open("images/target1.png")
after1 = Image.open("images/after1.png")

before2 = Image.open("images/before1.gif")
target2 = Image.open("images/target2.png")
after2 = Image.open("images/after2.gif")


img_cam = Image.open("images/camera.png") 
logo = Image.open("images/logo.png") 

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
    conn.close()
    # Close the database connection
    
#always appearing things
with st.container():
    #two columns, one for the main logo, one for the navmenu
    logo_column, navmenu_column = st.columns(2)
    #the column for the logo
    with logo_column:
        resize_logo = logo.resize([350,150])
        st.image(resize_logo)
    #the column for the for the selection box
    with navmenu_column:
        page = st.selectbox("", ("Home", "About","Samples", "Photo Colour Matching","Video Colour Matching","Text to Grade"))

#home page   
if page == "Home":
    #defining the reasons for completing the project
    st.write("a side project by a 4th Year Computer Engineering Student.")
    st.write("    - I decided to attempt this project due to a multitude of reasons. ")
    st.write("    - Firstly, my inability to learn how to properly colour grade.")
    st.write("    - Secondly, my passion for innovative projects.")
    st.write("    - Thirdly, my enthusiasm for all things photography and cinematography.")
    st.write("    - Lastly, I also do not want to pay for other commercial AI engines.")

#about page
if page == "About":
    with st.container():
            st.subheader("A colour grading engine using AI to match the colour grade of any picture or video.")
            st.write("[Learn More > ] (https://github.com/MichaelRice1)")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("What The Engine Can Do ")
            st.write("##")
            st.write(
                """
                - Match the colour grade of any video or image and apply it to any provided input file.
                - Take text input and apply the instructions to any provided input file.

                """
            )
            st.subheader("The Technology Used to Complete the Project")
            st.write(
                """
                - Python Streamlit Library used to create the frontend. 
                - Python ML Algorithm used in the backend.

                """
            )
        with right_column:
            resize_cam = img_cam.resize([550,550])
            st.image(resize_cam)

#sample pictures page
if page == "Samples":

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

#photo editing page
if page == "Photo Colour Matching":
    with st.container():
            st.write("-----")
            files_column, imgs_column, button_column = st.columns(3)
            with files_column:
                st.header("Upload images for Colour Grading Here")
                uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
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
                
#video editing page                
if page == "Video Colour Matching":
     with st.container():
            st.write("-----")
            files_column, vids_column, button_column = st.columns(3)
            with files_column:
                st.header("Upload videos for Colour Grading Here")
                uploaded_video = st.file_uploader("Upload a video", type=["mp4"])
            with vids_column:
                if uploaded_video is not None:
                    st.video(uploaded_video, format="video/mp4")
                else:
                    st.warning("Please upload a video")
            with button_column:
                grAIde_vids_button = st.button("Press to grAIde.")

#text to grade page
if page == "Text to Grade":
    with st.container():
            text_column, files_column2 = st.columns(2)
            with text_column:
                st.header("Input Text Here to Apply to Photo or Video")
                user_input = st.text_input("Enter your text here:", "")
            with files_column2:
                st.header("Upload images for Colour Grading Here")
                uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg","mp4","mov"])
    
    with st.container():
        if uploaded_file:
            st.image(uploaded_file)
            #add functionality for videos here    

