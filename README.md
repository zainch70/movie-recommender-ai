# 🎬 Movie Recommender System

This project is a movie recommendation system built with Python and Streamlit. It uses the TMDB (The Movie Database) API to fetch movie posters and metadata.

## 📦 Features

- Recommend similar movies using content-based filtering.
- View movie posters using TMDB API.
- Simple web interface with Streamlit.

---

## 🛠️ Setup Instructions

### Download Pre-trained artifacts folder from google drive first
Due to size limits on GitHub, download the `artifacts/` file from https://drive.google.com/drive/folders/1OBFmn9W0DEcKJoh0H9b6O_HOVkptKB3C?usp=drive_link
and place in just as app.py located before running the app.


### 1. Clone the repository

```bash
git clone https://github.com/zainch70/movie-recommender-ai.git
cd movie-recommender-ai
```

### 2. Create and activate virtual environment (optional but recommended)

```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the root directory and add your TMDB API key like this:

```env
TMDB_API_KEY=your_actual_tmdb_api_key_here
```

⚠️ Do NOT wrap the API key in quotes.

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

---

## 📄 File Structure

```
.
├── app.py                  # Main Streamlit app
├── data/                   # Movie data files
├── env/                    # Virtual environment (do not upload)
├── src/                    # Your source code
├── .env                    # Contains TMDB_API_KEY (do not upload to GitHub)
├── .gitignore              # Ensures .env and env/ are ignored
├── requirements.txt        # Required packages
└── README.md               # This file
```
