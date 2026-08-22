# GlobeTrotter — Intelligent Personalized Travel Planning Portal

GlobeTrotter is a production-grade, collaborative travel planning platform designed to help travelers discover destinations across India, build optimized day-wise itineraries, forecast travel costs using Machine Learning, and visualize route logs. 

Originally built matching the Odoo **GlobeTrotter** hackathon specification, this project has been upgraded into a premium portfolio product equipped with advanced NLP algorithms, regression model pipelines, live APIs, and geographic mapping modules.

---

## 🌟 Key Features

### 1. Core Platform Features (PDF Specifications)
* **Secure Authentication**: User sign-in, registration, profile details edit, and password reset workflows.
* **Traveler Profiles & Wishlists**: Custom travel profile preferences (budget levels, target seasons, travel themes) and interactive bookmarks.
* **Itinerary Sharing & Cloning**: Sharable read-only public URLs and one-click trip copying/cloning.
* **Interactive Timeline View**: Day-wise summaries mapping morning, afternoon, and evening slots.
* **Explore Catalogues**: Complete search directories for Indian destinations and tourist activities.

### 2. Extraordinary Upgrades (NLP, Machine Learning & Geospatial)
* **ML Cost Predictor (scikit-learn)**: A dedicated machine learning service ([budget_predictor.py](TravelPlanner/services/ml/budget_predictor.py)) that trains and compares **three regression models** (Linear Regression, Random Forest, and Decision Tree Regressor) on historical package rates. It registers the best-performing model based on $R^2$, MAE, and RMSE metrics, exposing model diagnostics inside the Django Admin.
* **Hybrid Destination Recommender**: Merges content-based filtering NLP (**TF-IDF Vectors + Cosine Similarity** on descriptions and tags) with rule-based scoring weights. Provides percentage accuracy scores and explainability logs (e.g., why a destination matches a user profile constraint).
* **Weather-Aware Itinerary Optimizer**: Spatially clusters sightseeing spots to minimize transit times, enforces a strict 8-hour daily limit to prevent traveler fatigue, and pulls live forecasts from the **OpenWeather API** to reorder activities (e.g., shifting outdoor sights to cooler morning slots or rescheduling them if rain is forecasted).
* **Leaflet & OpenStreetMap Integration**:
  * Displays cluster maps for catalog exploration.
  * Draws interactive 5 km radius overlay rings to help travelers see what else is nearby.
  * Computes Haversine distances and travel times, tracing daily route paths (polylines) on the trip itinerary page.

---

## 🛠️ Technology Stack

* **Backend**: Django 5.2 (Python)
* **Machine Learning & NLP**: Scikit-Learn, Numpy, Joblib
* **Frontend mapping**: Leaflet.js, OpenStreetMap
* **UI styling**: Bootstrap 5, FontAwesome (Dark Premium theme overrides)
* **Database**: SQLite (Production-ready relational schemas)
* **External APIs**: OpenWeather API

---

## 📂 Project Structure

```text
GlobeTrotter/
├── TravelPlanner/           # Main Django Project Source
│   ├── TravelPlanner/       # Configuration, main URLs, settings
│   ├── accounts/            # Authentication, user profiles & wishlist
│   ├── destinations/        # Destinations registry, AI recommendation views
│   ├── attractions/         # Activities, timing, entry fees
│   ├── trips/               # Trip model, timelines, day batch editors
│   ├── packages/            # Tour packages
│   ├── services/            
│   │   └── ml/              # Machine Learning algorithms
│   │       ├── budget_predictor.py      # Regression pipeline
│   │       └── itinerary_optimizer.py   # Spatially-aware reordering
│   ├── static/              # CSS, assets, and JS maps modules
│   └── templates/           # Premium dark-theme templates
├── README.md                # System documentation
└── requirements.txt         # Package dependencies
```

---

## 🚀 Setup and Installation

### 1. Prerequisites
Ensure you have **Python 3.10+** and `pip` installed.

### 2. Clone the Repository
```bash
git clone https://github.com/dharmikthakkar/GlobeTrotter.git
cd GlobeTrotter
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Database Setup
Run migrations to populate the SQLite schema:
```bash
python TravelPlanner/manage.py migrate
```

### 5. Import Sample Catalog Data
Seed the database with destinations, attractions, and packages:
```bash
python TravelPlanner/manage.py seed_data
```

### 6. Train the Machine Learning Predictor
Train the cost prediction models and save the best-performing pipeline:
```bash
python TravelPlanner/manage.py train_predictor
```
*Note: This command runs the scikit-learn pipeline, exports `trained_model.pkl`, `scaler.pkl`, and `encoder.pkl`, and logs metrics to `model_metrics.json`.*

---

## 🖥️ Running the Application

Start the local Django server:
```bash
python TravelPlanner/manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/`.

To inspect ML training diagnostics, login to the Django Admin at `http://127.0.0.1:8000/admin/`.

---

## 🧪 Running Tests
Verify database constraints and optimization calculations:
```bash
python TravelPlanner/manage.py test
```
