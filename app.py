import io

import pandas as pd
import streamlit as st
from google.cloud.storage import client
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

ENGINEERED_FEATURES = [
    'DRIVE POWER', 'LOAD POWER', 'CHARGE MECH POWER', 'CHARGE HYD POWER',
    'SERVO MECH POWER', 'SERVO HYD POWER', 'SCAVENGE POWER',
    'MAIN COOLER POWER', 'GEARBOX COOLER POWER'
]
PRESSURE_TEMPERATURE = ['PT4', 'HSU IN', 'TT2', 'HSU OUT']
VIBRATIONS = ['Vibration 1', ' Vibration 2']
FORECAST_FEATURES = ENGINEERED_FEATURES + PRESSURE_TEMPERATURE + VIBRATIONS
FORECAST_FEATURES = [f.strip().replace(' ', '_') for f in FORECAST_FEATURES]

st.set_page_config(
    page_title='Test data profile',
    page_icon='https://github.com/ivanokhotnikov/test_rig/blob/master/images/fav.png?raw=True',
    layout='centered',
)


def main():
    st.title('Test data profile')
    is_minimal = st.checkbox('Minimal', False)
    storage_client = client.Client()
    bucket = storage_client.get_bucket('test_rig_processed_data')
    blob = bucket.get_blob('/processed_data.csv')
    data_bytes = blob.download_as_bytes()
    df = pd.read_csv(io.BytesIO(data_bytes))
    forecast_df = df[FORECAST_FEATURES].apply(pd.to_numeric,
                                              errors='coerce',
                                              downcast='float')
    profile = ProfileReport(forecast_df, minimal=is_minimal, dark_mode=True)
    st_profile_report(profile)


if __name__ == "__main__":
    main()
