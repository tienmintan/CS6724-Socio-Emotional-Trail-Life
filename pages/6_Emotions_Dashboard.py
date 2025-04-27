import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------
# 1) PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
     layout="wide",
     initial_sidebar_state="expanded"
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
      .footer {
        text-align: left-align;
        font-size: 0.8rem;
        color: #666666;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #cccccc;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------
# 3) PAGE TITLE & TABS
# ----------------------------------------------------------------
st.title("🏞️ Hikers' Emotions Visualization Dashboard")
st.header("Select a year located on the side bar and explore our analysis of different emotions happening on the Appalachian Trail!")
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
file_path_top_10            = '2025-03-25_Top10Pct.xlsx'
file_path_emotions          = 'Emotions Visualization Chart.xlsx'
file_path_top_10_extraction = 'Top Ten Percent Data Extraction.xlsx'

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
# 9) TAB AND FOOTER CONTENT
# ----------------------------------------------------------------

def draw_footer():
    st.markdown("---")
    st.markdown(
        "<div class='footer'>"
        "Data source: Trail Journal Platform (trailjournals.com). "
        "Dataset: cleaned CSV of journal entries annotated with emotions "
        "(joy, surprise, disgust, anger, sadness, fear)."
        "</div>",
        unsafe_allow_html=True
    )

# 1) Individual Journeys
with tabs[0]:
    st.header("👣 Individual Journeys (Anonymized)")
    col1, col2 = st.columns([2, 1])
    with col1:
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
    
    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("""
            - **What the Graph Shows:** A timeline tracking Hiker 11’s daily emotional fluctuations during their 2022 Appalachian Trail hike, using journal data..
            - **X-axis (Date):** Represents the hiker’s progression over time, from June through October.
            - **Y-axis (Emotion):** Plots emotion categories, ranging from high-energy positive emotions (e.g., surprise) to low-energy negative emotions (e.g., fear).
            - **Dashed Lines:** Indicate three key trail segments — early hike, mid-hike, and final stretch — to contextualize emotional highs/lows within the trail journey.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Early Hike Caution:** Emotion logs reveal more fear and uncertainty in the early section of the hike, a common trend that could suggest mental preparation challenges.
            - **Mid-Hike Neutrality or Gaps:** Some hikers, like Hiker 11, may experience emotional flatlines or logging fatigue mid-hike, possibly due to physical weariness or lack of journaling motivation.
            - **End-Phase Silence or Anticipation:** Emotional logs taper off near the final leg, which could indicate exhaustion, determination, or fewer reflective entries.
            """)
            
            st.subheader("Use Cases:")
            st.markdown("""
            - **Trail Planning:** Hikers can use emotional trend data to prepare for psychological slumps, adding rest days or treats during low points (e.g., Phase 2 dips).
            - **Gear & Supply Strategy:** Pack extra comfort food or motivational gear (music, photos, etc.) during expected stress periods.
            - **Hiker Support Systems:** Friends or family tracking a hiker’s journey can offer targeted encouragement or check-ins during likely emotional downturns.
            - **Mental Health Checkpoints:** Trail organizations can use emotional data to identify which sections of the trail are most emotionally taxing and provide support resources accordingly.
            """)
     draw_footer()


# 2) Monthly Dominant Emotions
with tabs[1]:
    st.header("📊 Monthly Dominant Emotions")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **What you see:**  
        A bar for each month showing the *single* most common emotion among all hikers.

        **Trip‑planning scenario:**  
        > *You want to start in May but are nervous about unpredictable weather.  
        > May’s dominant emotion is fear (gray)—so plan for rain‑ready gear and  
        > consider an earlier start in April when joy was higher.*

        **Key insights:**  
        - Weather‑linked fear spikes in spring/fall.  
        - Summer months show consistent joy — ideal for first‑timers.  
        - 2022 dips suggest lower trail traffic — quieter, but less on‑trail support.
        """)
        st.plotly_chart(get_monthly_emotion_trends(selected_year), use_container_width=True)
    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("""
            - **What the Graph Shows:** A bar chart displaying the most common emotion among hikers for each month in 2022. Bars are color-coded by emotion and sized by frequency.
            - **X-axis (Date):** Each month from March to November 2022.
            - **Y-axis (Emotion Count):** Number of times the dominant emotion was logged by hikers in that month.
            - **Color Coding:** Yellow = Joy, Green = Surprise, Gray = Fear, Light Blue = Sadness.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Fear and Sadness Bracket the Season:** These emotions are most common at the start (spring) and end (fall) of the hiking season, possibly due to cold or unpredictable weather.
            - **Mid-Summer Joy Peak:** Joy dominates during June and July — ideal for first-time hikers looking for a more emotionally uplifting trail experience.
            - **May Spike in Fear:** May 2022 had the highest fear count, suggesting hikers faced early weather, gear, or trail-readiness concerns.
            - **Lower Counts Across 2022:** Emotion counts suggest fewer journal entries and possibly fewer hikers overall, which may mean quieter trails with less peer support.
            """)

            st.subheader("Use Cases:")
            st.markdown("""
            - **Trip Timing Optimization:** Plan hikes for joyful months like July to enhance morale and overall experience.
            - **Packing for Emotional Resilience:** Include rain-ready gear and comfort supplies in spring/fall when fear and sadness are more common.
            - **Mental Preparedness:** Anticipate emotional dips in colder months and prep strategies like journaling prompts or mindfulness routines.
            - **Trail Resource Planning:** Trail organizations can use monthly emotion trends to time support services (e.g., morale boosts or check-ins) where they’re most needed.
            """)
     draw_footer()

# 3) Overall Emotion Proportions
with tabs[2]:
    st.header("📈 Overall Emotion Proportions")
    col1, col2 = st.columns([2, 1])
    with col1:
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

    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("""
            - **What the Graph Shows:** A bar chart summarizing the proportion of each recorded emotion across the entire year based on hikers’ journal entries.
            - **X-axis (Emotion):** Lists the six emotions tracked: fear, joy, surprise, anger, sadness, and disgust.
            - **Y-axis (Proportion):** Represents the percentage share of each emotion relative to the total emotional records for the year.
            - **Color Coding:** Each bar is color-coded by emotion, with yellow for joy, gray for fear, green for surprise, blue tones for anger and sadness, and orange for disgust.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Fear and Joy Dominate Equally:** Each accounts for just under 30% of all recorded emotions, indicating a trail experience that’s both thrilling and mentally demanding.
            - **Surprise is a Strong Third:** At 15.65%, surprise suggests that unexpected moments — whether positive or challenging — are a frequent part of the trail.
            - **Low Negative Emotion Proportions:** Anger (11.56%), sadness (8.84%), and especially disgust (4.08%) are relatively rare, suggesting overall positive sentiment among hikers.
            - **Community Value Highlighted:** The balance of joy and fear indicates the importance of support systems, morale events, and social interaction for hikers.
            """)

            st.subheader("Use Cases:")
            st.markdown("""
            - **Group vs Solo Hike Planning:** If fear is high and joy is low, consider joining a group to boost emotional resilience — especially for first-timers.
            - **Support Strategies:** Trail organizations can design initiatives like morale boosts, mid-trail celebrations, or check-ins to balance out fear spikes.
            - **Mental Health Monitoring:** Use emotional proportions to benchmark against past years and assess the emotional well-being of the hiking community.
            - **Onboarding New Hikers:** Communicate realistic emotional expectations (e.g., highs and lows are common) to better prepare new hikers mentally.
            """)
     draw_footer()

# 4) Emotions Proportion Over Time
with tabs[3]:
    st.header("⏳ Emotions Proportion Over Time")
    col1, col2 = st.columns([2, 1])
    with col1:
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
    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("""
            - **What the Graph Shows:** A stacked bar chart illustrating the month-by-month mix of hiker emotions throughout the year.
            - **X-axis (Date):** Represents each month in 2022.
            - **Y-axis (Proportion):** Displays the percentage of total emotional records attributed to each emotion within the month.
            - **Color Coding:** Each emotion has a distinct color: joy (yellow), fear (gray), surprise (green), anger (blue), sadness (light blue), and disgust (orange).
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Seasonal Patterns:** Joy increases during summer (June–September), while fear and sadness are more prevalent in colder months like January and November.
            - **Surprise Peaks:** Noticeable spikes in surprise appear in April, July, and September — possibly linked to events like wildlife sightings or unexpected trail moments.
            - **Winter Fatigue Indicators:** January and November show higher shares of fear, anger, and sadness, suggesting a need for increased motivation and warmth during cold months.
            - **Consistent Emotional Diversity:** Most months display a varied mix of emotions, reinforcing the mental complexity of long-distance hiking.
            """)

            st.subheader("Use Cases:")
            st.markdown("""
            - **Trail Readiness Planning:** Hikers can select months with high joy and low fear (e.g., June or September) for more emotionally rewarding trips.
            - **Mental Health Strategy:** Use this emotional map to align support tactics (like guided meditations, comfort food drops, or rest days) with known emotional trends.
            - **Seasonal Event Planning:** Trail coordinators can align celebrations or wellness events with surprise or joy peaks for maximum morale impact.
            - **Gear Optimization:** Prepare for fear-heavy months with extra protection (rain gear, comfort items) and travel in groups during emotionally challenging periods.
            """)
     draw_footer()


# 5) Emotions Count Over Time
with tabs[4]:
    st.header("🔢 Emotions Count Over Time")
    col1, col2 = st.columns([2, 1])
    with col1:
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
    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("""
            - **What the Graph Shows:** A stacked bar chart showing the raw number of journal entries tagged with each emotion by month in 2022.
            - **X-axis (Date):** Monthly timeline from January through November 2022.
            - **Y-axis (Emotion Count):** Total number of emotion-labeled entries recorded in each month.
            - **Color Coding:** Each emotion is shown in a different color — joy (yellow), fear (gray), surprise (green), sadness (light blue), anger (blue), and disgust (orange).
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Summer Peaks (May–September):** Emotion activity surges in these months, with July showing the highest count (~500), suggesting peak trail usage and engagement.
            - **Winter Drop-Off:** Minimal entries in colder months like January and November reflect lower hiker turnout or fewer journal logs.
            - **May Stands Out:** With a particularly high balance of all emotions, May may offer a rich emotional experience but also more crowding.
            - **Solitude Indicators:** February and November, with just 10 and 7 entries respectively, indicate ideal months for hikers seeking solitude.
            """)

            st.subheader("Use Cases:")
            st.markdown("""
            - **Trip Timing for Solitude Seekers:** Plan for off-peak months like February or November to enjoy a quieter trail and less crowded shelters.
            - **Expect Crowds in Summer:** Use high emotion counts in June–August as indicators of busy periods for campsites and high social interaction.
            - **Trail Event Planning:** Trail managers can time events or wellness programs during months with peak emotional activity to reach more hikers.
            - **Logistics Planning:** Higher entry counts may correlate with the need for additional resources (e.g., resupply points, mental health support) during busier periods.
            """)
     draw_footer()



# 6) Top 10% Hikers’ Analysis
with tabs[5]:
    st.header("🚩 Top 10% Hikers’ Analysis")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **What you see:**  
        - Monthly counts (left) and proportions (right) for the *most engaged* 10% of hikers.
        - This means that they are the top 10% hikers who completed the most distances and reports in their hiking experience, hence they are considered the most engaged.

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
    with col2:
        with st.container(border=True):
            st.subheader("Graph Explanation:")
            st.write("""
            - **What the Graph Shows:** A stacked bar chart showing the raw monthly emotion counts for the most active 10% of hikers — those who journal the most.
            - **X-axis (Date):** Each month from March through November 2022.
            - **Y-axis (Emotion Count):** Total emotion-labeled journal entries recorded by top 10% hikers each month.
            - **Color Coding:** Joy (yellow), surprise (green), anger (blue), disgust (orange), fear (gray), and sadness (light blue) are shown as stacked segments per month.
            """)

            st.subheader("Key Insights:")
            st.markdown("""
            - **Top Hikers Set the Tone:** Emotional trends among the top 10% often anticipate broader trail sentiment and engagement.
            - **High Early-Season Fear (May):** Suggests that even experienced or active hikers feel significant pressure at the start of the hike — good reason to prepare mentally and logistically.
            - **Joy Surges in July & October:** These spikes may reflect rewarding trail segments or events worth aligning a trip around.
            - **Consistent Surprise in Summer Months:** Could correlate with wildlife, social encounters, or scenic highlights experienced by high-engagement hikers.
            """)

            st.subheader("Use Cases:")
            st.markdown("""
            - **Trailblazer-Inspired Planning:** Start your hike in sync with top hikers’ emotional highs (e.g., March joy spikes) to benefit from shared experiences and community energy.
            - **Targeted Gear Prep:** When even top hikers feel high fear in early months, it's wise to overprepare — especially with weather-resistant or comfort gear.
            - **Trail Segment Mapping:** Use peaks in joy or surprise among elite hikers to identify standout sections of the trail.
            - **Hiker Community Building:** Organize trail meetups or resource drops around periods with high emotion counts from top contributors.
            """)
     draw_footer()
