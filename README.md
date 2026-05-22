# 👗 Women's Clothing Reviews Dashboard

An interactive **Dash web application** for analyzing customer reviews, ratings, and product behavior in an e-commerce clothing dataset.

This project uses a **modular, deployable architecture** with separate page files and utilities - perfect for scalability and team collaboration.

---

## 🎯 Quick Start

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:8050
   ```

---

## 🚀 Features

- **Overview**: Key metrics (total reviews, avg rating, recommendation rate, customer age)
- **Customer Behavior**: Age analysis, feedback distribution, recommendation patterns
- **Product Insights**: Department & product performance, top reviewed items
- **Correlations & Trends**: Correlation heatmaps, trend vs non-trend analysis
- **Interactive**: Real-time filtering, responsive charts, multi-page navigation

---

## 📊 Tech Stack

- Python 3.x
- **Dash** (web framework)
- **Plotly** (interactive visualizations)
- **Pandas** & **NumPy** (data processing)
- **Dash Bootstrap Components** (styling)

---

## 📁 Project Structure

```
TestProject/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── PROJECT_STRUCTURE.md           # Detailed documentation
│
├── pages/                         # Dashboard pages
│   ├── overview.py               # Overview & KPIs
│   ├── behavior.py               # Customer behavior analysis
│   ├── products.py               # Product insights
│   └── trends.py                 # Correlations & trends
│
├── utils/                        # Shared utilities
│   ├── data_loader.py           # Data loading & preprocessing
│   └── navbar.py                # Navigation component
│
├── data/                         # Data directory
│   └── Womens Clothing E-Commerce Reviews.csv
│
├── assets/                       # Static files (CSS, images)
├── EDA.ipynb                     # Exploratory analysis notebook
├── StoryAndInsights.ipynb        # Insights notebook
└── README.md                     # This file
```

---

## 🏗️ Architecture Highlights

### Modular Design
- **Pages**: Each dashboard page is a self-contained module with layout and callbacks
- **Utils**: Reusable functions for data loading, navigation, and common tasks
- **Separation of Concerns**: Data logic separate from UI and visualization logic

### Scalability
- Add new pages without modifying core application logic
- Easy to extend with new features or data sources
- Team members can work on different pages in parallel

### Deployment Ready
- Standard Python project structure
- Compatible with Gunicorn, Heroku, Docker, AWS, and other platforms
- All dependencies listed in `requirements.txt`

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Steps

1. **Clone/navigate to project:**
   ```bash
   cd TestProject
   ```

2. **Create/activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

5. **Access the dashboard:**
   Open http://localhost:8050 in your web browser

---

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -b 0.0.0.0:8050 --workers 4 app:server
```

Note: Add to `app.py`:
```python
server = app.server  # Expose server for deployment
```

### Docker
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--workers", "4", "app:server"]
```

2. Build and run:
```bash
docker build -t dashboard .
docker run -p 8050:8050 dashboard
```

### Heroku
1. Create `Procfile`:
```
web: gunicorn -b 0.0.0.0:$PORT --workers 4 app:server
```

2. Deploy:
```bash
git push heroku main
```

### AWS / Azure / Google Cloud
Use standard Python WSGI deployment with the gunicorn command above, or containerize with Docker.

---

## 📊 Dashboard Pages

### 1. Overview
- **KPI Cards**: Total reviews, average rating, recommendation percentage, average age
- **Filters**: Department dropdown, rating range slider
- **Charts**: Rating distribution, recommendation probability, department averages

### 2. Customer Behavior
- **Filters**: Clothing class, recommended items only checkbox
- **Charts**: Age vs rating analysis, feedback distribution, recommendations by age group

### 3. Product Insights
- **Filters**: Department selection, top N products slider
- **Charts**: Average ratings by department, average ratings by class, top reviewed products

### 4. Correlations & Trends
- **Correlation Matrix**: Heatmap of key behavioral features
- **Trend Analysis**: Comparison of trend vs non-trend products across multiple metrics

---

## 🔧 Extending the Project

### Adding a New Page

1. Create `pages/new_page.py`:
```python
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

def get_new_page_layout(df):
    return dbc.Container([...])

def register_new_page_callbacks(app, df):
    @app.callback(...)
    def update_chart(...):
        ...
```

2. Update `app.py`:
```python
from pages.new_page import get_new_page_layout, register_new_page_callbacks

page_new = get_new_page_layout(df)

# In display_page callback
if pathname == '/new':
    return page_new

# Register callbacks
register_new_page_callbacks(app, df)
```

3. Update navbar in `utils/navbar.py` to include new link

---

## 📝 Notes

- Data file should be in `data/` directory
- Static assets (CSS, images) go in `assets/` directory
- Notebooks (EDA.ipynb, StoryAndInsights.ipynb) are for analysis and documentation
- Original monolithic version saved as `app_old.py` for reference

---

## 📄 License

This project uses publicly available data for educational purposes.

---

## 💡 Future Enhancements

- [ ] User authentication
- [ ] Data export functionality
- [ ] Advanced filtering options
- [ ] Real-time data updates
- [ ] Custom date range filtering
- [ ] PDF report generation
- [ ] Machine learning predictions