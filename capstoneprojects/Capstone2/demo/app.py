import gradio as gr
import numpy as np
import pandas as pd
import joblib

# Load Model
bestRF = joblib.load('Daegu_Apartment_RF_GridSearchCV.joblib')

# Prediction Function
def predict_price(time_to_subway, facilities_etc, facilities_public,
                  school_university, parking_basement, facilities_in_apt,
                  size_sqf, age, hallway_type, subway_station):
    
    #One-hot encoder
    hallway = ['corridor', 'mixed', 'terraced']
    hallway_encoder = {f'HallwayType_{s}': 1.0 if hallway_type == s else 0.0
                       for s in hallway}
    station = ['Bangoge', 'Banwoldang', 'Chil-sung-market', 'Daegu', 'Kyungbuk_uni_hospital', 'Myung-duk', 'Sin-nam', 'no_subway_nearby']
    station_encoder = {f'SubwayStation_{s}': 1.0 if subway_station == s else 0.0
                       for s in station}
    
    #Variable DataFrame
    inputDF = pd.DataFrame({
        'TimeToSubway': [time_to_subway],
        'N_FacilitiesNearBy(ETC)' : [facilities_etc],
        'N_FacilitiesNearBy(PublicOffice)': [facilities_public],
        'N_SchoolNearBy(University)' : [school_university],
        'N_Parkinglot(Basement)' : [parking_basement],
        'N_FacilitiesInApt' : [facilities_in_apt],
        'Size(sqf)' : [size_sqf],
        'age': [age],
        **{s: [value] for s, value in hallway_encoder.items()}, 
        **{s: [value] for s, value in station_encoder.items()},
    })

    #Predict
    preds = bestRF.predict(inputDF)
    preds_price = np.expm1(preds)[0]

    return f'Housingprice: {preds_price:.2f}'

#Tampilannya & input
with gr.Blocks(title= 'Daegu Apartment Price Predictor') as demo:
    gr.Markdown('Predict Daegu Apartment prices using Random Forest model')

    with gr.Row():
        with gr.Column():
            gr.Markdown('Property"s Detail')

            time_to_subway = gr.Dropdown(label='Time To Subway (in min)',
                                         choices=[('0-5min', 0),
                                                  ('10-15min', 1),
                                                  ('15-20min', 2),
                                                  ('5-10min', 3),
                                                  ('no_bus_stop_nearby', 4)], value=0)
            facilities_etc = gr.Number(label='No. of Facilities Nearby (ETC)')
            facilities_public = gr.Number(label='No. of Facilities Nearby (Public Office)')
            school_university = gr.Number(label='No. of Universities Nearby')
            parking_basement = gr.Number(label='No. of parking basements')
            facilities_in_apt = gr.Number(label='No. of Facilities in Apartment')
            size_sqf = gr.Number(label='Apartment size (in sqf)')
            age = gr.Number(label='How old is the apartment (in years)')
            
            hallway_type = gr.Dropdown(label='Types of Hallway',
                choices=['corridor', 'mixed', 'terraced'],
                value='mixed')

            subway_station = gr.Dropdown(
                label='Nearest Subway Stations',
                choices=['Bangoge', 'Banwoldang', 'Chil-sung-market', 'Daegu',
                    'Kyungbuk_uni_hospital', 'Myung-duk', 'Sin-nam', 'no_subway_nearby'],
                value='Daegu')

            predict_button = gr.Button('Predict the Price', variant='primary')
            output = gr.Textbox(label='Predicted Apartment Price', interactive=False)

            predict_button.click(fn=predict_price,
                inputs=[time_to_subway, facilities_etc, facilities_public,
                    school_university, parking_basement, facilities_in_apt,
                    size_sqf, age, hallway_type, subway_station],
                outputs=output)
demo.launch()
