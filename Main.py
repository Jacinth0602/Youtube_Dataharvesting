import streamlit as st

from streamlit_option_menu import option_menu


import Youtube_DataScrap, Queries, Home

st.set_page_config(
page_title="Youtube Data Harvesting and Data Warehousing",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Menu',
                options=['Home','Youtube Scrap','Queries'],
                icons=['house-fill','globe','question'],
                menu_icon='100',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'Black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "orange"},
        "nav-link-selected": {"background-color": "#FF4B4B"},}
                
                )
        for a in self.apps:
            if app == a["title"]:
                a["function"]()
# Create an instance of MultiApp
multi_app = MultiApp()

# Add your apps to the MultiApp instance
multi_app.add_app("Home", Home.app)
multi_app.add_app("Youtube Scrap", Youtube_DataScrap.app)
multi_app.add_app("Queries", Queries.app)


# Run the MultiApp
multi_app.run()
          
         