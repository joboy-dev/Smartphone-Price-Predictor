import streamlit as st
import pickle
import numpy as np
import sklearn

with open('smartphone.pickle', mode='rb') as model_file:
    model = pickle.load(model_file)
    

def predict_price(ram, rom, battery, processor_name, processor_core, processor_speed, screen_size, screen_res_x, screen_res_y, os_type, os_version, front_camera, rear_camera, sim_type):
    '''Function to predict price of smartphone'''
    
    processor_name_mapping = {
        'None': [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
        'A13': [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0], 
        'Apple': [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0], 
        'Bionic': [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0], 
        'Dimensity': [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0], 
        'Exynos': [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        'Helio': [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0], 
        'Kirin': [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0], 
        'Qualcomm': [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0], 
        'SC9863A': [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0], 
        'Snapdragon': [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0], 
        'Spreadtrum': [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], 
        'Tensor': [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0], 
        'Tiger': [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], 
        'Unisoc': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    }
    
    processor_core_mapping = {
        'None': [1,0,0,0,0], 
        'Dual Core': [0,1,0,0,0], 
        'Hexa Core': [0,0,1,0,0], 
        'Octa Core': [0,0,0,1,0], 
        'Quad Core': [0,0,0,0,1],
    }
    
    os_type_mapping = {
        'Android': [1,0], 
        'iOS': [0,1],
    }
    
    sim_type_mapping = {
        'Dual Sim': [1,0], 
        'Single Sim': [0,1],
    }
    
    processor_name_encoded = processor_name_mapping.get(processor_name)
    processor_core_encoded = processor_core_mapping.get(processor_core)
    os_type_encoded = os_type_mapping.get(os_type)
    sim_type_encoded = sim_type_mapping.get(sim_type)
    
    X_test = np.array([[ram, rom, battery, processor_speed, screen_size, screen_res_x, screen_res_y, os_version, front_camera, rear_camera] + processor_name_encoded + processor_core_encoded + os_type_encoded + sim_type_encoded])
    
    y_pred = model.predict(X_test)
    return y_pred
    

st.title('Smartphone Price Predictor')
st.write('An ML application to predict the price of a smartphone based on the specifications of the device.')

st.header('Fill in the form below')
st.write('Enter the specifications of the phone')

# Form input
ram = st.number_input(label='Enter RAM(GB)', min_value=1, max_value=64, value=1)

rom = st.number_input(label='Enter ROM(GB)', min_value=1, max_value=1024, value=1)

battery = st.number_input(label='Enter Battery Capacity(mAh)', min_value=1000, max_value=10000, value=1000)

processor_name = st.selectbox(label='Select Processor', options=['None', 'A13', 'Apple', 'Bionic', 'Dimensity', 'Exynos', 'Helio', 'Kirin', 'Qualcomm', 'SC9863A', 'Snapdragon', 'Spreadtrum', 'Tensor', 'Tiger', 'Unisoc'])

processor_core = st.selectbox(label='Select Processor Core', options=['None', 'Dual Core', 'Hexa Core', 'Octa Core', 'Quad Core'])

processor_speed = st.number_input(label='Enter Processor Speed(GHz)', min_value=0.1, max_value=10.0, value=1.0)

screen_size = st.number_input(label='Enter Screen Size(inches)', min_value=1.0, max_value=10.0, value=1.0)

screen_res_x = st.number_input(label='Enter Horizontal Screen Resolution(px)', min_value=100, max_value=3000, value=100)

screen_res_y = st.number_input(label='Enter Vertical Screen Resolution(px)', min_value=100, max_value=3000, value=100)

os_type = st.selectbox(label='Select Operating System', options=['Android', 'iOS'])

os_version = st.number_input(label='Enter OS Version', min_value=1, max_value=25, value=1)

front_camera = st.number_input(label='Enter Front Camera Sharpness(MP)', min_value=0.1, max_value=100.0, value=1.0)

rear_camera = st.number_input(label='Enter Rear Camera Sharpness(MP)', min_value=0.1, max_value=400.0, value=1.0)

sim_type = st.selectbox(label='Select Sim Type', options=['Dual Sim', 'Single Sim'])

if st.button(label='Predict Price'):
    price = predict_price(ram, rom, battery, processor_name, processor_core, processor_speed, screen_size, screen_res_x, screen_res_y, os_type, os_version, front_camera, rear_camera, sim_type)
    
    st.success(f'Price of the smartphone is ₦{price[0]:.2f}')
