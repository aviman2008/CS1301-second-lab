# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt
import csv
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---



st.title("2017 NFL Quarterback Statistics")

with open("data.json", "r") as file:
    data = json.load(file)




quarterbacks = data["data_points"]

#static graph

passing_yards = []
passer_ratings = []

for qb in quarterbacks:
    passing_yards.append(qb["Passing Yds"])
    passer_ratings.append(qb["Passer Rating"])

fig, ax = plt.subplots()

ax.scatter(passing_yards, passer_ratings)

for i in range(len(quarterbacks)):
    ax.annotate(
        quarterbacks[i]["label"],
        (passing_yards[i], passer_ratings[i]),
        xytext=(5,5),
        textcoords = "offset points",
        fontsize = 8
    )

ax.set_title("Passing Yards vs. Passer Rating")
ax.set_xlabel("Passing Yards")
ax.set_ylabel("Passer Rating")

st.pyplot(fig)

#adjustable graph

stats = [
    "Passing Yds",
    "Completion Percentage",
    "Passing Touchdowns",
    "Passer Rating",
    "Interceptions",
    "Rushing Yards"
]

if "selected_stat" not in st.session_state:
    st.session_state.selected_stat = "Passing Yds"

selected_stat = st.selectbox(
    "Choose a Statistic:",
    stats,
    key="selected_stat"
)




ranked_qbs = sorted(
    quarterbacks,
    key=lambda qb: qb[selected_stat],
    reverse = True
)


names = []
values = []

for qb in ranked_qbs:
    names.append(qb["label"])
    values.append(qb[selected_stat])


import pandas as pd

chart_data = pd.DataFrame({
    "Quarterback": names,
    selected_stat: values

})

st.bar_chart(
    chart_data,
    x="Quarterback",
    y=selected_stat,
    sort=False
)
    






# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

data = pd.read_csv("data.csv")
hours = data["hours"]
team = data["team"].unique()

st.header("Football Viewing Habits Distribution")

fig, ax = plt.subplots()

ax.hist(hours, bins=10, edgecolor="black")

ax.set_title("Distribution of Weekly Football Viewing")
ax.set_xlabel("Hours Watched per week")
ax.set_ylabel("Number of Respondents")

st.pyplot(fig)

selected_team = st.selectbox(
    "Select an NFL Team", 
    team,
    key="selected_nfl_team"
)

filtered_data = data[data["team"] == selected_team]
filtered_hours = filtered_data["hours"]
mean_hours = filtered_hours.mean()
median_hours = filtered_hours.median()


hour_ranges = pd.cut(
    filtered_hours,
    bins=[-1, 4, 9, 14, 19, float("inf")],
    labels=["0-4", "5-9", "10-14", "15-19", "20+"]
)

counts=hour_ranges.value_counts().sort_index()
fig2, ax2 = plt.subplots()
ax2.bar(counts.index.astype(str), counts.values)

ax2.set_title(f"Distribution of Weekly Football Viewing: {selected_team}")
ax2.set_xlabel("Hours Watched per week")
ax2.set_ylabel("Number of Respondents")

st.pyplot(fig2)

st.metric("Mean # of Hours Watched", round(mean_hours, 2))
st.metric("Median # of Hours Watched", round(median_hours, 2))

comparison = pd.DataFrame({
    "Team": [selected_team],
    "Median": [round(median_hours, 2)],
    "Mean": [round(mean_hours, 2)]
})




if os.path.exists('comparison.csv') and os.path.getsize('comparison.csv') > 0:
    existing_data = pd.read_csv("comparison.csv")
    existing_teams = existing_data["Team"].values
else:
    existing_teams = []
    

if selected_team not in existing_teams:
    comparison.to_csv(
        "comparison.csv",
        mode = "a",
        header=not os.path.exists("comparison.csv") or os.path.getsize("data.csv") == 0,
        index=False
    )

current_data_df = pd.read_csv("comparison.csv")
st.dataframe(current_data_df)


    


