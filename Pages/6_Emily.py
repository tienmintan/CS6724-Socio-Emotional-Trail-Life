import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------
# Set page configuration as the very first command (required)
# ----------------------------------------------------------------
st.set_page_config(page_title="Hikers' Emotions Dashboard", layout="wide")

# ------------------------------
# Custom CSS & Banner
# ------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        color: #333333;
    }
    .main {
        padding: 2rem;
    }
    .banner {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display a banner image with use_container_width instead of use_column_width
st.image("https://psychologicalcenter.com/wp-content/uploads/sites/76/2022/06/Hiker2-1024x576.jpg", use_container_width=True)

# ------------------------------
# Page Intro & Overview
# ------------------------------

st.title("🏞️ Hikers' Emotions Visualization Dashboard")
st.markdown("""
Welcome to the **Hikers' Emotions Dashboard**! This interactive tool is tailored for the Appalachian Trail community to help you explore and understand the emotional dynamics of long-distance hiking.

### Why is this Dashboard Important? 🤔
- **Emotional Awareness:** Research—including a 2024 study from Virginia Tech—shows that long-distance hiking is an emotional roller coaster. Hikers frequently express a mix of **joy** (boosted by endorphins and sunlight) and **fear** (stemming from steep, unfamiliar terrain and adverse weather).
- **Mental Health & Growth:** Many hikers seek mental clarity or healing on the trail while sometimes confronting underlying challenges like anxiety or depression.
- **Post-Trail Adjustment:** The transition back to daily life can be challenging, and understanding these dynamics can help in preparing for and managing post-trail emotions.
- **Nature’s Therapeutic Effects:** Exposure to natural light and the calming sounds of birdsong significantly enhance mood and sleep patterns.
- **Resource Guidance:** This dashboard also points you towards valuable resources (e.g., HIKE for Mental Health, The Umbrella Project) that support the well-being of hikers.

Explore the sections below to dive into personalized and aggregated insights that can empower you to plan a safer, more fulfilling journey on the Appalachian Trail! 🚶‍♂️🌄
""")

# ------------------------------
# Data Loading & Preprocessing
# ------------------------------

# Define file paths (adjust these file paths as needed)
file_path_top_10 = '2025-03-25_Top10Pct.xlsx'
file_path_emotions = 'Emotions Visualization Chart.xlsx'
file_path_top_10_extraction = 'Top Ten Percent Data Extraction.xlsx'

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

# Remove rows with emotions outside the target list
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
# Function Definitions for Graphs
# (Note: The collective graph is omitted as per request.)
# ------------------------------

def create_hiker_graph(df_hiker, hiker, selected_year):
    """Returns an individual hiker's emotional fluctuations line chart."""
    dominant_emotion_hiker = df_hiker.groupby(['date'], as_index=False).apply(lambda x: x.loc[x['label'].idxmax()])
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
    # Add phase boundaries (vertical dashed lines)
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
    """Returns a bar chart of the dominant emotion by month (with count and computed proportion)."""
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
    monthly_emotion_trends = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
    monthly_emotion_trends['date'] = monthly_emotion_trends['date'].dt.to_timestamp()
    monthly_totals = monthly_emotion_trends.groupby('date')['count'].sum().reset_index(name='total')
    dominant_emotion_by_month = monthly_emotion_trends.loc[
        monthly_emotion_trends.groupby('date')['count'].idxmax()
    ]
    dominant_emotion_by_month = dominant_emotion_by_month.merge(monthly_totals, on='date')
    dominant_emotion_by_month['proportion'] = dominant_emotion_by_month['count'] / dominant_emotion_by_month['total']
    
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
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{customdata[2]:.2%}',
        texttemplate='%{y}',
        textposition='outside',
        customdata=dominant_emotion_by_month[['label', 'count', 'proportion']].values
    )
    return fig

def get_emotion_proportions(selected_year):
    """Returns a bar chart summarizing overall emotion proportions (with raw counts)."""
    df_year = df_top_10[df_top_10['date'].dt.year == selected_year]
    counts = df_year['label'].value_counts().reset_index()
    counts.columns = ['Emotion', 'count']
    total_emotions = counts['count'].sum()
    counts['Proportion'] = counts['count'] / total_emotions
    
    fig = px.bar(
        counts,
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
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{y:.2%}',
        texttemplate='%{y:.2%}',
        textposition='outside',
        customdata=counts[['Emotion', 'count', 'Proportion']].values
    )
    return fig

def get_proportion_bar(selected_year):
    """Returns a bar chart for hikers' emotion proportions over time."""
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
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
        texttemplate='%{y:.2%}',
        textposition='outside',
        customdata=emotion_counts[['label', 'count', 'proportion']].values
    )
    return fig

def get_count_bar(selected_year):
    """Returns a bar chart for hikers' emotion counts over time."""
    df_year = df_emotions[df_emotions['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
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
        texttemplate='%{y}',
        textposition='outside',
        customdata=emotion_counts[['label', 'count']].values
    )
    return fig

def get_top_10_monthly_counts(selected_year):
    """Returns a bar chart for top 10% hikers' emotion counts (monthly)."""
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
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
        texttemplate='%{y}',
        textposition='outside',
        customdata=emotion_counts[['label', 'count', 'proportion']].values
    )
    return fig

def get_top_10_monthly_proportions(selected_year):
    """Returns a stacked bar chart for top 10% hikers' emotion proportions (monthly)."""
    df_year = df_top_10_extraction[df_top_10_extraction['date'].dt.year == selected_year]
    emotion_counts = df_year.groupby([df_year['date'].dt.to_period('M'), 'label']).size().reset_index(name='count')
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
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{customdata[1]}<br>Proportion: %{y:.2%}',
        texttemplate='%{y:.2%}',
        textposition='outside',
        customdata=emotion_counts[['label', 'count', 'proportion']].values
    )
    return fig

# ------------------------------
# Streamlit Layout & Display with Enhanced Aesthetics & Research Details
# ------------------------------

# Sidebar: Year Selection
year_options = sorted(df_top_10['date'].dt.year.unique())
selected_year = st.sidebar.selectbox("🗓️ Select Year", options=year_options, index=year_options.index(2022) if 2022 in year_options else 0)

# Section: Individual Hiker Emotional Fluctuations
st.header("👣 Individual Hiker Emotional Fluctuations")
st.markdown("""
Each graph below captures a hiker’s unique emotional journey along the Appalachian Trail.

**Why this is important:**  
- **Self-Reflection:** Recognizing your own emotional patterns aids in mental preparation and safety planning.  
- **Community Insight:** Comparing individual trends can build a supportive hiking community.
""")
df_year_filtered = df_top_10[df_top_10['date'].dt.year == selected_year]
for hiker in sorted(df_year_filtered['Hiker trail name'].unique()):
    st.subheader(f"Emotional Fluctuations for **{hiker}**")
    df_hiker = df_year_filtered[df_year_filtered['Hiker trail name'] == hiker]
    fig_hiker = create_hiker_graph(df_hiker, hiker, selected_year)
    st.plotly_chart(fig_hiker, use_container_width=True)

# Section: Monthly Dominant Emotions
st.header("📊 Monthly Dominant Emotions")
st.markdown("""
This chart displays the dominant emotion for each month along the trail.

**Key Insights:**  
- A 2024 study revealed that hikers frequently experience a blend of **joy** and **fear** — weather conditions often amplify these emotions.  
- Data from 2022 suggests fewer active hikers, possibly due to external challenges such as weather or trail accessibility.
""")
fig_monthly = get_monthly_emotion_trends(selected_year)
st.plotly_chart(fig_monthly, use_container_width=True)

# Section: Overall Emotion Proportions
st.header("📈 Overall Emotion Proportions")
st.markdown("""
This visualization summarizes the overall emotional landscape during the selected year.

**Why it Matters:**  
- It provides a snapshot of the collective emotional state on the trail, highlighting the balance between **joy** and **fear** — an essential duality in long-distance hiking.
""")
fig_proportions = get_emotion_proportions(selected_year)
st.plotly_chart(fig_proportions, use_container_width=True)

# Section: Hikers' Emotions Proportion Over Time
st.header("⏳ Emotions Proportion Over Time")
st.markdown("""
This chart tracks the evolution of emotion proportions on a monthly basis.

**Observations:**  
- Shifts in the balance between emotions may point to seasonal factors or specific trail segments affecting mood.
""")
fig_prop_bar = get_proportion_bar(selected_year)
st.plotly_chart(fig_prop_bar, use_container_width=True)

# Section: Hikers' Emotions Count Over Time
st.header("🔢 Emotions Count Over Time")
st.markdown("""
Here we show the raw monthly counts of emotional expressions recorded on the trail.

**Takeaway:**  
- Higher counts might indicate moments of intensive trail activity or emotional peaks.
- Notably, 2022 shows a decline compared to 2021 and 2023.
""")
fig_count_bar = get_count_bar(selected_year)
st.plotly_chart(fig_count_bar, use_container_width=True)

# Section: Top 10% Hikers Analysis (Counts)
st.header("🚩 Top 10% Hikers' Emotions Count (Monthly)")
st.markdown("""
This chart focuses on the top 10% of hikers — the most engaged users — displaying their monthly emotion counts.

**Insight:**  
- These data points can serve as early indicators of significant shifts in trail sentiment.
""")
fig_top10_counts = get_top_10_monthly_counts(selected_year)
st.plotly_chart(fig_top10_counts, use_container_width=True)

# Section: Top 10% Hikers Analysis (Proportions)
st.header("📊 Top 10% Hikers' Emotions Proportion (Monthly)")
st.markdown("""
This stacked bar chart illustrates the emotion proportions among the top 10% of hikers.

**Key Insight:**  
- The mix of **fear** and **joy** in this segment underlines the intensity and complexity of experiences among the most active trail users.
""")
fig_top10_props = get_top_10_monthly_proportions(selected_year)
st.plotly_chart(fig_top10_props, use_container_width=True)

# Additional Research & Resources Section
st.header("📖 Additional Research & Resources")
st.markdown("""
### Emotional Dynamics of Long-Distance Hiking 🌄💬

**The Trail as an Emotional Journey:**  
A 2024 study from Virginia Tech analyzed hikers' blogs and revealed that long-distance hiking is an emotional roller coaster, where **joy** 😊 and **fear** 😱 are predominant. Adverse weather often increases fear and frustration.  
**Sources:** Homemade Wanderlust, ResearchGate, ACM Digital Library  

---

### Mental Health Challenges and Growth 🧠🌱

Many hikers embark on the trail seeking mental clarity or healing, yet the journey can also unveil unresolved issues such as **depression**, **anxiety**, and **PTSD**. Facing these challenges often leads to significant personal growth and a deeper understanding of oneself.  
**Source:** The Trek  

---

### Post-Trail Adjustment Difficulties 🔄😔

Returning to everyday life after a long hike can be daunting. Many hikers report post-trail depression and a sense of loss, making reintegration a challenging process.  
**Sources:** Reddit, The Trek  

---

### Nature's Therapeutic Effects 🌿✨

- **Natural Light:** Enhances mood and regulates sleep by boosting serotonin levels and stabilizing circadian rhythms.  
- **Birdsong:** Offers a natural stress reliever and contributes to a calming, serene hiking experience.  
**Source:** Appalachian Trail Conservancy  

---

### Mental Toughness & Resilience 💪🏽🏋️‍♂️

Research indicates that while day hikers may excel in short-term toughness, thru-hikers demonstrate exceptional resilience over time—a vital trait for enduring the physical and emotional challenges of the trail.

---

### Helpful Resources & Community Support 📌

- **HIKE for Mental Health:** Explore [ihike.org](https://ihike.org) for hikes that promote mental health awareness.  
- **The Umbrella Project:** Offers therapeutic backpacking experiences for grief support.  
- **Appalachian Trail Conservancy:** Provides a resource library on hiking safety and health.  
- **Post-Trail Transition Guides:** Read articles like *"Coming Back to Base"* and *"Adjusting to Life at Home"* for tips on post-hike reintegration.  
- **Community Forums:** Connect with fellow hikers on Reddit’s [r/AppalachianTrail](https://www.reddit.com/r/AppalachianTrail/) and Trail Forums to share experiences and support each other.

---

Stay informed, stay safe, and keep the trail spirit alive! 🌟🚶‍♀️🌄
""")
