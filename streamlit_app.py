import streamlitç
import pandas
import requests
import snowflake.connector
from urllib.error import URLERROR

streamlit.title('My moms new healthy diner')

streamlit.header('Breakfast favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled ree-Range Egg')
streamlit.text(' 🥑🍞Avocado toast')
 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#NEW section to display fruity api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
       streamlit.error("Please select a fruit to ger informatcion.")
  else:
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       streamlit.dataframe(fruityvice_normalized)

except URLError as e:
 streamlit.error()

#don not run anything past here while we troubleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#allow the end user to add a fruit to the list - que añada manualmente una fruta
#add_my_fruit = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.append('Thanks for adding', add_my_fruit)

#this will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
