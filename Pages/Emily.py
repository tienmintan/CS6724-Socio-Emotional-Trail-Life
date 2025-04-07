import streamlit as st
import pandas as pd
import plotly.express as px

# Emily's code is below
# Define the file paths
file_path_top_10 = '/emilyelkins/2025-03-25_Top10Pct.xlsx'
file_path_emotions = '/emilyelkins/Emotions Visualization Chart.xlsx'
file_path_top_10_extraction = '/emilyelkins/Top Ten Percent Data Extraction.xlsx'

# Load the Excel files
df_top_10 = pd.read_excel(file_path_top_10, sheet_name='Top_10pct_Miles_2021-23', engine='openpyxl')
df_emotions = pd.read_excel(file_path_emotions, engine='openpyxl')
df_top_10_extraction = pd.read_excel(file_path_top_10_extraction, engine='openpyxl')

# Filter the data for the specified date range
df_top_10['date'] = pd.to_datetime(df_top_10[['year', 'Month', 'DayNo']].astype(str).agg('-'.join, axis=1), errors='coerce')
df_top_10 = df_top_10[df_top_10['date'].notna()]
df_top_10 = df_top_10[(df_top_10['date'].dt.year.isin([2021, 2022, 2023]))]

df_emotions['date'] = pd.to_datetime(df_emotions['date'], format='%m/%d/%y', errors='coerce')
df_emotions = df_emotions[df_emotions['date'].notna()]
df_emotions = df_emotions[(df_emotions['date'].dt.month.isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])) & (df_emotions['date'].dt.year.isin([2020, 2021, 2022, 2023, 2024]))]

df_top_10_extraction['date'] = pd.to_datetime(df_top_10_extraction[['year', 'Month', 'DayNo']].astype(str).agg('-'.join, axis=1), errors='coerce')
df_top_10_extraction = df_top_10_extraction[df_top_10_extraction['date'].notna()]
df_top_10_extraction = df_top_10_extraction[(df_top_10_extraction['date'].dt.year.isin([2021, 2022, 2023]))]

# Remove the neutral emotion from df_top_10 and df_top_10_extraction
df_top_10 = df_top_10[df_top_10['label'].isin(['sadness', 'anger', 'disgust', 'fear', 'joy', 'surprise'])]
df_top_10_extraction = df_top_10_extraction[df_top_10_extraction['label'].isin(['sadness', 'anger', 'disgust', 'fear', 'joy', 'surprise'])]

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

# Function to create the line graph for a hiker
def create_hiker_graph(df_hiker, hiker, selected_year):
    dominant_emotion_hiker = df_hiker.groupby(['date'], as_index=False).apply(lambda x: x.loc[x['label'].idxmax()])
    fig_hiker = px.line(dominant_emotion_hiker, x='date', y='label',
                        title=f"Emotional Fluctuations for {hiker} ({selected_year})",
                        labels={'date': 'Date', 'label': 'Emotion'},
                        color_discrete_map=custom_colors,
                        category_orders={'label': emotion_order},
                        line_shape='spline')
    fig_hiker.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Emotion',
        title={
            'text': f"Emotional Fluctuations for {hiker} ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        showlegend=False
    )
    x_min = dominant_emotion_hiker['date'].min()
    x_max = dominant_emotion_hiker['date'].max()
    phase_1_end = x_min + (x_max - x_min) / 3
    phase_2_end = x_min + 2 * (x_max - x_min) / 3
    fig_hiker.add_shape(
        type='line',
        x0=phase_1_end,
        y0=0,
        x1=phase_1_end,
        y1=1,
        line=dict(color='Red', dash='dash'),
        xref='x',
        yref='paper'
    )
    fig_hiker.add_shape(
        type='line',
        x0=phase_2_end,
        y0=0,
        x1=phase_2_end,
        y1=1,
        line=dict(color='Blue', dash='dash'),
        xref='x',
        yref='paper'
    )
    fig_hiker.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{y}',
        customdata=dominant_emotion_hiker[['label']].values
    )
    fig_hiker.update_layout(dragmode='zoom')
    return fig_hiker

# Function to create the monthly emotion trends graph
def create_monthly_emotion_trends(selected_year):
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
    monthly_emotion_trends = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    monthly_emotion_trends['date'] = monthly_emotion_trends['date'].dt.to_timestamp()
    dominant_emotion_by_month = monthly_emotion_trends.loc[monthly_emotion_trends.groupby('date')['count'].idxmax()]
    fig_monthly_emotion_trends = px.bar(dominant_emotion_by_month, x='date', y='count', color='label',
                                        title=f"Dominant Emotion by Month ({selected_year})",
                                        labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
                                        color_discrete_map=custom_colors,
                                        text='count')
    fig_monthly_emotion_trends.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Dominant Emotion by Month ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        showlegend=False
    )
    return fig_monthly_emotion_trends

# Function to create the emotion proportions graph
def create_emotion_proportions(selected_year):
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
    total_emotions = df_year['label'].value_counts().sum()
    emotion_proportions = (df_year['label'].value_counts() / total_emotions).reset_index()
    emotion_proportions.columns = ['Emotion', 'Proportion']
    fig_emotion_proportions = px.bar(emotion_proportions, x='Emotion', y='Proportion', color='Emotion',
                                     title=f"Emotion Proportions ({selected_year})",
                                     labels={'Emotion': 'Emotion', 'Proportion': 'Proportion'},
                                     color_discrete_map=custom_colors,
                                     text='Proportion')
    fig_emotion_proportions.update_layout(
        hovermode='x unified',
        xaxis_title='Emotion',
        yaxis_title='Proportion',
        title={
            'text': f"Emotion Proportions ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        showlegend=False
    )
    return fig_emotion_proportions
# Function to create the proportion bar chart
def create_proportion_bar(selected_year):
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()

    total_counts = emotion_counts.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts = emotion_counts.merge(total_counts, on='date')
    emotion_counts['proportion'] = emotion_counts['count'] / emotion_counts['total_count']

    fig_proportion_bar = px.bar(emotion_counts, x='date', y='proportion', color='label',
                                hover_data=['label', 'count', 'proportion'],
                                title=f"Hikers' Emotions Proportion Over Time ({selected_year})",
                                labels={'date': 'Date', 'proportion': 'Proportion', 'label': 'Emotion'},
                                color_discrete_map=custom_colors)

    fig_proportion_bar.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Proportion',
        title={
            'text': f"Hikers' Emotions Proportion Over Time ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_proportion_bar.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{y:.2%}',
        texttemplate='%{y:.2%}', textposition='outside',
        customdata=emotion_counts[['label', 'count']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_proportion_bar

# Function to create the count bar chart
def create_count_bar(selected_year):
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()

    fig_count_bar = px.bar(emotion_counts, x='date', y='count', color='label',
                           hover_data=['label', 'count'],
                           title=f"Hikers' Emotions Count Over Time ({selected_year})",
                           labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
                           color_discrete_map=custom_colors)

    fig_count_bar.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Hikers' Emotions Count Over Time ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_count_bar.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{y}',
        texttemplate='%{y}', textposition='outside',
        customdata=emotion_counts[['label', 'count']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_count_bar

# Function to create the top 10 monthly counts chart
def create_top_10_monthly_counts(selected_year):
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts_top_10_monthly = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts_top_10_monthly['date'] = emotion_counts_top_10_monthly['date'].dt.to_timestamp()

    total_counts_monthly = emotion_counts_top_10_monthly.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts_top_10_monthly = emotion_counts_top_10_monthly.merge(total_counts_monthly, on='date')
    emotion_counts_top_10_monthly['proportion'] = emotion_counts_top_10_monthly['count'] / emotion_counts_top_10_monthly['total_count']

    fig_top_10_monthly_counts = px.bar(emotion_counts_top_10_monthly, x='date', y='count', color='label',
                                       hover_data=['label', 'count', 'proportion'],
                                       title=f"Top 10% Hikers' Emotions Count Over Time (Monthly, {selected_year})",
                                       labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
                                       color_discrete_map=custom_colors)

    fig_top_10_monthly_counts.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Top 10% Hikers' Emotions Count Over Time (Monthly, {selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_top_10_monthly_counts.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{customdata[2]:.2%}',
        texttemplate='%{y}', textposition='outside',
        customdata=emotion_counts_top_10_monthly[['label', 'count', 'proportion']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_top_10_monthly_counts

# Function to create the top 10 monthly proportions chart
def create_top_10_monthly_proportions(selected_year):
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts_top_10_monthly = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts_top_10_monthly['date'] = emotion_counts_top_10_monthly['date'].dt.to_timestamp()

    total_counts_monthly = emotion_counts_top_10_monthly.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts_top_10_monthly = emotion_counts_top_10_monthly.merge(total_counts_monthly, on='date')
    emotion_counts_top_10_monthly['proportion'] = emotion_counts_top_10_monthly['count'] / emotion_counts_top_10_monthly['total_count']

    fig_top_10_monthly_proportions = px.bar(emotion_counts_top_10_monthly, x='date', y='proportion', color='label',
                                            hover_data=['label', 'count', 'proportion'],
                                            title=f"Top 10% Hikers' Emotions Proportion Over Time (Monthly, {selected_year})",
                                            labels={'date': 'Date', 'proportion': 'Emotion Proportion', 'label': 'Emotion'},
                                            color_discrete_map=custom_colors)

    fig_top_10_monthly_proportions.update_layout(
        barmode='stack',
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Proportion',
        title={
            'text': f"Top 10% Hikers' Emotions Proportion Over Time (Monthly, {selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
# Function to create the proportion bar chart
def create_proportion_bar(selected_year):
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()

    total_counts = emotion_counts.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts = emotion_counts.merge(total_counts, on='date')
    emotion_counts['proportion'] = emotion_counts['count'] / emotion_counts['total_count']

    fig_proportion_bar = px.bar(emotion_counts, x='date', y='proportion', color='label',
                                hover_data=['label', 'count', 'proportion'],
                                title=f"Hikers' Emotions Proportion Over Time ({selected_year})",
                                labels={'date': 'Date', 'proportion': 'Proportion', 'label': 'Emotion'},
                                color_discrete_map=custom_colors)

    fig_proportion_bar.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Proportion',
        title={
            'text': f"Hikers' Emotions Proportion Over Time ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_proportion_bar.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{y:.2%}',
        texttemplate='%{y:.2%}', textposition='outside',
        customdata=emotion_counts[['label', 'count']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_proportion_bar

# Function to create the count bar chart
def create_count_bar(selected_year):
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts['date'] = emotion_counts['date'].dt.to_timestamp()

    fig_count_bar = px.bar(emotion_counts, x='date', y='count', color='label',
                           hover_data=['label', 'count'],
                           title=f"Hikers' Emotions Count Over Time ({selected_year})",
                           labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
                           color_discrete_map=custom_colors)

    fig_count_bar.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Hikers' Emotions Count Over Time ({selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_count_bar.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{y}',
        texttemplate='%{y}', textposition='outside',
        customdata=emotion_counts[['label', 'count']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_count_bar

# Function to create the top 10 monthly counts chart
def create_top_10_monthly_counts(selected_year):
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts_top_10_monthly = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts_top_10_monthly['date'] = emotion_counts_top_10_monthly['date'].dt.to_timestamp()

    total_counts_monthly = emotion_counts_top_10_monthly.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts_top_10_monthly = emotion_counts_top_10_monthly.merge(total_counts_monthly, on='date')
    emotion_counts_top_10_monthly['proportion'] = emotion_counts_top_10_monthly['count'] / emotion_counts_top_10_monthly['total_count']

    fig_top_10_monthly_counts = px.bar(emotion_counts_top_10_monthly, x='date', y='count', color='label',
                                       hover_data=['label', 'count', 'proportion'],
                                       title=f"Top 10% Hikers' Emotions Count Over Time (Monthly, {selected_year})",
                                       labels={'date': 'Date', 'count': 'Emotion Count', 'label': 'Emotion'},
                                       color_discrete_map=custom_colors)

    fig_top_10_monthly_counts.update_layout(
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Count',
        title={
            'text': f"Top 10% Hikers' Emotions Count Over Time (Monthly, {selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig_top_10_monthly_counts.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{customdata[2]:.2%}',
        texttemplate='%{y}', textposition='outside',
        customdata=emotion_counts_top_10_monthly[['label', 'count', 'proportion']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_top_10_monthly_counts

# Function to create the top 10 monthly proportions chart
def create_top_10_monthly_proportions(selected_year):
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts_top_10_monthly = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    emotion_counts_top_10_monthly['date'] = emotion_counts_top_10_monthly['date'].dt.to_timestamp()

    total_counts_monthly = emotion_counts_top_10_monthly.groupby('date')['count'].sum().reset_index(name='total_count')
    emotion_counts_top_10_monthly = emotion_counts_top_10_monthly.merge(total_counts_monthly, on='date')
    emotion_counts_top_10_monthly['proportion'] = emotion_counts_top_10_monthly['count'] / emotion_counts_top_10_monthly['total_count']

    fig_top_10_monthly_proportions = px.bar(emotion_counts_top_10_monthly, x='date', y='proportion', color='label',
                                            hover_data=['label', 'count', 'proportion'],
                                            title=f"Top 10% Hikers' Emotions Proportion Over Time (Monthly, {selected_year})",
                                            labels={'date': 'Date', 'proportion': 'Emotion Proportion', 'label': 'Emotion'},
                                            color_discrete_map=custom_colors)

    fig_top_10_monthly_proportions.update_layout(
        barmode='stack',
        hovermode='x unified',
        clickmode='event+select',
        legend_title_text='Emotions',
        xaxis_title='Date',
        yaxis_title='Emotion Proportion',
        title={
            'text': f"Top 10% Hikers' Emotions Proportion Over Time (Monthly, {selected_year})",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="Black"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
     fig_top_10_monthly_proportions.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{customdata[2]:.2%}',
        texttemplate='%{y:.2%}', textposition='outside',
        customdata=emotion_counts_top_10_monthly[['label', 'count', 'proportion']].values,
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )

    return fig_top_10_monthly_proportions
    # End of Emily's code


st.set_page_config(
    page_title="Visualizations",  
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Visualizations Made By Emily")  

selected_year = st.selectbox("Select Year", [2021, 2022, 2023])
hiker_trail_names = df_top_10['Hiker trail name'].unique()
for hiker in hiker_trail_names:
    df_hiker = df_top_10[df_top_10['Hiker trail name'] == hiker]
    fig_hiker = create_hiker_graph(df_hiker, hiker, selected_year)
    st.plotly_chart(fig_hiker)
fig_monthly_emotion_trends = create_monthly_emotion_trends(selected_year)
st.plotly_chart(fig_monthly_emotion_trends)
fig_emotion_proportions = create_emotion_proportions(selected_year)
st.plotly_chart(fig_emotion_proportions)
fig_proportion_bar = create_proportion_bar(selected_year)
st.plotly_chart(fig_proportion_bar)
fig_count_bar = create_count_bar(selected_year)
st.plotly_chart(fig_count_bar)
fig_top_10_monthly_counts = create_top_10_monthly_counts(selected_year)
st.plotly_chart(fig_top_10_monthly_counts)
fig_top_10_monthly_proportions = create_top_10_monthly_proportions(selected_year)
st.plotly_chart(fig_top_10_monthly_proportions
