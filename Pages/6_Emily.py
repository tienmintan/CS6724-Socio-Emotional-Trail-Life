import streamlit as st
import pandas as pd
import plotly.express as px

# Set the Streamlit page configuration
st.set_page_config(page_title="Hikers'python3 Emotions Visualization Dashboard", layout="wide")

# ------------------------------
# Data Loading & Preprocessing
# ------------------------------

# Define file paths (update these paths as needed)
file_path_top_10 = '/Users/emilyelkins/Documents/SPRING 2025/PYTHON/CS6724-Socio-Emotional-Trail-Life/emilyelkins/2025-03-25_Top10Pct.xlsx'
file_path_emotions = '/Users/emilyelkins/Documents/SPRING 2025/PYTHON/CS6724-Socio-Emotional-Trail-Life/emilyelkins/Emotions Visualization Chart.xlsx'
file_path_top_10_extraction = '/Users/emilyelkins/Documents/SPRING 2025/PYTHON/CS6724-Socio-Emotional-Trail-Life/emilyelkins/Top Ten Percent Data Extraction.xlsx'

# Load the Excel files
df_top_10 = pd.read_excel(file_path_top_10, sheet_name='Top_10pct_Miles_2021-23', engine='openpyxl')
df_emotions = pd.read_excel(file_path_emotions, engine='openpyxl')
df_top_10_extraction = pd.read_excel(file_path_top_10_extraction, engine='openpyxl')

# Process df_top_10
df_top_10['date'] = pd.to_datetime(
    df_top_10[['year', 'Month', 'DayNo']].astype(str).agg('-'.join, axis=1),
    errors='coerce'
)
df_top_10 = df_top_10[df_top_10['date'].notna()]
df_top_10 = df_top_10[df_top_10['date'].dt.year.isin([2021, 2022, 2023])]

# Process df_emotions
df_emotions['date'] = pd.to_datetime(df_emotions['date'], format='%m/%d/%y', errors='coerce')
df_emotions = df_emotions[df_emotions['date'].notna()]
df_emotions = df_emotions[
    (df_emotions['date'].dt.month.isin(list(range(1, 13)))) &
    (df_emotions['date'].dt.year.isin([2020, 2021, 2022, 2023, 2024]))
]

# Process df_top_10_extraction
df_top_10_extraction['date'] = pd.to_datetime(
    df_top_10_extraction[['year', 'Month', 'DayNo']].astype(str).agg('-'.join, axis=1),
    errors='coerce'
)
df_top_10_extraction = df_top_10_extraction[df_top_10_extraction['date'].notna()]
df_top_10_extraction = df_top_10_extraction[df_top_10_extraction['date'].dt.year.isin([2021, 2022, 2023])]

# Remove the neutral emotion from dataframes
df_top_10 = df_top_10[df_top_10['label'].isin(['sadness', 'anger', 'disgust', 'fear', 'joy', 'surprise'])]
df_top_10_extraction = df_top_10_extraction[
    df_top_10_extraction['label'].isin(['sadness', 'anger', 'disgust', 'fear', 'joy', 'surprise'])
]

# Define custom colors for each emotion
custom_colors = {
    'sadness': 'cornflowerblue',
    'anger': 'royalblue',
    'disgust': 'orange',
    'fear': 'gray',
    'joy': 'yellow',
    'surprise': 'green'
}

# Define the order of emotions from most positive to most negative
emotion_order = ['joy', 'surprise', 'sadness', 'fear', 'disgust', 'anger']

# ------------------------------
# Function Definitions
# ------------------------------

def get_collective_emotion_line(selected_year):
    """Return a Plotly line chart showing collective emotional fluctuations."""
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]

    # For each hiker, determine the dominant emotion per day using the same logic as in individual graphs
    dominant_collective = (
        df_year.groupby(['Hiker trail name', 'date'], as_index=False)
               .apply(lambda x: x.loc[x['label'].idxmax()])
               .reset_index(drop=True)
    )

    fig = px.line(
        dominant_collective,
        x='date',
        y='label',
        color='Hiker trail name',
        title=f"Collective Emotional Fluctuations ({selected_year})",
        labels={'date': 'Date', 'label': 'Emotion'},
        color_discrete_map=custom_colors,
        category_orders={'label': emotion_order},
        line_shape='spline'
    )

    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Emotion',
        title={
            'text': f"Collective Emotional Fluctuations ({selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black")
    )

    # Compute phase boundaries and add vertical dashed lines
    x_min = dominant_collective['date'].min()
    x_max = dominant_collective['date'].max()
    phase_1_end = x_min + (x_max - x_min) / 3
    phase_2_end = x_min + 2 * (x_max - x_min) / 3

    fig.add_shape(
        type='line',
        x0=phase_1_end, y0=0, x1=phase_1_end, y1=1,
        line=dict(color='Red', dash='dash'),
        xref='x', yref='paper'
    )
    fig.add_shape(
        type='line',
        x0=phase_2_end, y0=0, x1=phase_2_end, y1=1,
        line=dict(color='Blue', dash='dash'),
        xref='x', yref='paper'
    )

    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{y}<br>Hiker: %{customdata}',
        customdata=dominant_collective[['Hiker trail name']]
    )
    return fig

def create_hiker_graph(df_hiker, hiker, selected_year):
    """Return a Plotly line chart showing an individual hiker's emotional fluctuations."""
    dominant_emotion_hiker = df_hiker.groupby(['date'], as_index=False)\
                                     .apply(lambda x: x.loc[x['label'].idxmax()])

    fig = px.line(
        dominant_emotion_hiker,
        x='date',
        y='label',
        title=f"Emotional Fluctuations for {hiker} ({selected_year})",
        labels={'date': 'Date', 'label': 'Emotion'},
        color_discrete_map=custom_colors,
        category_orders={'label': emotion_order},
        line_shape='spline'
    )

    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Emotion',
        title={
            'text': f"Emotional Fluctuations for {hiker} ({selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        showlegend=False
    )

    # Compute phase boundaries and add vertical dashed lines
    x_min = dominant_emotion_hiker['date'].min()
    x_max = dominant_emotion_hiker['date'].max()
    phase_1_end = x_min + (x_max - x_min) / 3
    phase_2_end = x_min + 2 * (x_max - x_min) / 3

    fig.add_shape(
        type='line',
        x0=phase_1_end, y0=0, x1=phase_1_end, y1=1,
        line=dict(color='Red', dash='dash'),
        xref='x', yref='paper'
    )
    fig.add_shape(
        type='line',
        x0=phase_2_end, y0=0, x1=phase_2_end, y1=1,
        line=dict(color='Blue', dash='dash'),
        xref='x', yref='paper'
    )

    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{y}',
        customdata=dominant_emotion_hiker[['label']].values
    )
    fig.update_layout(dragmode='zoom')
    return fig

def get_monthly_emotion_trends(selected_year):
    """Return a bar chart of the dominant emotion by month."""
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
    monthly_emotion_trends = df_year.groupby([df_year['date'].dt.to_period('M'), 'label'])\
                                    .size().reset_index(name='count')
    monthly_emotion_trends['date'] = monthly_emotion_trends['date'].dt.to_timestamp()
    dominant_emotion_by_month = monthly_emotion_trends.loc[
        monthly_emotion_trends.groupby('date')['count'].idxmax()
    ]
    fig = px.bar(
        dominant_emotion_by_month,
        x='date',
        y='count',
        color='label',
        title=f"Dominant Emotion by Month ({selected_year})",
        labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
        color_discrete_map=custom_colors,
        text='count'
    )
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Dominant Emotion by Month ({selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        showlegend=False
    )
    return fig

def get_emotion_proportions(selected_year):
    """Return a bar chart of emotion proportions for the selected year."""
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
    total_emotions = df_year['label'].value_counts().sum()
    emotion_proportions = (df_year['label'].value_counts() / total_emotions).reset_index()
    emotion_proportions.columns = ['Emotion', 'Proportion']

    fig = px.bar(
        emotion_proportions,
        x='Emotion',
        y='Proportion',
        color='Emotion',
        title=f"Emotion Proportions ({selected_year})",
        labels={'Emotion': 'Emotion', 'Proportion': 'Proportion'},
        color_discrete_map=custom_colors,
        text='Proportion'
    )
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Emotion',
        yaxis_title='Proportion',
        title={
            'text': f"Emotion Proportions ({selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        showlegend=False
    )
    return fig

def get_proportion_bar(selected_year):
    """Return a bar chart for hikers' emotions proportion over time."""
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label'])\
                            .size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()

    total_counts = emotion_counts.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts = emotion_counts.merge(total_counts, on='date')
    emotion_counts['proportion'] = emotion_counts['count'] / emotion_counts['total_count']

    fig = px.bar(
        emotion_counts,
        x='date',
        y='proportion',
        color='label',
        hover_data=['label', 'count', 'proportion'],
        title=f"Hikers' Emotions Proportion Over Time ({selected_year})",
        labels={'date': 'Date', 'proportion': 'Proportion', 'label': 'Emotion'},
        color_discrete_map=custom_colors
    )
    fig.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Proportion',
        title={
            'text': f"Hikers' Emotions Proportion Over Time ({selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{y:.2%}',
        texttemplate='%{y:.2%}', textposition='outside',
        customdata=emotion_counts[['label', 'count']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_count_bar(selected_year):
    """Return a bar chart for hikers' emotions count over time."""
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label'])\
                            .size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()

    fig = px.bar(
        emotion_counts,
        x='date',
        y='count',
        color='label',
        hover_data=['label', 'count'],
        title=f"Hikers' Emotions Count Over Time ({selected_year})",
        labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
        color_discrete_map=custom_colors
    )
    fig.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Hikers' Emotions Count Over Time ({selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{y}',
        texttemplate='%{y}', textposition='outside',
        customdata=emotion_counts[['label', 'count']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_top_10_monthly_counts(selected_year):
    """Return a bar chart for top 10% hikers' emotion counts over time (monthly)."""
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label'])\
                            .size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()
    total_counts = emotion_counts.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts = emotion_counts.merge(total_counts, on='date')
    emotion_counts['proportion'] = emotion_counts['count'] / emotion_counts['total_count']

    fig = px.bar(
        emotion_counts,
        x='date',
        y='count',
        color='label',
        hover_data=['label', 'count', 'proportion'],
        title=f"Top 10% Hikers' Emotions Count Over Time (Monthly, {selected_year})",
        labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
        color_discrete_map=custom_colors
    )
    fig.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Top 10% Hikers' Emotions Count Over Time (Monthly, {selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{customdata[2]:.2%}',
        texttemplate='%{y}', textposition='outside',
        customdata=emotion_counts[['label', 'count', 'proportion']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_top_10_monthly_proportions(selected_year):
    """Return a stacked bar chart for top 10% hikers' emotions proportions over time (monthly)."""
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label'])\
                            .size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()
    total_counts = emotion_counts.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts = emotion_counts.merge(total_counts, on='date')
    emotion_counts['proportion'] = emotion_counts['count'] / emotion_counts['total_count']

    fig = px.bar(
        emotion_counts,
        x='date',
        y='proportion',
        color='label',
        hover_data=['label', 'count', 'proportion'],
        title=f"Top 10% Hikers' Emotions Proportion Over Time (Monthly, {selected_year})",
        labels={'date': 'Date', 'proportion': 'Emotion Proportion', 'label': 'Emotion'},
        color_discrete_map=custom_colors
    )
    fig.update_layout(
        barmode='stack',
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Proportion',
        title={
            'text': f"Top 10% Hikers' Emotions Proportion Over Time (Monthly, {selected_year})",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{customdata[2]:.2%}',
        texttemplate='%{y:.2%}', textposition='outside',
        customdata=emotion_counts[['label', 'count', 'proportion']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

# ------------------------------
# Streamlit Layout & Display
# ------------------------------

st.title("Hikers' Emotions Visualization Dashboard")
st.write("""
This interactive dashboard displays various aspects of hikers' emotional experiences over time.
Use the sidebar to select the year of interest and explore the graphs below. Key insights include:

- **Collective Trends:** How emotions fluctuate collectively across all hiker trails.
- **Monthly Dominance:** Which emotion was most dominant each month.
- **Proportions & Counts:** Overall emotion proportions and counts over time.
- **Top 10% Analysis:** Detailed insights for the top 10% hiker group.
""")

# Sidebar: Year Selection
year_options = sorted(df_top_10['date'].dt.year.unique())
selected_year = st.sidebar.selectbox("Select Year", options=year_options, index=year_options.index(2022) if 2022 in year_options else 0)

# Section: Collective Emotional Fluctuations
st.header("Collective Emotional Fluctuations")
st.write("This graph shows the collective emotional fluctuations for all hikers during the selected year. Each line corresponds to one hiker, and key hiking phases are highlighted with vertical dashed lines.")
fig_collective = get_collective_emotion_line(selected_year)
st.plotly_chart(fig_collective, use_container_width=True)

# Section: Individual Hiker Emotional Fluctuations
st.header("Individual Hiker Emotional Fluctuations")
st.write("Below are the emotional fluctuation graphs for individual hikers. Hover over each graph to see the dominant emotion on each day.")
df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
hiker_names = sorted(df_year['Hiker trail name'].unique())
for hiker in hiker_names:
    st.subheader(f"Emotional Fluctuations for {hiker}")
    df_hiker = df_year[df_year['Hiker trail name'] == hiker]
    fig_hiker = create_hiker_graph(df_hiker, hiker, selected_year)
    st.plotly_chart(fig_hiker, use_container_width=True)

# Section: Monthly Emotion Trends
st.header("Monthly Dominant Emotions")
st.write("This bar chart displays the dominant emotion for each month based on the highest count on that month.")
fig_monthly = get_monthly_emotion_trends(selected_year)
st.plotly_chart(fig_monthly, use_container_width=True)

# Section: Emotion Proportions
st.header("Overall Emotion Proportions")
st.write("This chart shows the proportion of each emotion for the selected year.")
fig_proportions = get_emotion_proportions(selected_year)
st.plotly_chart(fig_proportions, use_container_width=True)

# Section: Hikers' Emotions Proportion Over Time
st.header("Hikers' Emotions Proportion Over Time")
st.write("This chart displays the proportion of emotions on a monthly basis. Hover over the bars to see exact proportions and counts.")
fig_prop_bar = get_proportion_bar(selected_year)
st.plotly_chart(fig_prop_bar, use_container_width=True)

# Section: Hikers' Emotions Count Over Time
st.header("Hikers' Emotions Count Over Time")
st.write("This chart shows the raw count of emotions on a monthly basis for the selected year.")
fig_count_bar = get_count_bar(selected_year)
st.plotly_chart(fig_count_bar, use_container_width=True)

# Section: Top 10% Hikers Analysis (Counts)
st.header("Top 10% Hikers' Emotions Count (Monthly)")
st.write("This chart focuses on the top 10% hiker group, showing the monthly count of emotions.")
fig_top10_counts = get_top_10_monthly_counts(selected_year)
st.plotly_chart(fig_top10_counts, use_container_width=True)

# Section: Top 10% Hikers Analysis (Proportions)
st.header("Top 10% Hikers' Emotions Proportion (Monthly)")
st.write("This stacked bar chart displays the monthly emotion proportions for the top 10% hiker group.")
fig_top10_props = get_top_10_monthly_proportions(selected_year)
st.plotly_chart(fig_top10_props, use_container_width=True)
