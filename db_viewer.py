import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def app():
    # Apply custom CSS
    st.markdown("""
        <style>
        /* Main Background and Container */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Glass Container Style */
        .css-1d391kg, .css-12oz5g7 {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 1rem !important;
            padding: 2rem !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Title Style */
        .css-10trblm.e16nr0p30 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar Styling */
        .css-1r6slb0 {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 1rem !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
        }
        
        /* Select Box Styling */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 0.5rem !important;
            color: white !important;
        }
        
        /* Multiselect Styling */
        .stMultiSelect > div > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 0.5rem !important;
            color: white !important;
        }
        
        /* DataFrame Styling */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 1rem !important;
            padding: 1rem !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Metric Container Styling */
        [data-testid="stMetricValue"] {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 1rem;
            padding: 1rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white !important;
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
        
        /* Slider Styling */
        .stSlider > div > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* Text Input Styling */
        .stTextInput > div > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 0.5rem !important;
            color: white !important;
        }
        
        /* Info Box Styling */
        .stAlert {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 1rem !important;
            padding: 1rem !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Subheader Styling */
        .css-10trblm {
            color: white !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin: 1rem 0 !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Error Message Styling */
        .stError {
            background: rgba(220, 38, 38, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 1rem !important;
            border: 1px solid rgba(220, 38, 38, 0.2) !important;
            color: white !important;
        }
        
        /* Download Button Styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
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
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
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

    # Database connection setup
    connection_string = f'mysql+pymysql://root:@localhost/newspaper'
    try:
        engine = create_engine(connection_string)
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        st.stop()

    # Fetch tables
    try:
        tables = pd.read_sql_query("SHOW TABLES", engine)
    except Exception as e:
        st.error(f"Error fetching tables: {str(e)}")
        st.stop()

    # Main title with emoji
    st.title("📊 Newspaper Database Viewer")

    # Create three columns for the header stats
    col1, col2, col3 = st.columns(3)
    
    try:
        with col1:
            total_tables = len(tables)
            st.metric("Total Tables", total_tables)
        
        table_names = tables.values.flatten().tolist()
        
        # Sidebar with glass morphism
        with st.sidebar:
            st.markdown
            
            selected_table = st.selectbox("Select Table", table_names)
            display_option = st.selectbox(
                "Choose display type",
                ["Table View", "Interactive Analysis", "Data Statistics"]
            )

        # Main content
        try:
            query = f"SELECT * FROM {selected_table}"
            df = pd.read_sql_query(query, engine)
            
            if display_option == "Table View":
                st.subheader("📋 Table View")
                
                # Info box with record count
                st.info(f"📊 Total records: {len(df)}")
                
                # Filter section
                with st.expander("🔍 Filter Data", expanded=True):
                    filter_cols = st.multiselect("Select columns to filter:", df.columns.tolist())
                    
                    filtered_df = df.copy()
                    for col in filter_cols:
                        if df[col].dtype in ['int64', 'float64']:
                            min_val = float(df[col].min())
                            max_val = float(df[col].max())
                            filter_range = st.slider(f"Filter {col}", min_val, max_val, (min_val, max_val))
                            filtered_df = filtered_df[filtered_df[col].between(filter_range[0], filter_range[1])]
                        else:
                            unique_values = df[col].unique().tolist()
                            selected_values = st.multiselect(f"Select {col}", unique_values, default=unique_values)
                            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
                
                st.dataframe(filtered_df)
                
            elif display_option == "Interactive Analysis":
                st.subheader("🔍 Interactive Analysis")
                
                # Search and Analysis Section
                with st.expander("🔎 Search and Analyze", expanded=True):
                    selected_columns = st.multiselect("Select columns:", df.columns.tolist(), default=df.columns.tolist())
                    search_term = st.text_input("🔍 Search across all columns:")
                    
                    if search_term:
                        filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
                        filtered_df = filtered_df[selected_columns]
                    else:
                        filtered_df = df[selected_columns]
                    
                    st.dataframe(filtered_df)
                    st.write(f"📊 Showing {len(filtered_df)} out of {len(df)} records")
                
                # Numeric Insights
                if len(filtered_df.select_dtypes(include=['int64', 'float64']).columns) > 0:
                    st.subheader("📈 Quick Insights")
                    numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns
                    selected_numeric = st.selectbox("Select numeric column:", numeric_cols)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean", f"{filtered_df[selected_numeric].mean():.2f}")
                    with col2:
                        st.metric("Median", f"{filtered_df[selected_numeric].median():.2f}")
                    with col3:
                        st.metric("Count", f"{filtered_df[selected_numeric].count()}")
            
            elif display_option == "Data Statistics":
                st.subheader("📊 Statistics")
                
                # Statistics Tabs
                tab1, tab2 = st.tabs(["📈 Numeric Stats", "ℹ️ Column Info"])
                
                with tab1:
                    numeric_stats = df.describe()
                    st.dataframe(numeric_stats)
                
                with tab2:
                    col_info = pd.DataFrame({
                        'Data Type': df.dtypes,
                        'Non-Null Count': df.count(),
                        'Null Count': df.isna().sum(),
                        'Unique Values': df.nunique()
                    })
                    st.dataframe(col_info)
            
            # Download section
            with st.expander("📥 Download Options", expanded=False):
                if st.button("Generate CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{selected_table}.csv",
                        mime="text/csv"
                    )
                
        except Exception as e:
            st.error(f"⚠️ Error processing data: {str(e)}")

    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    app()