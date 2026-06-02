import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns 
import matplotlib.pyplot as plt 
import streamlit  as st 
database_url ="postgresql://readonly_student.tyxjmbptftftcqgozyfc:StudentRead123!@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
engine =create_engine(database_url)
query ="""
select 
*from track
"""

df =pd.read_sql(query, engine)
f_df =(
    df.groupby("genre_id")[["track_id", "name", "composer"]].count().sort_values("genre_id", ascending =False)
    )
# print(f_df)
st.dataframe(f_df)


