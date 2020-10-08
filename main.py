import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px

pd.set_option('display.max_columns', None)
data = pd.read_csv('Border_Crossing_Entry_Data.csv')
data = data.drop("Port Code", axis=1)
data = data.rename(columns={"Port Name": "state", "State": "code", "Border": "border", "Date": "date", "Value": "count",
                            "Measure": "measure"})
data['date'] = pd.to_datetime(data['date']).dt.normalize()
data = data.replace({"Train Passengers": "Train", "Rail Containers Full": "Train", "Rail Containers Empty": "Train",
                     "Trians": "Train", "Bus Passengers": "Bus", "Buses": "Bus", "Trucks": "Truck",
                     "Truck Containers Full": "Truck", "Truck Containers Empty": "Truck",
                     "Personal Vehicles": "personal_vehicles", "Personal Vehicles Passengers": "personal_vehicles"})
print(data.head(20))

gbb = data.groupby("border")[["count"]].sum().reset_index()
fig = px.pie(gbb, values="count", names="border", template="seaborn")
fig.show()

gbb = data.groupby("measure")[["count"]].sum().reset_index()
fig = px.pie(gbb, values="count", names="measure", template="seaborn")
fig.show()

fig = px.sunburst(data, path=['border', 'code', 'measure'], values='count', color='code', hover_data=['measure'])
fig.show()
map_data = data.loc[:, ["date", "code", "count"]]
map_data1 = data.loc[:, ["code", "count"]]
map_data = map_data.groupby(["date", "code"])[["count"]].sum().reset_index()
map_data1 = map_data1.groupby(["code"])[["count"]].sum().reset_index()
fig = px.choropleth(map_data1, locations=map_data1["code"], color=map_data1["count"],
                    locationmode="USA-states",
                    scope="usa",
                    color_continuous_scale='Blues',

                    )
fig.show()
