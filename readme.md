# 🍽️ Swiggy Restaurant Recommendation System

A Machine Learning based Restaurant Recommendation System built using **Python**, **Scikit-Learn**, **Pandas**, and **Streamlit**.

The application recommends restaurants based on user preferences such as **City, Cuisine, Rating, Rating Count, and Budget** using **One-Hot Encoding** and **Cosine Similarity**.

---

# 📌 Project Overview

This project demonstrates an end-to-end recommendation system that includes:

- Data Cleaning
- Data Preprocessing
- One-Hot Encoding
- Recommendation Engine
- Streamlit Web Application
- Interactive Restaurant Recommendations

The recommendation engine computes similarity using the encoded dataset and maps the results back to the original cleaned dataset for user-friendly output.

---

# 🎯 Business Problem

Finding restaurants that match a user's preferences can be difficult when thousands of restaurants are available.

This system helps users discover restaurants by recommending similar restaurants based on:

- City
- Cuisine
- Rating
- Rating Count
- Budget

---

# 🎯 Objectives

- Clean and preprocess restaurant data
- Remove duplicates and missing values
- Encode categorical features using One-Hot Encoding
- Build a similarity-based recommendation engine
- Develop an interactive Streamlit application
- Display recommendations from the cleaned dataset

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.x |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-Learn |
| Encoding | OneHotEncoder |
| Similarity | Cosine Similarity |
| Web Application | Streamlit |
| Model Serialization | Joblib |
| IDE | VS Code |

---

# 📂 Project Structure

```text
Swiggy System/
│
├── data/
│   ├── raw/
│   │     restaurants.csv
│   │
│   └── processed/
│         cleaned_data.csv
│         encoded_data.csv
│
├── models/
│      encoder.pkl
│
├── scripts/
│      data_cleaning.py
│      preprocessing.py
│      recommendation_engine.py
│
├── streamlit_app/
│      app.py
│      app_final.py
│
├── requirements.txt
│
└── README.md
```

---

# 📊 Dataset

The dataset contains restaurant information including:

- Restaurant ID
- Restaurant Name
- City
- Rating
- Rating Count
- Cost
- Cuisine
- Address

### Features Used

### Categorical Features

- City
- Cuisine

### Numerical Features

- Rating
- Rating Count
- Cost

---

# 🧹 Data Cleaning

The following preprocessing steps were performed:

- Duplicate removal
- Missing value handling
- Feature selection
- Data validation
- Clean dataset creation

Output:

```
cleaned_data.csv
```

---

# ⚙️ Data Preprocessing

Categorical features are transformed using:

- One-Hot Encoding

Numerical features retained:

- Rating
- Rating Count
- Cost

The preprocessing pipeline:

- Fits OneHotEncoder
- Saves encoder
- Creates encoded dataset
- Preserves row alignment between datasets

Outputs:

```
cleaned_data.csv

encoded_data.csv

encoder.pkl
```

---

# 🧠 Recommendation Methodology

The recommendation engine uses:

- Cosine Similarity

Workflow:

```
User Preferences

↓

One-Hot Encoding

↓

Encoded Feature Vector

↓

Cosine Similarity

↓

Top Similar Restaurants

↓

Map Results to cleaned_data.csv

↓

Display Recommendations
```

The recommendation engine filters restaurants using:

- City
- Cuisine

and compares:

- Rating
- Rating Count
- Cost

before returning the most relevant restaurants.

---

# 💻 Streamlit Application

The Streamlit application provides a user-friendly interface for restaurant discovery.

## User Inputs

- City
- Cuisine
- Minimum Rating
- Minimum Rating Count
- Maximum Budget

## Output

Displays recommended restaurants including:

- Restaurant Name
- City
- Cuisine
- Rating
- Rating Count
- Cost
- Similarity Score

---

# 🚀 How to Run the Project

## Step 1

Clone the repository

```bash
git clone <repository-url>
```

---

## Step 2

Navigate to the project

```bash
cd "Swiggy System"
```

---

## Step 3

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4

Run Data Cleaning

```bash
python scripts/data_cleaning.py
```

---

## Step 5

Run Preprocessing

```bash
python scripts/preprocessing.py
```

---

## Step 6

Run Recommendation Engine

```bash
python scripts/recommendation_engine.py
```

---

## Step 7

Launch Streamlit

```bash
streamlit run streamlit_app/app.py
```

---

# 📈 Recommendation Workflow

```
Restaurant Dataset

↓

Data Cleaning

↓

cleaned_data.csv

↓

One-Hot Encoding

↓

encoded_data.csv

↓

encoder.pkl

↓

Recommendation Engine

↓

Cosine Similarity

↓

Recommended Restaurants

↓

Streamlit Dashboard
```

---

# 📁 Project Outputs

## Data Cleaning

- cleaned_data.csv

## Data Preprocessing

- encoded_data.csv
- encoder.pkl

## Recommendation Engine

- Similarity-based recommendations
- Mapping back to cleaned dataset

## Streamlit Application

Interactive restaurant recommendation dashboard.

---

# 📊 Evaluation Criteria

The project focuses on:

- Recommendation Quality
- User Experience
- Data Alignment
- Accurate Mapping
- Reproducibility

---

# ✅ Key Features

- Duplicate Removal
- Missing Value Handling
- One-Hot Encoding
- Cosine Similarity Recommendation
- Dynamic User Inputs
- Recommendation Mapping
- Interactive Streamlit Dashboard
- Modular Python Architecture

---

# 📌 Future Enhancements

- Hybrid Recommendation System
- Content + Collaborative Filtering
- Restaurant Images
- Location-based Recommendations
- User Login
- Favorites & History
- Cloud Deployment
- API Integration
- Restaurant Search
- Advanced Recommendation Ranking

---

# 👨‍💻 Author

**Kumaaran J**

Machine Learning | Python | Streamlit | Data Analytics

---

# 📜 License

This project is developed for educational and portfolio purposes.