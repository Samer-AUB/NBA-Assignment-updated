import streamlit as st
import pandas as pd
import plotly.express as px

import pandas as pd

# Use Pandas to read the CSV file into a DataFrame
df = pd.read_csv("Games.csv")

# Print the first 5 rows of the DataFrame
df.head()


# In[2]:


# Title for your Streamlit app
st.title('Top Winning and Most Losing Teams - for Home Team Statistics')

# Create a slider to select the years (assuming SEASON is the year)
year_range = st.slider("Select a Year", min_value=df['SEASON'].min(), max_value=df['SEASON'].max(), value=df['SEASON'].max())

# Create a dropdown to select between Winning and Losing Teams
selected_option = st.selectbox("Select Teams", ["Top Winning Teams", "Most Losing Teams"])

# Filter the DataFrame based on the selected year
df = df[df['SEASON'] == year_range]

# Filter the DataFrame based on the selected option
if selected_option == "Top Winning Teams":
    top_teams = df[df['HOME_TEAM_WINS'] == 1].groupby('Home Team').size().nlargest(5).index
else:
    top_teams = df[df['HOME_TEAM_WINS'] == 0].groupby('Home Team').size().nlargest(5).index

filtered_df = df[df['Home Team'].isin(top_teams)]

# Select specific columns for visualization
selected_columns = ['Free Throw Percentage_home',
                    '3 Point Field Goal Percentage_home',
                    "Percent of Team's Assists_home",
                    'Rebounds_home']

# Reshape the DataFrame for the stacked bar chart
melted_df = filtered_df.melt(id_vars=['Home Team'], value_vars=selected_columns)

# Create a horizontal stacked bar chart using Plotly Express
fig = px.bar(melted_df, 
             x='Home Team', 
             y='value',
             color='variable',
             title=f'{selected_option} - Home Team Statistics for {year_range}',
             labels={'value': 'Percentage', 'variable': 'Statistic'},
             color_discrete_map={'Free Throw Percentage_home': 'sky blue',
                                 '3 Point Field Goal Percentage_home': 'green',
                                 "Percent of Team's Assists_home": 'red',
                                 'Rebounds_home': 'grey'},
             height=400)

# Update the layout for better visualization
fig.update_layout(barmode='stack', xaxis_title='Team', yaxis_title='Percentage')

# Display the plot in Streamlit
st.plotly_chart(fig)



# In[12]:


# Title for your Streamlit app
st.title('Performance Metrics')

import streamlit as st
import pandas as pd
import plotly.express as px

# Load your DataFrame
df = pd.read_csv("Games.csv")

# Title for your Streamlit app
st.title('Number of Wins and Losses for Selected Teams')

# List of teams you want to analyze
selected_teams = ['Cleveland', 'Philadelphia', 'Warriors', 'Boston', 'Bulls']

# Check if there is only one unique year in the dataset
unique_years = df['SEASON'].unique()
if len(unique_years) == 1:
    st.error("There is only one unique year in the dataset. Please upload a dataset with multiple years.")
else:
    # Create a slider to select the years (assuming SEASON is the year)
    year_range = st.slider("Select a Year", min_value=df['SEASON'].min(), max_value=df['SEASON'].max())

    # Filter the DataFrame for selected teams and wins
    filtered_df = df[(df['Home Team'].isin(selected_teams)) & (df['HOME_TEAM_WINS'] == 1) & (df['SEASON'] == year_range)]

    # Create a vertical bar chart using Plotly Express for wins
    fig = px.bar(filtered_df, 
                 x='Home Team', 
                 color='Home Team',
                 title=f'Number of Wins for Selected Teams in {year_range}',
                 color_discrete_map={team: 'blue' for team in selected_teams},
                 height=400)

    # Update the layout for better visualization
    fig.update_layout(xaxis_title='Team', yaxis_title='Number of Wins')

    # Display the plot for wins in Streamlit
    st.plotly_chart(fig)

    # Filter the DataFrame for selected teams and losses
    filtered_df_losses = df[(df['Home Team'].isin(selected_teams)) & (df['HOME_TEAM_WINS'] == 0) & (df['SEASON'] == year_range)]

    # Create a vertical bar chart for losses using Plotly Express
    fig_losses = px.bar(filtered_df_losses, 
                         x='Home Team', 
                         color='Home Team',
                         title=f'Number of Losses for Selected Teams in {year_range}',
                         color_discrete_map={team: 'grey' for team in selected_teams},
                         height=400)

    # Update the layout for better visualization
    fig_losses.update_layout(xaxis_title='Team', yaxis_title='Number of Losses')

    # Display the plot for losses in Streamlit
    st.plotly_chart(fig_losses)


# In[10]:


# Annual Metrics for Teams

import streamlit as st
import pandas as pd
import plotly.express as px

# Load your DataFrame
df = pd.read_csv("Games.csv")

# Title for your Streamlit app
st.title('Annual Average Metrics for Selected Teams')

# Create a dropdown to select one or multiple team names
selected_teams = st.multiselect("Select Team(s)", df['Home Team'].unique())

# Calculate the annual average for the specified metrics
annual_avg_df = df.groupby(['SEASON', 'Home Team'])[['Free Throw Percentage_home',
                                                     '3 Point Field Goal Percentage_home',
                                                     "Percent of Team's Assists_home",
                                                     'Rebounds_home']].mean().reset_index()

# Filter the DataFrame based on selected teams and the year range (2017-2022)
filtered_df = annual_avg_df[(annual_avg_df['Home Team'].isin(selected_teams)) & (annual_avg_df['SEASON'].between(2017, 2022))]

# Create separate bar charts for each metric
metrics = ['Free Throw Percentage_home',
           '3 Point Field Goal Percentage_home',
           "Percent of Team's Assists_home",
           'Rebounds_home']

for metric in metrics:
    fig = px.bar(
        filtered_df,
        x='SEASON',
        y=metric,
        color='Home Team',
        title=f'Annual Average {metric} by Team',
        labels={'SEASON': 'Year'},
        category_orders={'SEASON': list(range(2017, 2023))}
    )
    st.plotly_chart(fig)


# In[13]:


import streamlit as st
import pandas as pd
import plotly.express as px

# Load your DataFrame
df = pd.read_csv("Games.csv")

# Title for your Streamlit app
st.title('Annual Average Metrics for Selected Teams')

# Calculate the annual average for the specified metrics
annual_avg_df = df.groupby(['SEASON', 'Home Team'])[['Free Throw Percentage_home',
                                                     '3 Point Field Goal Percentage_home',
                                                     "Percent of Team's Assists_home",
                                                     'Rebounds_home']].mean().reset_index()

# Select the specific teams for box plots (Warriors, Lakers, and Spurs)
selected_teams = ['Warriors', 'Lakers', 'Spurs']

# Filter the DataFrame for the selected teams
filtered_df = annual_avg_df[annual_avg_df['Home Team'].isin(selected_teams)]

# Create separate box plots for each metric
metrics = ['Free Throw Percentage_home',
           '3 Point Field Goal Percentage_home',
           "Percent of Team's Assists_home",
           'Rebounds_home']

for metric in metrics:
    fig = px.box(
        filtered_df,
        x='Home Team',
        y=metric,
        title=f'Box Plot for {metric} by Selected Teams',
        labels={'Home Team': 'Team'},
    )
    st.plotly_chart(fig)


# In[ ]:




