# BizCardX-Extracting-Business-Card-Data-with-OCR
## Introduction
BizCardX is a revolutionary project that harnesses the power of Optical Character Recognition (OCR) to effortlessly extract valuable data from business cards. With just a simple image upload, this application utilizes the easyOCR library to extract relevant information like names, job titles, phone numbers, and email addresses. The extracted data is then presented in a user-friendly format, ready to be stored in a MySQL database for future reference. With its seamless integration, users can easily view, modify, or delete the extracted data, ensuring a streamlined experience. Unlock the potential of BizCardX and say goodbye to manual data entry woes!

## Requirements for the project

    Python: Make sure you have Python installed on your system. The project is built using Python, and having Python installed is essential to run the code.
    
    GitHub: Ensure you have a GitHub account and know the basics of using Git version control. The project uses GitHub for versioning, collaboration, and sharing code.
    
    MySQL: Install MySQL or have access to a MySQL database. The project involves data extraction, transformation, and storage using MySQL, so having a MySQL server is necessary.
    
    Required Libraries: Install the necessary Python libraries using pip install or any package manager. The essential libraries include:
    
      * pandas as pd
      * streamlit as st
      * easyocr
      * PIL (Python Imaging Library)
      * mysql.connector
      * numpy as np
      * requests
      * matplotlib.pyplot as plt
      * os
      * import re
      * import cv2
      * import base64

Ensure all these libraries are installed before running the project code.

With these prerequisites in place, you'll be ready to explore and run the Bizcard project using Python, GitHub, and MySQL. Happy coding!

   
## Installation & Usage

To access the web app, simply open the provided URL in your web browser. Once there, you can start exploring the various features available on the app. The user-friendly interface allows you to interact with the app seamlessly. Provide the necessary inputs based on your specific needs, and in return, you'll receive insightful and interactive results. Enjoy the experience and gain valuable insights from the Bizcard extraction and modification.

    1. Clone the repository to your local machine using the following command: git clone https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR.git.
    2. Install the required libraries.
    3. Run the .py file.
    4. Create a MySQL database and tables, define constraints, and push data into MySQL using user-defined functions.
    5. Open a terminal window and navigate to the directory where the app is located using the following command: cd C:\Users\Phoenix\Desktop\bs_cards.
    6. Run the Streamlit app using the command [streamlit run bzcard.py] and access the app through the local URL provided.
    7. The app should now be running on a local server. If it doesn't start automatically, you can access it by going to either the given Local URL or Network URL.
    8. Experience the power of BizCardX, where you can effortlessly navigate through the app, effortlessly upload business cards, effortlessly extract valuable data, effortlessly save and effortlessly modify information. And if the need arises, effortlessly delete as well. 
    
BizCardX revolutionizes the way you handle business cards, eliminating manual data entry and streamlining your workflow to perfection.



## Components of the Dashboard

    1.Home page
    
    2.Extraction and Modification process page
    

1. Home page:
   This code defines the layout and content of the home page for the "Bizcard App." It provides a brief introduction to the app's functionality and prompts the user to click the "Get Started" button to proceed to the next page, which appears to be for extracting and modifying business card data using OCR.


         * st.title("Bizcard App"): Sets the title of the web application to "Bizcard App".

         * st.write(""" ... """, unsafe_allow_html=True): Writes the HTML content provided within triple quotes to the web application. This HTML content seems to define the layout and text displayed on the home page. The HTML content contains a heading, a couple of paragraphs, and a button.

         * The HTML content defines a <div> with a class of "home-text" to group the text elements together. It contains the following components:

               A large heading <h1> with the text "Welcome to BizCardX".
               A subheading <p> with the text "Extracting Business Card Data with OCR".
               A couple of paragraphs that provide introductory information about the app and its purpose.
               unsafe_allow_html=True: This parameter of the st.write() function tells Streamlit to allow rendering the provided HTML content. Without this parameter set to True, Streamlit would escape any HTML tags and display them as plain text.
         
         * if st.button("Get Started"): st.session_state['page'] = 'ext_mod': This line adds a button with the label "Get Started" to the home page. When the button is clicked, it sets a session state variable named 'page' to the value 'ext_mod'. The session state is a way to store and persist data across different pages of the application. By setting the 'page' variable to 'ext_mod', it likely serves as a signal to the application to navigate to another page, presumably the page for extracting and modifying business card data.
      


  2. Extraction and Modification process page:
     The ext_mod_page() function handles different aspects of the business card processing, depending on the option selected by the user. It offers features to upload, extract, modify, and delete business card data interactively.
  

           The function displays a title and a radio button group with three options: "Upload, Extract And Save Card To Database," "Update And Save Card To Database," and "Delete Card From The Database." Based on the selected option, different sections are shown.

            Section 1: Upload & Extract
         
            - Allows users to upload a business card image.
            - Displays the uploaded image and extracts contact information using OCR.
            - Shows the extracted data in a table.
            - Provides buttons to process the image further and save the data to a MySQL database.
     
            Section 2: Modify
         
            - Displays when "Update And Save Card To Database" is selected.
            - Allows users to select a card holder from a list and modify their information.
            - Provides a button to update the modified data in the database.
            - Shows a button to view all updated data in a DataFrame.
     
            Section 3: Delete
         
            - Displays when "Delete Card From The Database" is selected.
            - Allows users to select a card holder from a list for deletion.
            - Shows a warning message with an emoji for confirmation.
            - Provides a button to delete the selected card holder's information from the database.
      




## App Screenshots
![Screenshot (13)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/77a31be3-6e47-4db1-91ec-61682b70b198)

![Screenshot (14)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/3fca61a4-c803-4f2e-9162-c33d9abb8449)

![Screenshot (15)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/ff094a49-c0a3-4096-a68f-861a1182f7a9)

![Screenshot (23)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/03eef43d-7f8c-481b-8170-4be5b0d0945a)

![Screenshot (16)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/495c738f-37e6-495d-943f-93be23803da3)

![Screenshot (17)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/c99ec88a-cac4-48ae-9873-6fc504a24de4)

![Screenshot (18)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/a58fe8c8-d85c-4a9d-bb13-101bd74352fb)

![Screenshot (19)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/dfbe63ea-9ae7-441b-8e86-3277b3660486)

![Screenshot (20)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/fb8609f5-64c1-422d-ba00-9f4aac3cec9c)

![Screenshot (21)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/48fd588f-6f2c-49fd-b665-87f5f2a0df78)

![Screenshot (22)](https://github.com/preky777/BizCardX-Extracting-Business-Card-Data-with-OCR/assets/107749942/87580365-2fe8-42ce-8418-e7263c1cdac2)
