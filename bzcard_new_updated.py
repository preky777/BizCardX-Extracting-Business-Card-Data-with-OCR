import streamlit as st
import io
import os
import streamlit as st
from streamlit_ace import st_ace
import numpy as np
import pandas as pd
import easyocr
import mysql.connector
import re
import cv2
import base64
import PIL.Image
from PIL import Image
import matplotlib.pyplot as plt

# Create a connection to the MySql database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='rp#$9882',
    database='bscards3'
)
cursor = conn.cursor()

# Create a table to store the business card data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS business_cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255),
        card_holder_name VARCHAR(255),
        designation VARCHAR(255),
        mobile_number VARCHAR(50),
        email_address VARCHAR(255),
        website VARCHAR(255),
        area VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        pincode VARCHAR(10),
        image_data LONGBLOB
    )
''')
# Commit the changes and close the connection
conn.commit()
conn.close()


conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='rp#$9882',
        database='bscards3'
    )
cursor = conn.cursor()

reader = easyocr.Reader(['en'])

def fetch_card_data(card_id):
    # Function to fetch data for a specific business card based on the card ID from the database
    cursor.execute("SELECT * FROM business_cards WHERE id=%s", (card_id,))
    result = cursor.fetchone()
    if result:
        card_data = {
            "id": result[0],
            "company_name": result[1],
            "card_holder_name": result[2],
            "designation": result[3],
            "mobile_number": result[4],
            "email_address": result[5],
            "website": result[6],
            "area": result[7],
            "city": result[8],
            "state": result[9],
            "pincode": result[10]
        }
        return card_data
    else:
        return None


# Function to extract data from the image using easyOCR
def extract_data_from_image(uploaded_file):
    # Convert the BytesIO object to an image array using OpenCV
    img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
    reader = easyocr.Reader(['en'])
    l = reader.readtext(img, detail=0, paragraph=True)
    s = ' '.join(l)
    url_s = re.findall(r"[www|WWW|wwW]+[\.|\s]+[a-zA-Z0-9]+[\.|\][a-zA-Z]+", s)
    url = re.sub('[WWW|www|wwW]+ ', 'www.', url_s[0]) if url_s else ""

    email_s = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+", s)
    email = email_s[0] if email_s else ""
    mob_s = re.findall(r"[6-9]\d{9}|[\+9]\d{12}|[\+91]+\-\d{3}\-\d{4}|[\+1-2]\d{3}\-\d{3}\-\d{4}|[1-2]\d{2}\-\d{3}\-\d{4}|[0-9]{10}", s)
    mob = ', '.join(mob_s) if mob_s else ""
    ad_s = re.findall(r"[0-9]{1,4}\s[A-Za-z]+\s[A-Za-z]+[\s|\.|\,]\,\s[A-Za-z]+[\|\,|\;]\s[A-Za-z]+[\,\s|\,\s|\;\s|\s]+[0-6]{5,7}", s)
    ad = re.findall(r"([0-9]{1,4}\s[A-Za-z]+\s[A-Za-z]+)[\s|\.|\,]\,\s([A-Za-z]+)[\|\,|\;]\s([A-Za-z]+)[\,\s|\,\s|\;\s|\s]+([0-6]{5,7})", s)
    area_v = ad[0][0] if ad else ""
    city_v = ad[0][1] if ad else ""
    state_v = ad[0][2] if ad else ""
    pin = ad[0][3] if ad else ""
    l_s = l.copy()
    for i in l_s:
        if ad_s and ad_s[0] in i:
            j = l_s.index(i)
            del l_s[j]
        elif url_s and url_s[0] in i:
            j = l_s.index(i)
            del l_s[j]
        elif email in i:
            j = l_s.index(i)
            del l_s[j]
        elif mob in i:
            j = l_s.index(i)
            del l_s[j]
    x = l_s[0] if l_s else ""
    des_s = re.findall(r"[A-Za-z]+[\s|\s\&\s]+[A-Za-z]+$", x)
    des = des_s[0] if des_s else ""
    nam_s = x.replace(des, '')
    nam_l = re.findall(r"[A-Za-z]+\s[A-Za-z]+|[A-Za-z]+", nam_s)
    nam = nam_l[0] if nam_l else ""
    cmp = l_s[-1] if l_s else ""
    
    return {
        "company_name": cmp,
        "card_holder_name": nam,
        "designation": des,
        "mobile_number": mob,
        "email_address": email,
        "website": url,
        "area": area_v,
        "city": city_v,
        "state": state_v,
        "pincode": pin
    }

# CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
def img_to_binary(file):
        # Convert image data to binary format
        with open(file, 'rb') as file:
            binaryData = file.read()
        return binaryData

# Function to save data to MySQL with the business card image
def save_to_mysql(data, uploaded_file):

    saved_img = os.getcwd()+ "\\" + "bs_card_images"+ "\\"+ uploaded_file.name

    # Truncate the mobile number to a maximum of 30 characters
    truncated_mobile_number = data["mobile_number"][:30]

    query = "INSERT INTO business_cards (company_name, card_holder_name, designation, mobile_number, email_address, website, area, city, state, pincode, image_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        data["company_name"],
        data["card_holder_name"],
        data["designation"],
        truncated_mobile_number,
        data["email_address"],
        data["website"],
        data["area"],
        data["city"],
        data["state"],
        data["pincode"],
        img_to_binary(saved_img)
    )
    cursor.execute(query, values)
    conn.commit()


# Function to update data in MySQL
def update_in_mysql(data, card_id):
    query = "UPDATE business_cards SET company_name=%s, card_holder_name=%s, designation=%s, mobile_number=%s, email_address=%s, website=%s, area=%s, city=%s, state=%s, pincode=%s WHERE id=%s"
    values = (
        data["company_name"],
        data["card_holder_name"],
        data["designation"],
        data["mobile_number"],
        data["email_address"],
        data["website"],
        data["area"],
        data["city"],
        data["state"],
        data["pincode"],
        card_id
    )
    cursor.execute(query, values)
    conn.commit()

# Function to delete data from MySQL
def delete_from_mysql(card_id):
    query = "DELETE FROM business_cards WHERE id=%s"
    values = (card_id,)
    cursor.execute(query, values)
    conn.commit()



def home_page():
    st.title("Bizcard App")
    st.write("""
        <div class="home-text">
            <h1 style='font-size: 48px; font-weight: bold;'>Welcome to BizCardX</h1>
            <p style='font-size: 28px;'>Extracting Business Card Data with OCR</p>
            <br>
            <p style='font-size: 18px;'>Use BizCardX to effortlessly extract contact information</p>
            <p style='font-size: 18px;'>from business cards and save it to your database.</p>
            <br>
            <p style='font-size: 18px;'>Upload an image of a business card and let BizCardX work its magic!</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Get Started"):
        st.session_state['page'] = 'ext_mod'

def image_preview(image, res): 
    # Create a copy of the image to draw the rectangles on
    image_with_boxes = image.copy()
    
    for (bbox, _, _) in res: 
        # Unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))
        
        # Draw the rectangle
        cv2.rectangle(image_with_boxes, tl, br, (0, 255, 0), 2)

    # Display the image with bounding boxes
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.axis('off')
    plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
    plt.show()

def pil_to_base64(image):
    # Convert PIL image to base64 string
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def show_business_cards():
    # Function to display the business card data along with the corresponding image
    cursor.execute("SELECT * FROM business_cards")
    data_rows = cursor.fetchall()

    # Create a list to store the data and images
    data_list = []

    for row in data_rows:
        card_id, company_name, card_holder_name, designation, mobile_number, email_address, website, area, city, state, pincode, image_data = row

        # Append each row data and image to the main data_list
        data_list.append([
            card_id, company_name, card_holder_name, designation, mobile_number,
            email_address, website, area, city, state, pincode, image_data
        ])

    # Create a Pandas DataFrame from the collected data
    data_df = pd.DataFrame(data_list, columns=[
        "Card ID", "Company Name", "Card Holder Name", "Designation", "Mobile Number",
        "Email Address", "Website", "Area", "City", "State", "Pincode", "Image"
    ])

    st.dataframe(data_df)



def delete_business_card():
    cursor.execute("SELECT card_holder_name FROM business_cards")
    result = cursor.fetchall()
    business_cards = {row[0]: row[0] for row in result}
    selected_card = st.selectbox("Select a card holder name to delete", list(business_cards.keys()))
    st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
    st.write("#### Proceed to delete this card?")
    if st.button("Yes Delete Business Card"):
        # Delete the business card information from the database
        delete_from_mysql(selected_card)
        st.success("Business card information deleted from the database.")


def ext_mod_page():
    st.markdown("<h1 style='text-align: center; color: white;'>Extraction And Modification Process</h1>", unsafe_allow_html=True)
    # CREATING OPTION MENU
    selected_option = st.radio(
        "Select an Option:",
        ["Upload,Extract And Save To Database", "Update And Save To Database","Delete From The Database"],
        index=0,
        key="option_menu"
    )

    # Add some space between the option menu and other elements
    st.write("<br><br>", unsafe_allow_html=True)


    # Section 1: Upload & Extract
    if selected_option == "Upload,Extract And Save To Database":
        st.subheader("Upload and Extract Business Card Data")
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = None

        if "extracted_data" not in st.session_state:
            st.session_state.extracted_data = None

        if "selected_card_id" not in st.session_state:
            st.session_state.selected_card_id = None

        # ... (rest of your existing code)

        uploaded_file = st.file_uploader("Upload a Business Card Image", type=["jpg", "png"])
        st.session_state.uploaded_file = uploaded_file

        if st.session_state.uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Business Card", use_column_width=True)
            extracted_data = extract_data_from_image(uploaded_file)
            if st.button("Extract Information"):
                st.markdown("#     ")
                st.markdown("#     ")
                with st.spinner("Please wait processing image..."):
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    saved_img = os.getcwd()+ "\\" + "bs_card_images"+ "\\"+ uploaded_file.name
                    image = cv2.imread(saved_img)
                    res = reader.readtext(saved_img)
                    st.markdown("### Image Processing")
                    st.pyplot(image_preview(image,res))
                st.subheader("Extracted Information:")
                data_dict = {
                    "Field": ["Company Name", "Card Holder Name", "Designation", "Mobile Number", "Email Address", "Website", "Area", "City", "State", "Pincode"],
                    "Value": [extracted_data["company_name"], extracted_data["card_holder_name"], extracted_data["designation"], extracted_data["mobile_number"], extracted_data["email_address"], extracted_data["website"], extracted_data["area"], extracted_data["city"], extracted_data["state"], extracted_data["pincode"]]
                }
                st.table(data_dict)

            if st.button("Save to Database"):
                save_to_mysql(extracted_data, uploaded_file)
                st.success("Data saved to the database.")

    # Section 2: Modify
    elif selected_option == "Update And Save To Database":

        st.subheader("Manage Business Card Data")
        show_business_cards()
        st.markdown("## Updating done here")

        try:
            cursor.execute("SELECT id FROM business_cards")
            result = cursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card ID to Update", list(business_cards.keys()))

            selected_card_data = fetch_card_data(selected_card)

            # Use emojis and custom CSS styling with markdown
            st.markdown(f"### :pencil2: You have selected **{selected_card_data['card_holder_name']}'s** card to update")

           

            # Use st.form context manager to create a form
            st.markdown("### Business Card ID")
            st.text_input("Card ID", value=selected_card_data["id"], key="card_id", disabled=True)
            st.markdown("### Update Card Information:")

            form1=st.form(key='form1')
            company_name = form1.text_input("Company Name", value=selected_card_data["company_name"], key="company_name",help="click below button to Save changes to database")
            card_holder = form1.text_input("Card Holder Name", value=selected_card_data["card_holder_name"], key="card_holder_name",help="click below button to Save changes to database")
            designation = form1.text_input("Designation", value=selected_card_data["designation"], key="designation",help="click below button to Save changes to database")
            mobile_number = form1.text_input("Mobile Number", value=selected_card_data["mobile_number"], key="mobile_number",help="click below button to Save changes to database")
            email = form1.text_input("Email Address", value=selected_card_data["email_address"], key="email_address",help="click below button to Save changes to database")
            website = form1.text_input("Website", value=selected_card_data["website"], key="website",help="click below button to Save changes to database")
            area = form1.text_input("Area", value=selected_card_data["area"], key="area",help="click below button to Save changes to database")
            city = form1.text_input("City", value=selected_card_data["city"], key="city",help="click below button to Save changes to database")
            state = form1.text_input("State", value=selected_card_data["state"], key="state",help="click below button to Save changes to database")
            pincode = form1.text_input("PinCode", value=selected_card_data["pincode"], key="pincode",help="click below button to Save changes to database")
            sb1=form1.form_submit_button('Save changes to DB')

            if sb1:
                data = {"id": selected_card_data["id"],"company_name": company_name,"card_holder_name": card_holder,"designation": designation,"mobile_number": mobile_number,"email_address": email,"website": website,"area": area,"city": city,"state": state,"pincode": pincode}
                update_in_mysql(data, selected_card_data["id"])
                st.success("Updated successfully to the database.")




        except:
            st.warning("There is no data available in the database")

        if st.button("View updated data"):
            cursor.execute("SELECT id, company_name, card_holder_name, designation, mobile_number, email_address, website, area, city, state, pincode FROM business_cards")
            updated_data = cursor.fetchall()
            if updated_data:
                updated_df = pd.DataFrame(updated_data, columns=["Card ID", "Company Name", "Card Holder Name", "Designation", "Mobile Number", "Email Address", "Website", "Area", "City", "State", "PinCode"])
                st.write(updated_df)
            else:
                st.warning("No data available in the database.")



    elif selected_option == "Delete From The Database":
        st.subheader("Manage Business Card Data")
        show_business_cards()
        cursor.execute("SELECT id, card_holder_name FROM business_cards")
        result = cursor.fetchall()
        business_cards = {}
        for row in result:
            card_id, card_holder_name = row
            business_cards[card_id] = card_holder_name
        
        selected_card_id = st.selectbox("Select a card ID to Delete", list(business_cards.keys()))

        selected_card = business_cards[selected_card_id]

        # Use emojis and custom CSS styling with markdown
        st.markdown(f"### :wastebasket: You have selected **{selected_card}'s** card to delete")
        st.markdown("#### :warning: Proceed to delete this card?")

        if st.button("Yes, Delete Business Card"):
            cursor.execute(f"DELETE FROM business_cards WHERE id={selected_card_id}")
            conn.commit()
            st.success("Business card information deleted from the database.")


        


def main():
    st.session_state.setdefault('page', 'home')

    if st.session_state['page'] == 'home':
        home_page()
    elif st.session_state['page'] == 'ext_mod':
        ext_mod_page()

    # Check if the Rerun button is pressed
    if st.button("Rerun"):
        # Reset the page to 'home' to show the home page again
        st.session_state['page'] = 'home'
        # Trigger a rerun of the app
        st.experimental_rerun()

if __name__ == "__main__":
    main()