import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------
# 1) PAGE CONFIG (must be first)
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Hikers' Emotions Dashboard",
    layout="wide"
)

# ----------------------------------------------------------------
# 2) CUSTOM CSS FOR ACCESSIBILITY & ENGAGEMENT
# ----------------------------------------------------------------
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
      /* muted, semi‑transparent key‑insight boxes */
      .key-finding {
        background-color: rgba(2, 136, 209, 0.1);
        border-left: 4px solid rgba(2, 136, 209, 0.6);
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        font-size: 0.95rem;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------
# 3) PAGE TITLE & TABS
# ----------------------------------------------------------------
st.title("🏞️ Hikers' Emotions Visualization Dashboard")
tabs = st.tabs([
    "👣 Individual Journeys",
    "📊 Monthly Dominant",
    "📈 Overall Proportions",
    "⏳ Time Trends",
    "🔢 Raw Counts",
    "🚩 Top 10% Analysis"
])

# ----------------------------------------------------------------
# 4) DATA LOADING & PREPROCESSING
# ----------------------------------------------------------------
file_path_top_10            = '/Users/emilyelkins/Documents/SPRING 2025/PYTHON/CS6724-Socio-Emotional-Trail-Life/emilyelkins/2025-03-25_Top10Pct.xlsx'
file_path_emotions          = '/Users/emilyelkins/Documents/SPRING 2025/PYTHON/CS6724-Socio-Emotional-Trail-Life/emilyelkins/Emotions Visualization Chart.xlsx'
file_path_top_10_extraction = '/Users/emilyelkins/Documents/SPRING 2025/PYTHON/CS6724-Socio-Emotional-Trail-Life/emilyelkins/Top Ten Percent Data Extraction.xlsx'

df_top_10            = pd.read_excel(file_path_top_10, sheet_name='Top_10pct_Miles_2021-23', engine='openpyxl')
df_emotions          = pd.read_excel(file_path_emotions, engine='openpyxl')
df_top_10_extraction = pd.read_excel(file_path_top_10_extraction, engine='openpyxl')

# parse dates & filter target years
df_top_10['date'] = pd.to_datetime(
    df_top_10[['year','Month','DayNo']].astype(str).agg('-'.join, axis=1),
    errors='coerce'
)
df_top_10 = df_top_10[df_top_10['date'].dt.year.isin([2021,2022,2023])]

df_emotions['date'] = pd.to_datetime(df_emotions['date'], format='%m/%d/%y', errors='coerce')
df_emotions = df_emotions[df_emotions['date'].dt.year.isin([2020,2021,2022,2023,2024])]

df_top_10_extraction['date'] = pd.to_datetime(
    df_top_10_extraction[['year','Month','DayNo']].astype(str).agg('-'.join, axis=1),
    errors='coerce'
)
df_top_10_extraction = df_top_10_extraction[df_top_10_extraction['date'].dt.year.isin([2021,2022,2023])]

# filter to allowed emotions
allowed = ['sadness','anger','disgust','fear','joy','surprise']
df_top_10            = df_top_10   [df_top_10   ['label'].isin(allowed)]
df_top_10_extraction = df_top_10_extraction[df_top_10_extraction['label'].isin(allowed)]

# ----------------------------------------------------------------
# 5) ANONYMIZE ONLY df_top_10
# ----------------------------------------------------------------
unique_hikers = sorted(df_top_10['Hiker trail name'].unique())
anon_map = {orig: f"Hiker {i+1}" for i, orig in enumerate(unique_hikers)}
df_top_10['hiker_anon'] = df_top_10['Hiker trail name'].map(anon_map)

# ----------------------------------------------------------------
# 6) COLORS & EMOTION ORDER
# ----------------------------------------------------------------
custom_colors = {
    'sadness':'cornflowerblue',
    'anger':'royalblue',
    'disgust':'orange',
    'fear':'gray',
    'joy':'yellow',
    'surprise':'green'
}
emotion_order = ['joy','surprise','sadness','fear','disgust','anger']

# ----------------------------------------------------------------
# 7) SIDEBAR: YEAR SELECTOR
# ----------------------------------------------------------------
year_options  = sorted(df_top_10['date'].dt.year.unique())
selected_year = st.sidebar.selectbox(
    "🗓️ Select Year", year_options,
    index=year_options.index(2022) if 2022 in year_options else 0
)

# ----------------------------------------------------------------
# 8) GRAPH FUNCTIONS WITH RED‑ON‑SELECT
# ----------------------------------------------------------------
def create_hiker_graph(df_h, anon, yr):
    dom = df_h.groupby('date')\
              .apply(lambda x: x.loc[x['label'].idxmax()])\
              .reset_index(drop=True)
    fig = px.line(
        dom, x='date', y='label',
        title=f"Emotional Fluctuations for {anon} ({yr})",
        labels={'date':'Date','label':'Emotion'},
        color_discrete_map=custom_colors,
        category_orders={'label':emotion_order},
        line_shape='spline'
    )
    fig.update_layout(hovermode='x unified', showlegend=False, dragmode='zoom')
    # phase boundaries
    x0, x1 = dom['date'].min(), dom['date'].max()
    for frac, col in [(1/3,'red'), (2/3,'blue')]:
        xi = x0 + (x1 - x0) * frac
        fig.add_shape(dict(
            type='line', x0=xi, x1=xi, y0=0, y1=1,
            xref='x', yref='paper', line=dict(color=col, dash='dash')
        ))
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Emotion: %{y}')
    return fig

def get_monthly_emotion_trends(yr):
    d = df_top_10[df_top_10['date'].dt.year==yr]
    m = d.groupby([d['date'].dt.to_period('M'),'label'])\
         .size().reset_index(name='count')
    m['date'] = m['date'].dt.to_timestamp()
    tot = m.groupby('date')['count'].sum().reset_index(name='total')
    dm = m.loc[m.groupby('date')['count'].idxmax()].merge(tot, on='date')
    dm['prop'] = dm['count']/dm['total']
    fig = px.bar(
        dm, x='date', y='count', color='label', text='count',
        labels={'count':'Emotion Count'},
        color_discrete_map=custom_colors
    )
    fig.update_layout(hovermode='x unified', showlegend=False, clickmode='event+select')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>'
                      'Count: %{customdata[1]}<br>Prop: %{customdata[2]:.2%}',
        customdata=dm[['label','count','prop']].values,
        textposition='outside',
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_emotion_proportions(yr):
    d = df_top_10[df_top_10['date'].dt.year==yr]
    cnt = d['label'].value_counts().rename_axis('Emotion').reset_index(name='count')
    cnt['prop'] = cnt['count']/cnt['count'].sum()
    fig = px.bar(
        cnt, x='Emotion', y='prop', text='prop',
        color='Emotion', color_discrete_map=custom_colors
    )
    fig.update_layout(hovermode='x unified', showlegend=False, clickmode='event+select')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Count: %{customdata[1]}<br>Prop: %{y:.2%}',
        customdata=cnt[['Emotion','count']].values,
        texttemplate='%{y:.2%}', textposition='outside',
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_proportion_bar(yr):
    d = df_emotions[df_emotions['date'].dt.year==yr]
    m = d.groupby([d['date'].dt.to_period('M'),'label'])\
         .size().reset_index(name='count')
    m['date'] = m['date'].dt.to_timestamp()
    tot = m.groupby('date')['count'].sum().reset_index(name='total')
    m = m.merge(tot, on='date')
    m['prop'] = m['count']/m['total']
    fig = px.bar(
        m, x='date', y='prop', color='label',
        labels={'prop':'Proportion'}, color_discrete_map=custom_colors
    )
    fig.update_layout(hovermode='x unified',
                      legend=dict(orientation="h", y=1.02, x=1),
                      clickmode='event+select')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>'
                      'Count: %{customdata[1]}<br>Prop: %{y:.2%}',
        customdata=m[['label','count']].values,
        texttemplate='%{y:.2%}', textposition='outside',
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_count_bar(yr):
    d = df_emotions[df_emotions['date'].dt.year==yr]
    m = d.groupby([d['date'].dt.to_period('M'),'label'])\
         .size().reset_index(name='count')
    m['date'] = m['date'].dt.to_timestamp()
    fig = px.bar(
        m, x='date', y='count', color='label',
        labels={'count':'Emotion Count'}, color_discrete_map=custom_colors
    )
    fig.update_layout(hovermode='x unified',
                      legend=dict(orientation="h", y=1.02, x=1),
                      clickmode='event+select')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Count: %{y}',
        customdata=m[['label','count']].values,
        texttemplate='%{y}', textposition='outside',
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_top10_counts(yr):
    d = df_top_10_extraction[df_top_10_extraction['date'].dt.year==yr]
    m = d.groupby([d['date'].dt.to_period('M'),'label'])\
         .size().reset_index(name='count')
    m['date'] = m['date'].dt.to_timestamp()
    tot = m.groupby('date')['count'].sum().reset_index(name='total')
    m = m.merge(tot, on='date')
    m['prop'] = m['count']/m['total']
    fig = px.bar(
        m, x='date', y='count', color='label',
        labels={'count':'Emotion Count'}, color_discrete_map=custom_colors
    )
    fig.update_layout(hovermode='x unified',
                      legend=dict(orientation="h", y=1.02, x=1),
                      clickmode='event+select')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>'
                      'Count: %{customdata[1]}<br>Prop: %{customdata[2]:.2%}',
        customdata=m[['label','count','prop']].values,
        texttemplate='%{y}', textposition='outside',
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

def get_top10_props(yr):
    d = df_top_10_extraction[df_top_10_extraction['date'].dt.year==yr]
    m = d.groupby([d['date'].dt.to_period('M'),'label'])\
         .size().reset_index(name='count')
    m['date'] = m['date'].dt.to_timestamp()
    tot = m.groupby('date')['count'].sum().reset_index(name='total')
    m = m.merge(tot, on='date')
    m['prop'] = m['count']/m['total']
    fig = px.bar(
        m, x='date', y='prop', color='label',
        labels={'prop':'Proportion'}, color_discrete_map=custom_colors
    )
    fig.update_layout(barmode='stack',
                      hovermode='x unified',
                      legend=dict(orientation="h", y=1.02, x=1),
                      clickmode='event+select')
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Emotion: %{customdata[0]}<br>Prop: %{customdata[1]:.2%}',
        customdata=m[['label','prop']].values,
        texttemplate='%{y:.2%}', textposition='outside',
        selected=dict(marker=dict(color='red', opacity=1)),
        unselected=dict(marker=dict(opacity=0.3))
    )
    return fig

# ----------------------------------------------------------------
# 9) TAB CONTENT
# ----------------------------------------------------------------

# 1) Individual Journeys
with tabs[0]:
    st.header("👣 Individual Journeys (Anonymized)")
    st.markdown("""
    **What you see:**  
    A day‑by‑day line indicating each hiker’s emotions based on the date entered.  
    - **X‑axis (Date):** Daily progress  
    - **Y‑axis (Emotion):** From joy (top) to anger (bottom)  
    - **Dashed lines:** Mark three hiking phases (early, middle, final push)

    **Trip‑planning scenario:**  
    > *Imagine you’re planning a 25‑day thru‑hike and worried about mid‑trail slumps.  
    > Check “Hiker 3” to see when their joy dipped in Phase 2 — you can  
    > schedule a rest day or extra resupply at that point.*

    **Key insights:**  
    - Spot early‑phase fear spikes to pack extra comfort foods.  
    - Celebrate mid‑trail joy peaks with planned photo stops.  
    - Prepare mentally for end‑section fatigue before you hit it.
    """)
    dfy = df_top_10[df_top_10['date'].dt.year == selected_year]
    for anon in sorted(dfy['hiker_anon'].unique()):
        dfo = dfy[dfy['hiker_anon'] == anon]
        st.subheader(anon)
        st.plotly_chart(create_hiker_graph(dfo, anon, selected_year), use_container_width=True)


# 2) Monthly Dominant Emotions
with tabs[1]:
    st.header("📊 Monthly Dominant Emotions")
    st.markdown("""
    **What you see:**  
    A bar for each month showing the *single* most common emotion among all hikers.

    **Trip‑planning scenario:**  
    > *You want to start in May but are nervous about unpredictable weather.  
    > May’s dominant emotion is fear (red)—so plan for rain‑ready gear and  
    > consider an earlier start in April when joy was higher.*

    **Key insights:**  
    - Weather‑linked fear spikes in spring/fall.  
    - Summer months show consistent joy — ideal for first‑timers.  
    - 2022 dips suggest lower trail traffic — quieter, but less on‑trail support.
    """)
    st.plotly_chart(get_monthly_emotion_trends(selected_year), use_container_width=True)


# 3) Overall Emotion Proportions
with tabs[2]:
    st.header("📈 Overall Emotion Proportions")
    st.markdown("""
    **What you see:**  
    A summary of each emotion’s share across the entire year.

    **Trip‑planning scenario:**  
    > *You’re deciding whether to hike solo or in a group.  
    > If fear accounts for 40% and joy only 30%, you might prefer a buddy  
    > until you’re more comfortable with the trail.*

    **Key insights:**  
    - A high fear proportion signals the importance of community support.  
    - Balanced joy/fear encourages mid‑trail morale boosts like summit parties.  
    - Low disgust/anger shows overall positive hiker sentiment.
    """)
    st.plotly_chart(get_emotion_proportions(selected_year), use_container_width=True)


# 4) Emotions Proportion Over Time
with tabs[3]:
    st.header("⏳ Emotions Proportion Over Time")
    st.markdown("""
    **What you see:**  
    A stacked bar chart of emotion mixes month‑by‑month.

    **Trip‑planning scenario:**  
    > *Planning a June start? Notice June has 50% joy, 20% fear, 15% surprise.  
    > Pack extra sunscreen for those joyful sunny days and rain gear for the fearful 20%.*

    **Key insights:**  
    - Seasonal shifts (i.e. winter→fear, summer→joy).  
    - Surprise peaks could align with wildlife sightings or trail events.  
    - Use this to tailor mental‑health tactics month‑to‑month.
    """)
    st.plotly_chart(get_proportion_bar(selected_year), use_container_width=True)


# 5) Emotions Count Over Time
with tabs[4]:
    st.header("🔢 Emotions Count Over Time")
    st.markdown("""
    **What you see:**  
    Raw counts of emotion-labeled entries each month.

    **Trip‑planning scenario:**  
    > *You’d rather hike in less‑crowded months to avoid overpacked shelters.  
    > Notice February has only 10 entries vs July’s 200—ideal for solitude seekers.*

    **Key insights:**  
    - Peak activity in summer → expect crowded campsites.  
    - Off‑season dips show quieter trail but tougher weather.  
    - Use counts to choose your comfort vs. solitude balance.
    """)
    st.plotly_chart(get_count_bar(selected_year), use_container_width=True)


# 6) Top 10% Hikers’ Analysis
with tabs[5]:
    st.header("🚩 Top 10% Hikers’ Analysis")
    st.markdown("""
    **What you see:**  
    - Monthly counts (left) and proportions (right) for the *most engaged* 10% of hikers.

    **Trip‑planning scenario:**  
    > *Want to follow the “trailblazers”? If their joy spikes in March,  
    > consider starting then to benefit from local trail communities and events.*

    **Key insights:**  
    - Top 10% patterns often foreshadow broader trail sentiment.  
    - High fear in Phase 1 among top hikers suggests extra gear prep.  
    - Watching their joy surges can point to must‑visit trail segments.
    """)
    st.plotly_chart(get_top10_counts(selected_year), use_container_width=True)
    st.plotly_chart(get_top10_props(selected_year),  use_container_width=True)
