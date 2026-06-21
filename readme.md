# 🍽️ Swiggy Restaurant Recommendation System using Streamlit

## 📌 Project Overview

This project is a Machine Learning-based Restaurant Recommendation System built using the Swiggy restaurant dataset. The system recommends restaurants similar to a selected restaurant using Cosine Similarity and One-Hot Encoding techniques.

The application is deployed using Streamlit to provide an interactive and user-friendly interface.

---

# 🚀 Skills & Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- One-Hot Encoding
- Cosine Similarity
- Recommendation Systems
- Data Preprocessing
- Machine Learning

---

# 📂 Project Structure

```bash
Swiggy System/
│
├── data/
│   ├── raw/
│   │   └── swiggy.csv
│   │
│   └── processed/
│       ├── cleaned_data.csv
│       └── encoded_data.csv
│
├── models/
│   └── encoder.pkl
│
├── scripts/
│   ├── data_cleaning.py
│   ├── preprocessing.py
│   └── recommendation_engine.py
│
├── streamlit_app/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🎯 Problem Statement

The objective of this project is to build a restaurant recommendation system using restaurant data from Swiggy.

The system recommends restaurants based on similarities in:
- City
- Cuisine
- Rating
- Rating Count
- Cost

The recommendation engine uses:
- One-Hot Encoding
- Cosine Similarity

to identify similar restaurants.

---

# 📊 Dataset Information

### Dataset Columns

| Column Name | Description |
|---|---|
| id | Restaurant ID |
| name | Restaurant Name |
| city | Restaurant City |
| rating | Restaurant Rating |
| rating_count | Number of Ratings |
| cost | Approximate Cost |
| cuisine | Cuisine Type |
| address | Restaurant Address |

---

# ⚙️ Project Workflow

## 1️⃣ Data Cleaning

The raw Swiggy dataset contains:
- Missing values
- Duplicate rows
- Non-numeric values
- Currency symbols
- Text inconsistencies

### Cleaning Steps:
- Removed duplicates
- Handled missing values
- Cleaned rating column
- Cleaned cost column
- Standardized text columns

### Output:
```bash
data/processed/cleaned_data.csv
```

---

## 2️⃣ Data Preprocessing

### Feature Engineering
Categorical features:
- city
- cuisine

Numerical features:
- rating
- rating_count
- cost

### One-Hot Encoding
Text categories were converted into numerical vectors using OneHotEncoder.

Example:

| city |
|---|
| Chennai |
| Bangalore |

becomes:

| city_Chennai | city_Bangalore |
|---|---|
| 1 | 0 |
| 0 | 1 |

### Outputs:
```bash
data/processed/encoded_data.csv
models/encoder.pkl
```

---

## 3️⃣ Recommendation System

### Recommendation Method
This project uses:

# Cosine Similarity

Cosine Similarity compares restaurant feature vectors mathematically and identifies restaurants with similar characteristics.

### Recommendation Flow

```text
Selected Restaurant
        ↓
Fetch Restaurant Vector
        ↓
Compare Against All Restaurants
        ↓
Calculate Similarity Scores
        ↓
Sort by Highest Similarity
        ↓
Return Top Recommendations
```

---

# 🖥️ Streamlit Application

The Streamlit app allows users to:
- Select a restaurant
- Generate recommendations
- View similar restaurants interactively

### Features
- Interactive dropdown selection
- ML-powered recommendations
- Restaurant details display
- User-friendly UI

---

# 📈 Recommendation System Architecture

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Cleaned Dataset
     ↓
One-Hot Encoding
     ↓
Encoded Dataset
     ↓
Cosine Similarity
     ↓
Recommendation Engine
     ↓
Streamlit Application
```

---

# ▶️ How to Run the Project

## Step 1: Clone Repository

```bash
git clone <repository_link>
```

---

## Step 2: Install Requirements

```bash
pip install -r requirements.txt
```

---

## Step 3: Run Data Cleaning

```bash
python scripts/data_cleaning.py
```

---

## Step 4: Run Preprocessing

```bash
python scripts/preprocessing.py
```

---

## Step 5: Run Recommendation Engine

```bash
python scripts/recommendation_engine.py
```

---

## Step 6: Launch Streamlit App

```bash
streamlit run streamlit_app/app.py
```

---

# 📌 Key Learnings

- Data Cleaning & Preprocessing
- Feature Engineering
- One-Hot Encoding
- Cosine Similarity
- Recommendation Systems
- Streamlit Application Development
- Scalable ML System Design
- Memory Optimization Techniques

---

# 🔥 Challenges Faced

## Memory Explosion Problem

Initially, an all-vs-all cosine similarity matrix was attempted:

```python
cosine_similarity(encoded_df)
```

This caused:
- Extremely large memory allocation
- 164 GB RAM requirement
- System crash

### Solution
Implemented dynamic similarity computation:

```python
cosine_similarity(selected_vector, encoded_df)
```

This compares:
- One selected restaurant
- Against all restaurants

making the system scalable and memory efficient.

---

# 📊 Results

- Successfully built a recommendation engine
- Generated restaurant recommendations using cosine similarity
- Developed an interactive Streamlit web application
- Created scalable recommendation architecture

---

# 📌 Future Improvements

- Add cuisine filters
- Add city-based recommendations
- Add price range filtering
- Deploy on Streamlit Cloud
- Use FAISS for faster similarity search
- Add restaurant images
- Add NLP-based menu similarity

---

# 👨‍💻 Author

Kumaaran J

---

# 📜 License

This project is for educational and learning purposes.