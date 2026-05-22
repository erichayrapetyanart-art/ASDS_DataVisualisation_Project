# Setup Guide for New Users

This guide explains how to clone and run the Women's Clothing Reviews Dashboard on your machine.

## Prerequisites

- **Python 3.7+** (check with `python --version`)
- **Git** (check with `git --version`)
- **pip** (usually included with Python)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/erichayrapetyanart-art/ASDS_DataVisualisation_Project.git
cd ASDS_DataVisualisation_Project/TestProject
```

Or if you have SSH set up:
```bash
git clone git@github.com:erichayrapetyanart-art/ASDS_DataVisualisation_Project.git
cd ASDS_DataVisualisation_Project/TestProject
```

### 2. Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

You should see:
```
Dash is running on http://127.0.0.1:8050/
```

### 5. Open in Browser

Open your web browser and go to:
```
http://127.0.0.1:8050
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError" when running app.py

**Solution:** Make sure your virtual environment is activated:
```bash
# Check if (venv) appears in your terminal prompt
# If not, run the activation command:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Issue: "Port 8050 is already in use"

**Solution:** Kill the process using port 8050:

**On macOS/Linux:**
```bash
lsof -i :8050 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

**On Windows:**
```bash
netstat -ano | findstr :8050
taskkill /PID <PID> /F
```

Then run `python app.py` again.

### Issue: "No module named 'pandas'" or similar

**Solution:** Reinstall requirements:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Data file not found

**Solution:** Make sure you're running from the correct directory:
```bash
# You should be in the TestProject directory
pwd  # On macOS/Linux
cd  # On Windows
# Should show: .../TestProject
```

### Issue: Permission denied on macOS/Linux

**Solution:** Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

---

## Project Structure

```
TestProject/
├── app.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── PROJECT_STRUCTURE.md  # Detailed architecture
├── SETUP.md             # This file
│
├── pages/               # Dashboard pages
│   ├── overview.py
│   ├── behavior.py
│   ├── products.py
│   └── trends.py
│
├── utils/               # Utilities
│   ├── data_loader.py
│   └── navbar.py
│
├── data/                # Data directory
│   └── Womens Clothing E-Commerce Reviews.csv
│
└── assets/              # Static files (CSS, images)
```

---

## Development Workflow

### To modify the code:

1. **Make changes** to any Python files
2. **Save** (auto-refresh with debug mode on)
3. **Check browser** for changes (page auto-reloads when code changes)

### To add a new page:

1. Create `pages/your_page.py` with layout and callbacks
2. Import in `app.py`
3. Update navbar in `utils/navbar.py`
4. Add routing in `app.py`

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for details.

---

## Production Deployment

For deploying to production (Heroku, AWS, Docker, etc.):

See the **Deployment** section in [README.md](README.md)

---

## Getting Help

- Check [README.md](README.md) for feature documentation
- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture details
- Review the [original issue](#) if you have specific questions

---

## Updating Code

After the repository is updated:

```bash
git pull origin main
pip install -r requirements.txt  # In case dependencies changed
python app.py
```

---

## Notes for Team Members

✅ **What's included:**
- All required dependencies in `requirements.txt`
- Data file in `data/` directory
- Complete modular application structure
- Documentation for setup and architecture

✅ **Virtual environment:**
- Each user should create their own `venv/`
- It's excluded from git (see `.gitignore`)
- The venv is NOT shared across machines

✅ **Data:**
- Data file is included in the repository
- Located in `data/Womens Clothing E-Commerce Reviews.csv`
- Large files are OK for academic/class projects

✅ **No sensitive info:**
- No API keys, passwords, or credentials in repository
- Safe to push to public GitHub

---

## Questions or Issues?

If you encounter problems:

1. Check this Setup Guide first
2. Check the Troubleshooting section
3. Review the README for usage questions
4. Check the Project Structure documentation

Good luck! 🚀
