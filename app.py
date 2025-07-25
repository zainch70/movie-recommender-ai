# 1. IMPORTS
import pickle
import streamlit as st # type: ignore
import requests
from PIL import Image # type: ignore
from dotenv import load_dotenv # type: ignore
import os

api_key = os.getenv("TMDB_API_KEY")

# 2. PAGE CONFIG
st.set_page_config(
    page_title="WatchCraft AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. CUSTOM CSS
st.markdown("""
<style>
    /* Main styles */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Select box */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1E293B;
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-2px);
    }
    
    /* Movie cards */
    .movie-card {
        background: #1E293B;
        border-radius: 10px;
        padding: 15px;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Text styles */
    .stMarkdown h1 {
        text-align: center;
        margin-bottom: 2rem;
        font-size: 2.5rem;
        background: linear-gradient(90deg, #4F46E5, #E11D48);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Spacing */
    .spacer {
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 4. LOAD DATA
@st.cache_data
def load_data():
    movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()
movies_list = movies['title'].values

# 5. HELPER FUNCTIONS
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
    return None

def recommend(movie_title, num_recommendations=5):
    try:
        index = movies[movies['title'] == movie_title].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movies = []
        recommended_posters = []
        
        for i in distances[1:num_recommendations+1]:  # Now uses the parameter
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_posters.append(poster)
                recommended_movies.append(movies.iloc[i[0]].title)
                
        return recommended_movies, recommended_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []

# 6. SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h2 style='color: #4F46E5;'>WatchCraft AI</h2>
        <p style='color: #94A3B8;'>Your personal movie curator</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 Preferences")
    num_recommendations = st.slider("Number of recommendations", 3, 10, 5)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    <p style='color: #94A3B8; font-size: 0.9rem;'>
        WatchCraft AI uses machine learning to analyze movies and find perfect matches based on your preferences.
    </p>
    """, unsafe_allow_html=True)

# 7. MAIN CONTENT
st.markdown("""
<h1>
    <span style='background: linear-gradient(90deg, #4F46E5, #E11D48); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        Movie Recommendation Engine
    </span>
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: #94A3B8; font-size: 1.1rem; margin-bottom: 40px;'>
    Discover your next favorite movie with our AI-powered recommendation system
</p>
""", unsafe_allow_html=True)

# Hide Streamlit's default label and insert custom-styled label
st.markdown("""
<style>
    /* Hide default label of selectbox */
    div[data-testid="stSelectbox"] > label {
        display: none;
    }

    /* Custom label style */
    .custom-label {
        font-size: 1.1rem;
        font-weight: 500;
        color: #FAFAFA;
        margin-bottom: 0.3rem;
        display: block;
    }
</style>

<label class="custom-label">🔍 Search or select a movie</label>
""", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Search or select a movie", 
    movies_list,
    label_visibility="collapsed" 
)

if st.button('🎬 Get Recommendations', type='primary'):
    with st.spinner('Analyzing thousands of movies to find your perfect matches...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, num_recommendations)
        
        if recommended_movie_names:
            st.markdown("---")
            st.markdown(f"""
            <h3 style='color: #FFFFFF; margin-bottom: 30px;'>
                Because you liked <span style='color: #4F46E5;'>{selected_movie}</span>, you might enjoy:
            </h3>
            """, unsafe_allow_html=True)
            
            cols = st.columns(len(recommended_movie_names))
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                    <div class='movie-card'>
                        <img src='{recommended_movie_posters[i]}' style='width: 100%; border-radius: 8px; margin-bottom: 12px;' alt='{recommended_movie_names[i]}'>
                        <h4 style='color: #FFFFFF; margin: 0;'>{recommended_movie_names[i]}</h4>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Couldn't generate recommendations for this movie. Please try another selection.")