import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import plotly.express as px
st.set_page_config(
    page_title="Crimes in US Communities Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Анализ датасета Crimes in US Communities")
df = pd.read_csv('/Users/olegafanasev/PycharmProjects/streamlitproj/crimedata.csv')
st.header("Средний процент преступлений по расам для всех поселений выбранного штата")
state_filter = st.selectbox("Выберите штат", pd.unique(df["state"]))
df_with_state_filter = df[df["state"] == state_filter]
chart_data = pd.DataFrame(
    [df_with_state_filter["racepctblack"].mean(), df_with_state_filter["racePctWhite"].mean(),
     df_with_state_filter["racePctAsian"].mean(), df_with_state_filter["racePctHisp"].mean()],
    ['black', 'white', 'asian', 'hispanic'])
st.bar_chart(chart_data)
st.header("Зависимость между выбранным видом преступления и средним доходом")
type_of_crime = st.selectbox("Выберите тип преступления: ",
                             ['murders', 'arsons', 'autoTheft', 'larcenies', 'burglaries', 'assaults', 'rapes',
                              'robberies'])
if type_of_crime == 'murders':
    x = df["murdPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
elif type_of_crime == 'arsons':
    x = df["arsonsPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
elif type_of_crime == 'autoTheft':
    x = df["autoTheftPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
elif type_of_crime == 'larcenies':
    x = df["larcPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
elif type_of_crime == 'burglaries':
    x = df["burglPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
elif type_of_crime == 'assaults':
    x = df["assaultPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
elif type_of_crime == 'rapes':
    x = df["rapesPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
else:
    x = df["robbbPerPop"]
    y = df["medIncome"]
    p = figure()
    p.circle(x, y)
    st.bokeh_chart(p, use_container_width=True)
st.header("Вывод координат тех штатов, где есть поселения численностью больше введенного значения со штатом полицейских машин")
df2 = pd.read_csv(
    '/Users/olegafanasev/PycharmProjects/streamlitproj/world_country_and_usa_states_latitude_and_longitude_values.csv')
new_df = df2[['usa_state_code', 'usa_state_latitude', 'usa_state_longitude']].copy()
new_df = new_df.dropna()
state_to_its_coords = dict()
for index, row in new_df.iterrows():
    state_to_its_coords[row['usa_state_code']] = [row['usa_state_latitude'], row['usa_state_longitude']]
number = st.text_input("Введите численность", "1000000")
if st.button('Submit'):
    if number.isdigit():
        st.success("Correct input!")
    else:
        st.error("Wrong input!")
df_with_population_filter = df[df["population"] >= int(number)]
arr_for_mapping = []
for index, row in df_with_population_filter.iterrows():
    if row['PolicCars'] > 0:
        arr_for_mapping.append(state_to_its_coords[row['state']])
df_for_mapping = pd.DataFrame(arr_for_mapping, columns=['lat', 'lon'])
st.map(df_for_mapping)
dict_for_dublicates = dict()
for index, row in df.iterrows():
    if row['communityName'] not in dict_for_dublicates:
        dict_for_dublicates[row['communityName']] = 1
    else:
        dict_for_dublicates[row['communityName']] += 1
array_for_dublicates = []
for key, value in dict_for_dublicates.items():
    if value > 1:
        array_for_dublicates.append(key)
st.header("Сравнительная таблица выбранных городов-дубликатов по названию")
community_filter = st.radio("Выберите поселение", array_for_dublicates)
df_dublicate = df[df["communityName"] == community_filter]
st.table(df_dublicate)
st.header("Ещё один график и селектор")
if st.button("Нажми если хочешь это увидеть"):
    st.subheader("Зависимость между размерами домохозяйства и арендной платой")
    fig = px.density_heatmap(
        data_frame=df, y="householdsize", x="RentMedian"
    )
    st.write(fig)