#import required libraries
import streamlit as st
import pandas as pd
import oracledb
import numpy as np
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import datetime
import dateutil.relativedelta
import time
from stqdm import stqdm
import matplotlib.pyplot as plt
import seaborn as sns
import os
import altair as alt
from PIL import Image
from datetime import date
import sys
import logging
from logging.handlers import RotatingFileHandler

#load logo
im = Image.open('logo.jpg')

#Configuring the main page with backgorund color, title and logo
st.set_page_config(page_title="Price Reporting", page_icon=im, layout="wide", initial_sidebar_state="auto", menu_items=None)
original_title = '<center><p style="margin-top:-40px;font-family:bold; color:#184a7d; font-size: 50px; background-color:#ebfcfc;border: 1px solid #bae8f5;border-radius:5px;">Price Reporting</p></center>'
st.markdown(original_title, unsafe_allow_html=True)
oos_limit = 7

#log set up 
if not os.path.isdir(os.getcwd()+'/'+date.today().strftime('%m-%d-%Y')):
    os.mkdir(os.getcwd()+'/'+date.today().strftime('%m-%d-%Y'))
    
app_log = logging.getLogger('root')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = os.getcwd()+'\\'+date.today().strftime('%m-%d-%Y')+'\\reporting_app'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=10*1024*1024, backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)

def _all():
    """Function to call when department, collection and sku filters selected as ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df, height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df))
    return grid_table

def dept_all():
    """Function to call when department filter selected as ALL and collection, sku filters selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['Collection'] == st.session_state.coll) & (grid_df['SKU'] == st.session_state.sku)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['Collection'] == st.session_state.coll) & (grid_df['SKU'] == st.session_state.sku)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['SKU'] == st.session_state.sku)]))
    return grid_table
  
def sku_all():
    """Function to call when sku filter selected as ALL and department, collection filters selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll)]))
    return grid_table

def col_all():
    """Function to call when collection filter selected as ALL and department, sku filters selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['SKU'] == st.session_state.sku)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['SKU'] == st.session_state.sku)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['SKU'] == st.session_state.sku)]))
    return grid_table

def all_selected():
    """Function to call when department, collection, sku filters selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll) & (grid_df['SKU'] == st.session_state.sku)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll) & (grid_df['SKU'] == st.session_state.sku)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll) & (grid_df['SKU'] == st.session_state.sku)]))
    return grid_table

def coll_sku_all():
    """Function to call when collection, sku filters selected as ALL and department filter selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['Department'] == st.session_state.dept)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['Department'] == st.session_state.dept)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['Department'] == st.session_state.dept)]))
    return grid_table

def dept_sku_all():
    """Function to call when department, sku filters selected as ALL and collection filter selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['Collection'] == st.session_state.coll)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['Collection'] == st.session_state.coll)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['Collection'] == st.session_state.coll)]))
    return grid_table

def dept_coll_all():
    """Function to call when department, collection filters selected as ALL and sku filter selection is not ALL
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Filtering the price input tab table based on selected filters")
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%m/%d/%Y')
    gd = GridOptionsBuilder.from_dataframe(grid_df[(grid_df['SKU'] == st.session_state.sku)])
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(grid_df[(grid_df['SKU'] == st.session_state.sku)], height=250, gridOptions=gridoptions,update_mode=GridUpdateMode.SELECTION_CHANGED)
    grid_df['Price Change Date'] = pd.to_datetime(grid_df['Price Change Date']).dt.strftime('%d/%m/%Y')
    st.write("Total rows : ",len(grid_df[(grid_df['SKU'] == st.session_state.sku)]))
    return grid_table

#funtion to convert the input dataframe to csv format
def convert_df(df):
    """Function to call when department, collection filters selected as ALL and sku filter selection is not ALL
    :Parameters:
    -----------
            df : dataframe to convert into csv format
    
    :Returns:
    --------
    returns csv formatted dataframe
    """
    app_log.info("Convert input dataframe into csv format and return as function output")
    return df.to_csv().encode('utf-8')

def filter_change():
    """Function to call when there is a change in department, collection, sku filters
    
    :Returns:
    --------
    returns data based on the filters selected
    """
    app_log.info("Selected Filters:"+st.session_state.dept+", "+st.session_state.coll+", "+st.session_state.sku)
    if (st.session_state.dept == 'ALL') and (st.session_state.coll == 'ALL') and (st.session_state.sku == 'ALL'):
        data = _all()
    elif (st.session_state.dept != 'ALL') and (st.session_state.coll == 'ALL') and (st.session_state.sku == 'ALL'):
        data = coll_sku_all()
    elif (st.session_state.dept == 'ALL') and (st.session_state.coll !='ALL') and (st.session_state.sku == 'ALL'):
        data = dept_sku_all()
    elif (st.session_state.dept == 'ALL') and (st.session_state.coll == 'ALL') and (st.session_state.sku != 'ALL'):
        data = dept_coll_all()
    elif (st.session_state.dept == 'ALL') and (st.session_state.coll != 'ALL') and (st.session_state.sku != 'ALL'):
        data = dept_all()
    elif (st.session_state.dept != 'ALL') and (st.session_state.coll == 'ALL') and (st.session_state.sku != 'ALL'):
        data = col_all()
    elif (st.session_state.dept != 'ALL') and (st.session_state.coll != 'ALL') and (st.session_state.sku == 'ALL'):
        data = sku_all()
    elif (st.session_state.dept != 'ALL') and (st.session_state.coll == 'ALL') and (st.session_state.sku == ' ALL'):
        data = coll_sku_all()
    elif (st.session_state.dept == 'ALL') and (st.session_state.coll != 'ALL') and (st.session_state.sku == ' ALL'):
        data = dept_sku_all()
    elif (st.session_state.dept == 'ALL') and (st.session_state.coll == 'ALL') and (st.session_state.sku != ' ALL'):
        data = dept_coll_all()
    else:
        data = all_selected()
    return data

@st.cache(allow_output_mutation=True,ttl=3600)
def get_connection():
    """Function to connect to database
    
    :Returns:
    --------
    returns database connect instance
    """
    app_log.info("Connecting to database")
    return oracledb.connect(user = sys.argv[1], password = sys.argv[2],
                    host = "dfw-prd-ora-dss-1", port = 1521, sid="dssp")

@st.cache(suppress_st_warning=True, ttl = 3600)
def get_onetimebuy(query):
    """Function to get one time buy data from the database
    :Parameters:
    -----------
            query : query to execute
    
    :Returns:
    --------
    returns executed query result
    """
    app_log.info("Fetching one time buy data from the database")
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    col_names = list(pd.DataFrame(cur.description)[0])
    data = pd.DataFrame(data,columns=col_names)
    return data

@st.cache(allow_output_mutation=True,suppress_st_warning=True)
def get_promo_and_offer(query):
    """Function to get promotion and offers data from database
    :Parameters:
    -----------
            query : query to execute
    
    :Returns:
    --------
    returns executed query result
    """
    app_log.info("Get promotions and offers data from the database")
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    col_names = list(pd.DataFrame(cur.description)[0])
    data = pd.DataFrame(data,columns=col_names)
    return data

@st.cache(suppress_st_warning=True,allow_output_mutation=True,ttl=3600)
def uploading_master_report(file):
    """Function to read master report data
    :Parameters:
    -----------
            file : master report data in v3 format
    
    :Returns:
    --------
    returns dataframe and weeks availablein master report data
    """
    if file is not None:
        app_log.info("Reading master report data")
        dataframe = pd.read_excel(file, header = [5,6,7,8], sheet_name = 'Report')
        li = [d for a,b,c,d in dataframe.columns[0:67]]
        li1 = [f'{c}{d}' for a,b,c,d in dataframe.columns[67:]]
        week = [b for a,b,c,d in dataframe.columns[67:119]]
        dataframe.columns = li + li1
        return dataframe,week

@st.cache(suppress_st_warning=True, allow_output_mutation=True,ttl=3600)
def read_offers_file(file):
    """Function to read promotions and offers data
    :Parameters:
    -----------
            file : promotions and offers file
    
    :Returns:
    --------
    returns promotions and offers dataframe
    """
    app_log.info("Reading promotions and offers data")
    promotions = pd.read_excel(file, sheet_name = 'Promotions ')
    offers = pd.read_excel(file, sheet_name = 'Offers ')
    return offers, promotions

@st.cache(suppress_st_warning=True, allow_output_mutation=True,ttl=3600)
def get_kpi_data_from_report():
    """Function to get kpi data(gross margin, oos, net sales, net sales qty) from master report data
    
    :Returns:
    --------
    returns dataframe
    """
    app_log.info("Fetching only useful data from master report for futher analysis")
    cols = data_with_header.columns[67:119]
    temp_cols = [f'{i}{j}' for i,j in zip(week,cols)]
    d = {}
    for i,j in zip(cols,temp_cols):
        d[i] = j
    cols = list(cols)
    cols.insert(0,'Sku')
    data_with_header[cols].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="gm")
    gm = data_with_header[cols].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="gm")
    sku_qty = [i.replace('GM $','Net Sales Qty') for i in cols]
    data_with_header[sku_qty].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="net sales qty")
    qty = data_with_header[sku_qty].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="net sales qty")
    sku_ns = [i.replace('GM','Net Sales') for i in cols]
    data_with_header[sku_ns].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="net sales")
    ns = data_with_header[sku_ns].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="net sales")
    sku_oos = [i.replace('GM $','Store OOS %') for i in cols]
    data_with_header[sku_oos].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="oos")
    oos = data_with_header[sku_oos].melt(id_vars=["Sku"], 
        var_name="Date", 
        value_name="oos")
    final_df= gm
    final_df['Net Sales Qty'] = qty['net sales qty']
    final_df['Net Sales'] = ns['net sales']
    final_df['OOS%'] = oos['oos']
    final_df['Date'] = final_df['Date'].map(d)
    return final_df
    
@st.cache(suppress_st_warning=True, allow_output_mutation=True,ttl=3600)
def clean_the_data(final_df):
    """Function to format and make data clean for further analysis
    
    :Returns:
    --------
    returns dataframe
    """
    app_log.info("Formatting and making data clean for further analysis")
    final_df['WEEK'] = final_df['Date'].str[4:6]
    final_df['Mon'] = final_df['Date'].str[15:18]
    final_df['YEAR'] = final_df['Date'].str[19:23]
    mon_dict = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12}
    final_df['MONTH'] = final_df['Mon'].map(mon_dict)
    final_df['DD-MM-YYYY'] = final_df['Date'].str[12:14].astype(str)+ "-" + final_df['MONTH'].astype(str)+ "-" + final_df['YEAR']
    final_df['MONTH-YEAR'] = final_df['MONTH'].astype(str)+ "-" + final_df['YEAR']
    final_df['ACTUAL_WEEK'] = pd.to_datetime(final_df['DD-MM-YYYY'], dayfirst = True).dt.week
    df = final_df[['Sku','WEEK','ACTUAL_WEEK','MONTH-YEAR','DD-MM-YYYY','Net Sales Qty','Net Sales','gm','OOS%']].rename(columns = {'Sku':'SKU','Net Sales Qty':'NET SALES QTY','Net Sales':'NET SALES','gm':'GM'})
    df = df.dropna(axis = 0, subset = ['SKU'])
    df['SKU'] = df['SKU'].astype(int)
    oos_d = df.dropna()[['SKU','WEEK','ACTUAL_WEEK','MONTH-YEAR','DD-MM-YYYY','NET SALES QTY','NET SALES','GM','OOS%']].groupby(['SKU','WEEK','ACTUAL_WEEK','MONTH-YEAR','DD-MM-YYYY']).sum()
    oos_d.reset_index(inplace = True)
    oos_d['ONETIMEBUY'] = 0
    return oos_d

try:
    #create tabs
    price_input_tab, price_change_report_tab, kpi_tab = st.tabs(["Price Input", "Price Change Report", "KPI"])
    
    #price_input_tab to filter and select skus for report generate
    with price_input_tab:
    
        #css to style the page
        st.markdown("""<style>[data-baseweb="select"] {margin-top: -140px;background-color:#d7f1fa;border: 1px solid #bae8f5;border-radius:5px;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>[data-baseweb="input"] {margin-top: -140px;background-color:#d7f1fa;border: 1px solid #bae8f5;border-radius:5px;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>.css-184tjsw p {font-size: 20px;color:#184a7d;font-family:bold;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>.ag-cell-label-container {font-size: 10px;background-color: #bde9ba;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>p {font-size: 18px;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>[data-testid = stFileUploader] {margin-top: -120px;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>.css-1x8cf1d {font-size: 18px;background-color:#ebfcfc;font-family:bold; color:#184a7d;border: 1px solid #bae8f5;border-radius:5px;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>.st-fb,.st-e3,.st-d4,.st-ef,.st-eg {background-color:#ebfcfc;font-family:bold; color:#184a7d;}</style>""",unsafe_allow_html=True)
        st.markdown("""<style>.ag-header {background-color:#ebfcfc;font-family:bold; color:#184a7d;}</style>""",unsafe_allow_html=True)
        
        read_master_report, file2, read_promotios = st.columns(3)
        
        #file uploader to read master data
        with read_master_report:
            holder1 = st.empty()
            app_log.info("upload master report data")
            uploaded_file = holder1.file_uploader("Upload Master Report Data :")
            if uploaded_file is not None:
                data_with_header,week = uploading_master_report(uploaded_file)
            
        #file uploader to read promotions and offers data
        with read_promotios:
            holder2 = st.empty()
            app_log.info("upload promotions and offers data")
            offers_file = holder2.file_uploader("Upload Offers and Promotions Data :")
            if offers_file is not None:
                offers_data, promotions_data = read_offers_file(offers_file)
                holder1.empty()
                holder2.empty()
                
        #make sure user uploads valid data
        if uploaded_file is not None and offers_file is not None:
            app_log.info("Both uploded files are accepted")
            #get only required columns from master data
            frst_price_inp_data_no_na = data_with_header.dropna(axis=0, subset=['PC Date'])[['Sku','Advertising Description','Department','Vendor','Sku Status','Class','SubClass','Master Collection','Collection','Pricing Collection','Most Recent Price Change Amt','PC Date']]
            sec_price_inp_data_no_na = data_with_header.dropna(axis=0, subset=['2nd PC Date'])[['Sku','Advertising Description','Department','Vendor','Sku Status','Class','SubClass','Master Collection','Collection','Pricing Collection','2nd Most Recent  Price Change Amt','2nd PC Date']]
            thrd_price_inp_data_no_na = data_with_header.dropna(axis=0, subset=['3rd PC Date'])[['Sku','Advertising Description','Department','Vendor','Sku Status','Class','SubClass','Master Collection','Collection','Pricing Collection','3rd Most Recent Price Change Amt','3rd PC Date']]
            frst_price_inp_data_no_na.rename(columns = {'Most Recent Price Change Amt':'Price'},inplace = True)
            sec_price_inp_data_no_na.rename(columns = {'2nd Most Recent  Price Change Amt':'Price','2nd PC Date':'PC Date'}, inplace = True)
            thrd_price_inp_data_no_na.rename(columns = {'3rd Most Recent Price Change Amt':'Price','3rd PC Date':'PC Date'}, inplace = True)
            grid_df = pd.concat([frst_price_inp_data_no_na,sec_price_inp_data_no_na,thrd_price_inp_data_no_na], axis = 0)
            grid_df = grid_df[['Sku','Advertising Description','Price','PC Date','Department','Sku Status','Vendor','Class','SubClass','Master Collection','Collection','Pricing Collection']].rename(columns = {'Sku':'SKU','Advertising Description':'Description','PC Date':'Price Change Date'})
            grid_df.rename(columns = {'Sku':'SKU','Advertising Description':'Description','PC Date':'Price Change Date'}, inplace = True)
            unique_depts = list(['KITCHEN'])
            #unique_depts = list(grid_df['Department'].unique())
            #unique_depts.insert(0,'ALL')
            
            department_filter, collection_filter, sku_filter, start_date_filter, end_date_filter = st.columns(5)
            
            #Department filter
            with department_filter:
                app_log.info("add department filter in price input tab")
                st.markdown('<p style="margin-top: -130px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the Department :</p>', unsafe_allow_html=True)
                dept_menu = st.selectbox('', unique_depts, key = 'dept')
        
            #get collection data based on department selected
            if st.session_state.dept == 'ALL':
                unique_colls = list(grid_df['Collection'].unique())
            else:
                unique_colls = list(grid_df[grid_df['Department'] == st.session_state.dept]['Collection'].unique())
                
            unique_colls.sort()
            unique_colls.insert(0,'ALL')
            
            #Collection filter
            with collection_filter:
                app_log.info("add collection filter in input price tab")
                st.markdown('<p style="margin-top: -130px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the Collection :</p>', unsafe_allow_html=True)
                coll_menu = st.selectbox('', unique_colls, key = 'coll')
        
            #get sku data based on department and collection selected
            if (st.session_state.dept == 'ALL') & (st.session_state.coll == 'ALL'):
                unique_skus = list(grid_df['SKU'].unique())
            elif (st.session_state.dept == 'ALL') & (st.session_state.coll != 'ALL'):   
                unique_skus = list(grid_df[grid_df['Collection'] == st.session_state.coll]['SKU'].unique())
            elif (st.session_state.dept != 'ALL') & (st.session_state.coll == 'ALL'):
                unique_skus = list(grid_df[grid_df['Department'] == st.session_state.dept]['SKU'].unique())
            else:
                unique_skus = list(grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll)]['SKU'].unique())
            
            unique_skus = [int(i) for i in unique_skus]
            unique_skus.sort()
            unique_skus.insert(0,'ALL')
    
            #SKU filter
            with sku_filter:
                app_log.info("add sku filter in input price tab")
                st.markdown('<p style="margin-top: -130px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the SKU :</p>', unsafe_allow_html=True)
                sku_menu = st.selectbox('', unique_skus, key = 'sku')
                
            #get kpi data from master report
            kpi_data = get_kpi_data_from_report()
            
            #get final data for analysis
            oos_d = clean_the_data(kpi_data)
            
            #start date filter for comparision
            with start_date_filter:
                app_log.info("add start date filter in price input tab")
                st.markdown('<p style="margin-top: -130px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the Period - Start Date :</p>', unsafe_allow_html=True)
                frm = st.date_input('', min_value = min(pd.to_datetime(oos_d['DD-MM-YYYY'], dayfirst = True)), max_value = max(pd.to_datetime(oos_d['DD-MM-YYYY'], dayfirst = True)), value = min(pd.to_datetime(oos_d['DD-MM-YYYY'], dayfirst = True)))
            
            #end date filter for comparision
            with end_date_filter:
                app_log.info("add end date filter in price input tab")
                st.markdown('<p style="margin-top: -130px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">End Date :</p>', unsafe_allow_html=True)
                to = st.date_input('', min_value = min(pd.to_datetime(oos_d['DD-MM-YYYY'], dayfirst = True)), max_value = max(pd.to_datetime(oos_d['DD-MM-YYYY'], dayfirst = True)), value = max(pd.to_datetime(oos_d['DD-MM-YYYY'], dayfirst = True)))
            
            select_all_checkbox, download_data_button = st.columns([50,9])
            
            #select_all checkbox to generate report for all the rows displayed in input_tab
            with select_all_checkbox:
                app_log.info("add select all checkbox in price input tab")
                agree = st.checkbox('Select all')
                
            data = filter_change()
            if agree:
                data.selected_rows = data.data
            csv = convert_df(data.data)
            
            #button to download the data displayed in input_tab
            app_log.info("add download button in price input tab")
            with download_data_button:
                st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='large_df.csv',
                mime='text/csv',
                )
    
            #get one time buy data from data base
            app_log.info("query to get one time buy information")
            query = '''select	a11.SKU  SKU,NVL(a11.DESC_B, a11.DESC_A)  DESC_A,max(a11.SKU)  WJXBFS1 from	DSSMGR."DT1_ITEM" a11 where(((a11.SKU)		
            in(select s22.SKU from DSSMGR."DT1_ITEM_ATTRIBUTE_MATRIX" s22 where	s22.ATTR_VALUE_ID in ('YESONETIMEBUY'))) and a11.STATUS in ('A'))			
            group by a11.SKU,NVL(a11.DESC_B, a11.DESC_A)'''
            ses_data = get_onetimebuy(query)
        
            #flag skus with one time buy
            app_log.info("flag skus with one time buy")
            for sku in ses_data['SKU']:
                oos_d.loc[(oos_d['SKU'] == sku),['ONETIMEBUY']]=1
        
            app_log.info("Check any promotion applied for that week")
            def check_promo(li):
                """Function to check is there any on going promotions for that week(input)
    
                :Returns:
                --------
                returns 1 if that week has promotions else returns 0
                """
                cou = [i for i in li if i]
                if len(set(cou).intersection(promotion_codes)) > 0:
                    return 1
                else:
                    return 0
            
            app_log.info("Check any offer applied for that week")
            def check_offer(li):
                """Function to check is there any on going offers for that week(input))
    
                :Returns:
                --------
                returns 1 if that week has offers else returns 0
                """
                cou = [i for i in li if i]
                if len(set(cou).intersection(set(offer_codes))) > 0:
                    return 1
                else:
                    return 0
        
            #dataframe to store the final generated report for skus find comparable
            app_log.info("dataframe to store final report for skus which has comparable periods")
            res_df = pd.DataFrame({'Vendor':[],'SKU':[],'PRICE':[],'LAST PRICE':[],'PRICE CHANGE DATE':[],'BEFORE_PRICE_CHANGE':[],'AFTER_PRICE_CHANGE':[],'BEFORE':[],'AFTER':[],'BEFORE PRICE CHANGE':[],
            'AFTER PRICE CHANGE':[],'BEFORE PRICE CHANGE $':[],'AFTER PRICE CHANGE $':[],'BEFORE_PRICE CHANGE':[],'AFTER_PRICE CHANGE':[],'BEFORE PRICE_CHANGE %':[],'AFTER PRICE_CHANGE %':[],'BEFORE PRICE CHANGE %':[],'AFTER PRICE CHANGE %':[]})
            columns=[('','Vendor'),('','SKU'),('','PRICE'),('','LAST PRICE'),('','PRICE CHANGE DATE'),('WEEKS','BEFORE_PRICE_CHANGE'),('WEEKS','AFTER_PRICE_CHANGE'),('BEYOND 3 MONTHS','BEFORE'),('BEYOND 3 MONTHS','AFTER'),('NET SALES','BEFORE PRICE CHANGE'),('NET SALES','AFTER PRICE CHANGE'),('GROSS PROFIT','BEFORE PRICE CHANGE $'),('GROSS PROFIT','AFTER PRICE CHANGE $'),
            ('UNITS','BEFORE_PRICE CHANGE'),('UNITS','AFTER PRICE CHANGE'),('GROSS MARGIN RATE','BEFORE PRICE_CHANGE %'),('GROSS MARGIN RATE','AFTER PRICE_CHANGE %'),('OOS','BEFORE PRICE CHANGE %'),('OOS','AFTER PRICE CHANGE %')]
            res_df.columns=pd.MultiIndex.from_tuples(columns)
            
            #dataframe to store the final generated report for skus not find comparable
            app_log.info("dataframe to store final report for skus which has no comparable periods")
            no_com_df = pd.DataFrame({'SKU':[],'PRICE':[],'PRICE CHANGE DATE':[]})
            
            temp1,temp2,temp3,submit_button,temp5,temp6,temp7 = st.columns(7)
            
            #submit button
            with submit_button:
                app_log.info("add submit button in price input tab")
                click = st.button('Submit')
            
            #price change report tab where generated reports will be shown
            with price_change_report_tab:
                app_log.info("price change report tab")
                #get file path and check file exists or not
                os.path.isfile("report_data.csv")
                if (os.path.isfile("report_data.csv")) & (not click) & (os.path.isfile("add_info.csv")):
                    temp_data = pd.read_csv('report_data.csv')
                    temp_data.drop(columns = ['Unnamed: 0'], inplace = True)
                    temp_data.rename(columns = {'Unnamed: 1':'','Unnamed: 2':' ','Unnamed: 3':'  ','Unnamed: 4':'   ','Unnamed: 5':'    ','TIME PERIOD.1':'TIME PERIOD ','TIME PERIOD.2':'TIME PERIOD  ',
                    'TIME PERIOD.3':'TIME PERIOD   ','GROSS PROFIT.1':'GROSS PROFIT ','GROSS MARGIN RATE.1':'GROSS MARGIN RATE ','NET SALES.1':'NET SALES ',
                    'OOS.1':'OOS ','UNITS.1':'UNITS ','BEYOND 3 MONTHS.1':'BEYOND 3 MONTHS '}, inplace = True)
                    
                    #display skus with comparable periods
                    app_log.info("display skus with comparable periods")
                    st.write("These are the comparable periods for the following SKUs:")
                    st.dataframe(temp_data)
                    csv = convert_df(temp_data)
                    st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='large_df.csv',
                    mime='text/csv',
                    )
                    
                    #display skus with no comparable periods
                    app_log.info("display skus with no comparable periods")
                    st.write("These are no comparable periods found for the following SKUs:")
                    add_info = pd.read_csv('add_info.csv')
                    add_info.drop(columns = ['Unnamed: 0'], inplace = True)
                    add_info['PRICE'] = [str(round(i,2)) for i in add_info['PRICE']]
                    st.dataframe(add_info)

                #check atleast one row is selected to generate report
                if ((len(data.selected_rows) > 0) & click):
                    data.selected_rows = pd.DataFrame(data.selected_rows)
                    for i in stqdm(range(0,len(data.selected_rows))):
                        #read each record sku, price, price change date, vendor 
                        sku = data.selected_rows.iloc[i]['SKU']
                        price = data.selected_rows.iloc[i]['Price']
                        date = pd.to_datetime(data.selected_rows.iloc[i]['Price Change Date'])
                        vendor = data.selected_rows.iloc[i]['Vendor']
                        app_log.info("finding comparable periods for the sku with pice and dates are :",sku,price,date)
                        
                        #query to get promotion and offer data from data base for the selected sku
                        app_log.info("get promotions and offers data from the database for the sku :",sku)
                        query = '''select C$_PROCESS_DATE,SKU,DEPT_NAME,ITEM_PROMO_CODE,ITEM_PRICE_OVERRIDE_CODE,ITEM_SALES_AMT,ITEM_QTY,RETAIL_PRICE,COST_PRICE from SJUNEJA.PRICING_ORDER_FG_N_HIERARCHY WHERE SKU ='''+ str(sku)
                        pro_data = get_promo_and_offer(query)
                        
                        #compute
                        pro_data['PROFIT'] = pro_data['RETAIL_PRICE'] - pro_data['COST_PRICE']
                        pro_data = pro_data[pro_data['C$_PROCESS_DATE'].notna()]
                        pro_data['ACTUAL_WEEK'] = pd.to_datetime(pro_data['C$_PROCESS_DATE'], dayfirst = True).dt.week
                        d = pro_data[['ACTUAL_WEEK','ITEM_PROMO_CODE','ITEM_PRICE_OVERRIDE_CODE']].groupby('ACTUAL_WEEK').agg({'ITEM_PROMO_CODE':list,'ITEM_PRICE_OVERRIDE_CODE':list})
                        offer_codes = set(offers_data[offers_data['Should a week containing this offer be considered for price change comparison ? (Y/N)'] == 'N']['OFFER CODE'])
                        promotion_codes = set(promotions_data[promotions_data['Should a week containing this promotion be considered for price change comparison ? (Y/N)'] == 'N']['PROMO_CODE'])
                        
                        #check for promotions and offers
                        d['promo'] = d['ITEM_PROMO_CODE'].apply(check_promo)
                        d['offers'] = d['ITEM_PRICE_OVERRIDE_CODE'].apply(check_offer)
                        
                        d.reset_index(0,inplace = True)
                        promo_available_weeks = d['ACTUAL_WEEK']
                        oos_ses_data = oos_d[oos_d['SKU'] == sku]
                        oos_ses_data['PROMOTION'] = 0
                        oos_ses_data['OFFER'] = 0
                        
                        #flag the week with promotions
                        app_log.info("flag weeks which has promotions")
                        for week in list(d['ACTUAL_WEEK']):
                            if d[d['ACTUAL_WEEK'] == week]['promo'].iloc[0] > 0:
                                oos_ses_data.loc[oos_ses_data['ACTUAL_WEEK'] == week ,['PROMOTION']]=1
                        
                        #flag the week with offers
                        app_log.info("flag weeks which has offers")
                        for week in list(d['ACTUAL_WEEK']):
                            if d[d['ACTUAL_WEEK'] == week]['offers'].iloc[0] > 0:
                                oos_ses_data.loc[oos_ses_data['ACTUAL_WEEK'] == week ,['OFFER']]=1
                                
                        oos_ses_data['DD-MM-YYYY'] = pd.to_datetime(oos_ses_data['DD-MM-YYYY'], dayfirst = True)
                        oos_ses_data['OOS%'] = [i*100 for i in oos_ses_data['OOS%']]
                        if (st.session_state.dept == 'ALL') & (st.session_state.coll == 'ALL') & (st.session_state.sku == 'ALL'):
                            sel = grid_df
                        elif (st.session_state.dept != 'ALL') & (st.session_state.coll == 'ALL') & (st.session_state.sku == 'ALL'):
                            sel = grid_df[(grid_df['Department'] == st.session_state.dept)]
                        elif (st.session_state.dept == 'ALL') & (st.session_state.coll != 'ALL') & (st.session_state.sku == 'ALL'):
                            sel = grid_df[(grid_df['Collection'] == st.session_state.coll)]
                        elif (st.session_state.dept == 'ALL') & (st.session_state.coll == 'ALL') & (st.session_state.sku != 'ALL'):
                            sel = grid_df[(grid_df['SKU'] == st.session_state.sku)]
                        elif (st.session_state.dept != 'ALL') & (st.session_state.coll != 'ALL') & (st.session_state.sku == 'ALL'):
                            sel = grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll)]
                        elif (st.session_state.dept == 'ALL') & (st.session_state.coll != 'ALL') & (st.session_state.sku != 'ALL'):
                            sel = grid_df[(grid_df['SKU'] == st.session_state.sku) & (grid_df['Collection'] == st.session_state.coll)] 
                        elif (st.session_state.dept != 'ALL') & (st.session_state.coll == 'ALL') & (st.session_state.sku != 'ALL'):
                            sel = grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['SKU'] == st.session_state.sku)]
                        else:
                            sel = grid_df[(grid_df['Department'] == st.session_state.dept) & (grid_df['Collection'] == st.session_state.coll) & (grid_df['SKU'] == st.session_state.sku)]
                        
                        #get all the dates for the selected sku
                        app_log.info("get all the weeks data available for the sku :",sku)
                        sel = sel[sel['SKU'] == sku]
                        sel['Price Change Date'] = pd.to_datetime(sel['Price Change Date'], dayfirst = True)
                        sel.sort_values(by = 'Price Change Date', ascending = True, inplace = True)
                        sel['ind'] = [j for j in range(len(sel))]
                        sel['SKU'] = sel['SKU'].astype(int)
                        after = sel[sel['ind'] == (sel[sel['Price Change Date'] == date]['ind'].iloc[0])+1]['Price Change Date']
                        
                        #check for other price change dates in after period
                        app_log.info("check for other price changes in after period for the sku :",sku)
                        if len(after) > 0:
                            after = sel[sel['ind'] == (sel[sel['Price Change Date'] == date]['ind'].iloc[0])+1]['Price Change Date'].iloc[0]
                        else:
                            after = None
                        before = sel[sel['ind'] == (sel[sel['Price Change Date'] == date]['ind'].iloc[0])-1]['Price Change Date']
                        last_price = ''
                        
                        #check for other price changes dates in before period
                        app_log.info("check for other price changes in before period for the skus :",sku)
                        if len(before) > 0:
                            before = sel[sel['ind'] == (sel[sel['Price Change Date'] == date]['ind'].iloc[0])-1]['Price Change Date'].iloc[0]
                            last_price = sel[sel['ind'] == (sel[sel['Price Change Date'] == date]['ind'].iloc[0])-1]['Price'].iloc[0]
                        else:
                            before = None
                            
                        bfr_date = pd.to_datetime(before, dayfirst = True)
                        sel_date = pd.to_datetime(sel[sel['ind'] == (sel[sel['Price Change Date'] == date]['ind'].iloc[0])]['Price Change Date'].iloc[0], dayfirst = True)
                        aft_date = pd.to_datetime(after, dayfirst = True)
                        temp = oos_ses_data[oos_ses_data['ACTUAL_WEEK'] == sel_date.week]['DD-MM-YYYY']
                        
                        #fetch only valid weeks for comaparision
                        app_log.info("get only valid weeks for comparision based upon the price changes in before and after period")
                        if len(temp) > 0:
                            if sel_date < temp.iloc[0]:
                                oos_ses_data = oos_ses_data[oos_ses_data['ACTUAL_WEEK'] != ((sel_date.week)-1)]
                            elif sel_date > temp.iloc[0]:
                                oos_ses_data = oos_ses_data[oos_ses_data['ACTUAL_WEEK'] != ((sel_date.week)+1)]
                            elif sel_date == temp.iloc[0]:
                                oos_ses_data = oos_ses_data[oos_ses_data['ACTUAL_WEEK'] != sel_date.week]
                        if (after == None) & (before == None):
                            aft_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] > sel_date)]
                            bfr_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] < sel_date)]
                        elif (after == None) & (before != None):
                            aft_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] > sel_date)]
                            bfr_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] > bfr_date) & (oos_ses_data['DD-MM-YYYY'] < sel_date)]
                        elif (after != None) & (before == None):
                            aft_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] > sel_date) & (oos_ses_data['DD-MM-YYYY'] < aft_date)]
                            bfr_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] < sel_date)]
                        else:
                            aft_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] > sel_date) & (oos_ses_data['DD-MM-YYYY'] < aft_date)]
                            bfr_weeks_data = oos_ses_data[(oos_ses_data['DD-MM-YYYY'] > bfr_date) & (oos_ses_data['DD-MM-YYYY'] < sel_date)]
                            
                        #filter weeks that doesn't have promotions, offers, oos < 7
                        app_log.info("remove weeks which has external factors like promotions, offers, oos<7")
                        aft_weeks_data = aft_weeks_data[(aft_weeks_data['ONETIMEBUY'] == 0) & (aft_weeks_data['PROMOTION'] == 0) & (aft_weeks_data['OFFER'] == 0) & (aft_weeks_data['OOS%'] < oos_limit)]
                        bfr_weeks_data = bfr_weeks_data[(bfr_weeks_data['ONETIMEBUY'] == 0) & (bfr_weeks_data['PROMOTION'] == 0) & (bfr_weeks_data['OFFER'] == 0) & (bfr_weeks_data['OOS%'] < oos_limit)]
                        frm = pd.to_datetime(frm, dayfirst = True)
                        to = pd.to_datetime(to, dayfirst = True)
                        
                        #filter weeks that comes between the dates selected in the price input tab
                        app_log.info("filter weeks that comes between the dates selected in the price input tab")
                        aft_weeks_data = aft_weeks_data[(aft_weeks_data['DD-MM-YYYY'] >= frm) & (aft_weeks_data['DD-MM-YYYY'] <= to)]
                        bfr_weeks_data = bfr_weeks_data[(bfr_weeks_data['DD-MM-YYYY'] >= frm) & (bfr_weeks_data['DD-MM-YYYY'] <= to)]
                        weeks_to_consider = min(len(bfr_weeks_data),len(aft_weeks_data))
                        app_log.info("check atleast one week is there to comapare")
                        if weeks_to_consider > 0:
                            aft_weeks_data.sort_values(by = 'DD-MM-YYYY', ascending = True, inplace = True)
                            bfr_weeks_data.sort_values(by = 'DD-MM-YYYY', ascending = True, inplace = True)
                            
                            #scale down the weeks if more than 6
                            app_log.info("scale down to six weeks if weeks exceeds more than 6")
                            if weeks_to_consider <= 6:
                                aft_weeks_data = aft_weeks_data.head(weeks_to_consider)
                                bfr_weeks_data = bfr_weeks_data.tail(weeks_to_consider)
                            else:
                                aft_weeks_data = aft_weeks_data.head(6)
                                bfr_weeks_data = bfr_weeks_data.tail(6)
                                
                            #get 3 month boundary date from the price change date for beyond 3 months flag
                            app_log.info("get 3 month boundary date from the price change date for beyond 3 months flag")
                            d = datetime.datetime.strptime(str(date)[:10], "%Y-%m-%d")
                            d2 = d - dateutil.relativedelta.relativedelta(months=3)
                            d3 = d + dateutil.relativedelta.relativedelta(months=3)
                            minDate = pd.to_datetime(min(bfr_weeks_data['DD-MM-YYYY']), dayfirst = True)
                            maxDate = pd.to_datetime(max(aft_weeks_data['DD-MM-YYYY']), dayfirst = True)
                            d2 = pd.to_datetime(d2, dayfirst = True)
                            d3 = pd.to_datetime(d3, dayfirst = True)
                            flag = 'N'
                            
                            #beyond 3 months before period
                            app_log.info("check for beyond 3 months in before period")
                            if minDate < d2:
                                flag = 'Y'
                            aft_flag = 'N'
                            
                            #beyond 3 months after period
                            app_log.info("check for beyond 3 months in after period")
                            if maxDate > d3:
                                aft_flag = 'Y'
                            l_price = '<NA>'
                            if last_price != '':
                                l_price = str(round(last_price,2))
                                
                            #compute gross margin rate
                            gmr_b = "0 %"
                            if bfr_weeks_data['NET SALES'].sum() > 0:
                                gmr_b = str(int(float(round(((bfr_weeks_data['GM'].sum())/(bfr_weeks_data['NET SALES'].sum())*100),2))))+" %"
                            gmr_a = "0 %"
                            if aft_weeks_data['NET SALES'].sum() > 0:
                                gmr_a = str(int(float(round(((aft_weeks_data['GM'].sum())/(aft_weeks_data['NET SALES'].sum())*100),2))))+" %"
                            bfw,afw = "",""
                            for i,j in zip(aft_weeks_data['WEEK'],bfr_weeks_data['WEEK']):
                                bfw = bfw +str(j)+","
                                afw = afw +str(i)+","
                                
                            #append skus with comparable periods to res_df dataframe
                            res_df.loc[len(res_df)] = [str(vendor),int(sku),str(round(price,2)),l_price,pd.to_datetime(date).strftime('%m/%d/%Y'),bfw.rstrip(','),afw.rstrip(','),flag,aft_flag,"$ "+str(int(float(round(bfr_weeks_data['NET SALES'].sum(),2)))),"$ "+str(int(float(round(aft_weeks_data['NET SALES'].sum(),2)))),"$ "+str(int(float(round(bfr_weeks_data['GM'].sum(),2)))),"$ "+str(int(float(round(aft_weeks_data['GM'].sum(),2)))),bfr_weeks_data['NET SALES QTY'].sum(),aft_weeks_data['NET SALES QTY'].sum(),gmr_b,gmr_a,str(int(float(round((bfr_weeks_data['OOS%'].mean()),2))))+" %",str(int(float(round((aft_weeks_data['OOS%'].mean()),2))))+" %"]
                        else:
                            #append skus with no comparable periods to no_com_df dataframe
                            no_com_df.loc[len(no_com_df)] = [int(sku),str(round(price,2)),pd.to_datetime(date).strftime('%m/%d/%Y')]
                               
                    #print skus with comparale periods 
                    app_log.info("display skus with comparable periods")
                    st.write("These are the comparable periods for the following SKUs:")
                    st.write(res_df)
                    csv = convert_df(res_df)
                    
                    #download_button to download generated report
                    app_log.info("download button to download generated report in price change report tab")
                    st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='large_df.csv',
                    mime='text/csv',
                    )
                    
                    #print skus with no comparable periods
                    app_log.info("display skus with no comparable periods")
                    st.write("These are no comparable periods found for the following SKUs:")
                    st.write(no_com_df)
                    
            #kpi tab for graphical insights
            with kpi_tab:
                app_log.info("kpi tab")
                #only on clicking submit in input_tab then save the files locally
                if click :
                    res_df.to_csv('report_data.csv')
                    no_com_df.to_csv('add_info.csv')
                    
                #get file path and check file exist or not
                file = os.path.isfile("report_data.csv")
                if (file) | (click):  
                    kpi_df = pd.read_csv('report_data.csv')
                    
                    #check atleast one sku with comparable is available for visualization 
                    app_log.info("check atleast one sku with comparable is available for visualization")
                    if len(kpi_df) > 1:
                        kpi_df['Collection'] = ''
                        kpi_df['Department'] = ''
                        data = data_with_header.dropna(axis = 0, subset = ['Sku'])
                        data['Sku'] = data['Sku'].astype('int')
                        kpi_df.drop(labels = [0], axis = 0, inplace = True)
                        kpi_df.rename(columns = {'Unnamed: 1':'Vendor','Unnamed: 2':'SKU','Unnamed: 3':'PRICE','Unnamed: 5':'PC DATE','Unnamed: 4':'LAST PRICE'}, inplace = True)
                        
                        #formatting the data as required
                        kpi_df['SKU'] = kpi_df['SKU'].astype('float')
                        kpi_df['SKU'] = kpi_df['SKU'].astype('int')
                        kpi_df['NET SALES'] = kpi_df['NET SALES'].str.replace('$','')
                        kpi_df['NET SALES.1'] = kpi_df['NET SALES.1'].str.replace('$','')
                        kpi_df['GROSS PROFIT'] = kpi_df['GROSS PROFIT'].str.replace('$','')
                        kpi_df['GROSS PROFIT.1'] = kpi_df['GROSS PROFIT.1'].str.replace('$','')
                        kpi_df['OOS'] = kpi_df['OOS'].str.replace('%','')
                        kpi_df['OOS.1'] = kpi_df['OOS.1'].str.replace('%','')
                        kpi_df['GROSS MARGIN RATE'] = kpi_df['GROSS MARGIN RATE'].str.replace('%','')
                        kpi_df['GROSS MARGIN RATE.1'] = kpi_df['GROSS MARGIN RATE.1'].str.replace('%','')
                        kpi_df['NET SALES'] = kpi_df['NET SALES'].astype('float')
                        kpi_df['NET SALES.1'] = kpi_df['NET SALES.1'].astype('float')
                        kpi_df['GROSS PROFIT'] = kpi_df['GROSS PROFIT'].astype('float')
                        kpi_df['GROSS PROFIT.1'] = kpi_df['GROSS PROFIT.1'].astype('float')
                        kpi_df['UNITS'] = kpi_df['UNITS'].astype('float')
                        kpi_df['UNITS.1'] = kpi_df['UNITS.1'].astype('float')
                        kpi_df['OOS'] = kpi_df['OOS'].astype('float')
                        kpi_df['OOS'] = kpi_df['OOS'].apply(lambda x : np.round(x,2))
                        kpi_df['OOS.1'] = kpi_df['OOS.1'].astype('float')
                        kpi_df['OOS.1'] = kpi_df['OOS.1'].apply(lambda x : np.round(x,2))
                        kpi_df['GROSS MARGIN RATE'] = kpi_df['GROSS MARGIN RATE'].astype('float')
                        kpi_df['GROSS MARGIN RATE'] = kpi_df['GROSS MARGIN RATE'].apply(lambda x : np.round(x,2))
                        kpi_df['GROSS MARGIN RATE.1'] = kpi_df['GROSS MARGIN RATE.1'].astype('float')
                        kpi_df['GROSS MARGIN RATE.1'] = kpi_df['GROSS MARGIN RATE.1'].apply(lambda x : np.round(x,2))
                        kpi_df['PRICE'] = kpi_df['PRICE'].astype('float')
                        kpi_df['PRICE'] = kpi_df['PRICE'].apply(lambda x : np.round(x,2))
                        
                        #add department and collection columns
                        for i,j in zip(kpi_df['SKU'],range(0,len(kpi_df['SKU']))):
                            kpi_df.iloc[j, 21] = data[data['Sku'] == i]['Department'].iloc[0]
                            kpi_df.iloc[j, 20] = data[data['Sku'] == i]['Collection'].iloc[0]

                        department,collection,sku_kpi,price_date = st.columns(4)
                        kpi_unique_depts = list(kpi_df['Department'].unique())
                        
                        #department filter
                        with department:
                            app_log.info("department filter in kpi tab")
                            st.markdown('<p style="margin-top: 10px;margin-bottom: 110px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the Department :</p>', unsafe_allow_html=True)
                            kpi_dept_menu = st.selectbox('', kpi_unique_depts, key = 'kpi_dept')
                
                        kpi_unique_colls = list(kpi_df[kpi_df['Department'] == st.session_state.kpi_dept]['Collection'].unique())
      
                        #collection filter
                        with collection:
                            app_log.info("collection filter in kpi tab")
                            st.markdown('<p style="margin-top: 10px;margin-bottom: 110px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the Collection :</p>', unsafe_allow_html=True)
                            kpi_coll_menu = st.selectbox('', kpi_unique_colls, key = 'kpi_coll')

                        kpi_unique_skus = list(kpi_df[(kpi_df['Department'] == st.session_state.kpi_dept) & (kpi_df['Collection'] == st.session_state.kpi_coll)]['SKU'].unique())
        
                        kpi_unique_skus = [int(i) for i in kpi_unique_skus]
                        
                        #sku filter
                        with sku_kpi:
                            app_log.info("sku filter in kpi tab")
                            st.markdown('<p style="margin-top: 10px;margin-bottom: 110px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the SKU :</p>', unsafe_allow_html=True)
                            kpi_sku_menu = st.selectbox(options = kpi_unique_skus, label = "", key = 'kpi_sku')
                
                        kpi_sel = kpi_df[(kpi_df['Department'] == st.session_state.kpi_dept) & (kpi_df['Collection'] == st.session_state.kpi_coll) & (kpi_df['SKU'] == st.session_state.kpi_sku)]
                        kpi_unique_prices = [str(r['PRICE'])+'-'+str(r['PC DATE']) for i,r in kpi_sel.iterrows()]     
            
                        #price & date filter
                        with price_date:
                            app_log.info("price & date filter in kpi tab")
                            st.markdown('<p style="margin-top: 10px;margin-bottom: 110px;padding-bottom: 0px;color:#184a7d; font-size: 20px;">Select the Price - Date :</p>', unsafe_allow_html=True)
                            kpi_price_menu = st.selectbox(options = kpi_unique_prices, label = '', key = 'kpi_price')
                
                        price, date = st.session_state.kpi_price.split('-')
                        date = pd.to_datetime(date,dayfirst = True)
                        kpi_sel['PC DATE'] = pd.to_datetime(kpi_sel['PC DATE'], dayfirst = True)
            
                        row = kpi_sel[(kpi_sel['PRICE'] == float(price)) & (kpi_sel['PC DATE'] == date)]
                        st.info("Weeks Considered Before Price Change are : "+row['WEEKS'].iloc[0]+" -----  "+"  Price Change Date : "+date.strftime('%d/%m/%Y')+"  ----- "+"Weeks Considered After Price Change are : "+row['WEEKS.1'].iloc[0])
                        #st.write("")
                        net_sales,units,gross_profit = st.columns(3)
                        gross_margin_rate,oos,g6 = st.columns(3)
                        
                        #Net sales bar graph
                        with net_sales:
                            app_log.info("net sales bar graph")
                            st.write(" ")
                            original_title = '<center><p style="font-family:bold; color:#184a7d; font-size: 20px;background-color:#ebfcfc;border: 1px solid #bae8f5;border-radius:5px;;">NET SALES</p></center>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            st.write(" ")
                            df = pd.DataFrame({"NET SALES": ["Before", "After"],"values":[float(row['NET SALES']),float(row['NET SALES.1'])]})
                            bars = alt.Chart(df).mark_bar().encode(y='values',x='NET SALES',color='NET SALES').properties(width=380,height=430)
                            text = bars.mark_text(align='center', dx=0, dy=-8, fontSize=15, fontWeight='bold', opacity = 1).encode(text = 'values:Q')
                            cha = alt.layer(bars, text).configure_axis(grid=False)
                            cha
                        
                        #Units bar graph
                        with units:
                            app_log.info("units bar graph")
                            st.write(" ")
                            original_title = '<center><p style="font-family:bold; color:#184a7d; font-size: 20px;background-color:#ebfcfc;border: 1px solid #bae8f5;border-radius:5px;;">UNITS</p></center>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            st.write(" ")
                            df = pd.DataFrame({"UNITS": ["Before", "After"],"values":[int(float(row['UNITS'])),int(float(row['UNITS.1']))]})
                            bars = alt.Chart(df).mark_bar().encode(y='values',x='UNITS',color='UNITS').properties(width=380,height=430)
                            text = bars.mark_text(align='center', dx=0, dy=-8, fontSize=15, fontWeight='bold', opacity= 1).encode(text = 'values:Q')
                            cha = alt.layer(bars, text).configure_axis(grid=False)
                            cha
                            
                        #Gross profit bar graph
                        with gross_profit:
                            app_log.info("gross profit bar graph")
                            st.write(" ")
                            original_title = '<center><p style="font-family:bold; color:#184a7d; font-size: 20px;background-color:#ebfcfc;border: 1px solid #bae8f5;border-radius:5px;;">GROSS PROFIT</p></center>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            st.write(" ")
                            df = pd.DataFrame({"GROSS PROFIT": ["Before", "After"],"values":[float(row['GROSS PROFIT']),float(row['GROSS PROFIT.1'])]})
                            bars = alt.Chart(df).mark_bar().encode(y='values',x='GROSS PROFIT',color='GROSS PROFIT').properties(width=380,height=430)
                            text = bars.mark_text(align='center', dx=0, dy=-8, fontSize=15, fontWeight='bold', opacity=1).encode(text = 'values:Q')
                            cha = alt.layer(bars, text).configure_axis(grid=False)
                            cha
                            
                        #Gross margin rate bar graph
                        with gross_margin_rate:
                            app_log.info("gross margin rate bar graph")
                            st.write(" ")
                            original_title = '<center><p style="font-family:bold; color:#184a7d; font-size: 20px;background-color:#ebfcfc;border: 1px solid #bae8f5;border-radius:5px;;">GROSS MARGIN RATE</p></center>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            st.write(" ")
                            df = pd.DataFrame({"GROSS MARGIN RATE": ["Before", "After"],"values":[float(row['GROSS MARGIN RATE']),float(row['GROSS MARGIN RATE.1'])]})
                            bars = alt.Chart(df).mark_bar().encode(x='GROSS MARGIN RATE',y='values',color='GROSS MARGIN RATE').properties(width=380,height=430)
                            text = bars.mark_text(align='center', dx=0, dy=-8, fontSize=15, fontWeight='bold', opacity=1).encode(text = 'values:Q')
                            cha = alt.layer(bars, text).configure_axis(grid=False)
                            cha
                            
                        #OOS bar graph
                        with oos:
                            app_log.info("oos bar graph")
                            st.write(" ")
                            original_title = '<center><p style="font-family:bold; color:#184a7d; font-size: 20px;background-color:#ebfcfc;border: 1px solid #bae8f5;border-radius:5px;;">OOS</p></center>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            st.write(" ")
                            df = pd.DataFrame({"OOS": ["Before", "After"], "values": [float(row['OOS']),float(row['OOS.1'])]})
                            bars = alt.Chart(df).mark_bar().encode(y='values',x='OOS',color='OOS').properties(width=380,height=430)
                            text = bars.mark_text(align='center', dx=0, dy=-8, fontSize=15, fontWeight='bold', opacity=1).encode(text = 'values:Q')
                            cha = alt.layer(bars, text).configure_axis(grid=False)
                            cha
                    else:
                        st.info("Didn't find SKU's with comparable period")
                else:
                    st.info("No data found")
                    with price_change_report_tab:
                        st.info("No data found")
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    app_log.error(e)
    st.warning(e)
    st.warning(exc_tb.tb_lineno)