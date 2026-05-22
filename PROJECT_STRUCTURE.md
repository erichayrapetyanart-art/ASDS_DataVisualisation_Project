# Project Structure

This dashboard has been reorganized into a modular, deployable structure.

## Directory Layout

```
TestProject/
├── app.py                          # Main entry point
├── app_old.py                      # Original monolithic version (backup)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── data/                           # Data files
│   └── Womens Clothing E-Commerce Reviews.csv
├── assets/                         # Static assets (CSS, images, etc.)
├── pages/                          # Page modules
│   ├── __init__.py
│   ├── overview.py                 # Overview dashboard page
│   ├── behavior.py                 # Customer behavior analysis page
│   ├── products.py                 # Product insights page
│   └── trends.py                   # Correlations & trends page
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── data_loader.py             # Data loading & preparation
│   └── navbar.py                  # Navigation bar component
├── EDA.ipynb                       # Exploratory data analysis notebook
├── StoryAndInsights.ipynb          # Story and insights notebook
└── venv/                           # Virtual environment
```

## Module Descriptions

### `app.py`
**Main application entry point.** Orchestrates the entire Dash application:
- Loads and prepares data
- Creates the NavBar and page layouts
- Sets up URL routing
- Registers all callbacks
- Starts the development/production server

### `pages/` Directory
Each module represents a different dashboard page with its own layout and callbacks:

- **`overview.py`**: Key metrics and overview charts (KPI cards, rating distribution, recommendations)
- **`behavior.py`**: Customer behavior analysis (age vs rating, feedback distribution, recommendations by age group)
- **`products.py`**: Product and department performance insights (average ratings, top reviewed items)
- **`trends.py`**: Correlation analysis and trend vs non-trend product comparison

Each page module contains:
- `get_<page>_layout(df)`: Function that returns the Dash layout
- `register_<page>_callbacks(app, df)`: Function that registers all page-specific callbacks

### `utils/` Directory
Shared utilities and helper functions:

- **`data_loader.py`**: 
  - `load_and_prepare_data()`: Loads CSV and performs feature engineering
  
- **`navbar.py`**: 
  - `create_navbar()`: Creates the navigation bar component

## How to Run

1. **Activate virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies (if needed):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the dashboard:**
   Open your browser to `http://localhost:8050`

## Deployment

This modular structure is deployment-ready:

### Using Gunicorn (Production)
```bash
gunicorn -b 0.0.0.0:8050 app:server
```

Note: Update `app.py` to expose the server object:
```python
server = app.server
```

### Using Heroku
1. Add `Procfile`:
   ```
   web: gunicorn app:server
   ```

2. Deploy with git push

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
```

## Benefits of This Structure

✅ **Modularity**: Each page is independent and easy to maintain
✅ **Scalability**: Easy to add new pages without cluttering core app
✅ **Reusability**: Utilities can be imported and used across pages
✅ **Testability**: Individual modules can be tested separately
✅ **Deployment**: Standard structure recognized by deployment platforms
✅ **Collaboration**: Team members can work on different pages simultaneously

## Adding New Pages

1. Create new file in `pages/` directory (e.g., `pages/new_page.py`)
2. Define layout function: `get_new_page_layout(df)`
3. Define callback registration: `register_new_page_callbacks(app, df)`
4. Import and register in `app.py`
5. Update navbar in `utils/navbar.py`

Example:
```python
# In app.py
from pages.new_page import get_new_page_layout, register_new_page_callbacks

page_new = get_new_page_layout(df)

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/new':
        return page_new
    # ...

register_new_page_callbacks(app, df)
```
