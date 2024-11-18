import streamlit as st
from streamlit_option_menu import option_menu
import main, db_viewer

# Page configuration
st.set_page_config(
    page_title="Interview ChatBot",
    layout="wide"
)

# Custom CSS with glass morphism effect
st.markdown("""
    <style>
    /* Main Background and Container */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #363636 100%);
    }
    
    /* Glass Container Style */
    .css-1d391kg, .css-12oz5g7 {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 1rem !important;
        padding: 2rem !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar Styling */
    .css-1r6slb0 {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 1rem !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Option Menu Container */
    [data-testid="stSidebarNav"] {
        background: transparent !important;
        padding: 1rem !important;
    }
    
    /* Menu Title */
    .nav-link {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0.5rem !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .nav-link:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateX(5px);
    }
    
    .nav-link-selected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 0.5rem !important;
    }
    
    /* Title Style */
    .css-10trblm.e16nr0p30 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        border-radius: 2rem !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Text Input & Select Box Styling */
    .stTextInput > div > div, .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0.5rem !important;
        color: white !important;
    }
    
    /* Alert/Info Box Styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Custom Option Menu Styling */
    .menu-title {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        text-align: center !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-bottom: 1rem !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .css-10trblm.e16nr0p30 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            padding: 0.5rem 1.5rem !important;
            font-size: 0.875rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        # Sidebar with glass morphism effect
        with st.sidebar:
            st.markdown('<div class="menu-title">Categorization Tools</div>', unsafe_allow_html=True)
            
            app = option_menu(
                menu_title=None,  # Remove default menu title
                options=['🛠️ Tool', '🗄️ Database'],
                icons=['tools', 'database-fill'],  # Added icons
                default_index=1,
                styles={
                    "container": {
                        "padding": "0.5rem",
                        "background-color": "transparent"
                    },
                    "icon": {
                        "color": "white",
                        "font-size": "1.2rem"
                    },
                    "nav-link": {
                        "color": "white",
                        "font-size": "1.1rem",
                        "text-align": "left",
                        "padding": "1rem",
                        "border-radius": "0.5rem",
                        "margin": "0.5rem 0",
                        "--hover-color": "rgba(255, 255, 255, 0.1)"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "color": "white"
                    },
                }
            )
            
            # Add some space and additional info in sidebar
            st.markdown("---")
            
        # Main content with glass container effect
        st.markdown("""
            <div style='padding: 2rem; background: rgba(255, 255, 255, 0.05); 
            border-radius: 1rem; backdrop-filter: blur(10px);'>
        """, unsafe_allow_html=True)
        
        if app == '🛠️ Tool':
            main.app()
        if app == '🗄️ Database':
            db_viewer.app()
            
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app = MultiApp()
    app.run()