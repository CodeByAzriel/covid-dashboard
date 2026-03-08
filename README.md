# 🌍 COVID-19 Interactive Dashboard

This is a **COVID-19 dashboard** built with **Streamlit, Pandas, and Plotly**.  
It shows current COVID-19 statistics for any country, historical trends, and top 10 countries by total and active cases.

---

## 📸 Screenshot

![Dashboard Screenshot](screenshots/dashboard1.png)

---

## 🚀 How to Run Locally

1. Clone the repository:

```bash
# Clone the repository
git clone https://github.com/CodeByAzriel/covid-dashboard.git
cd covid-dashboard

# Create a virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Open your browser at http://localhost:8501 to see the dashboard
