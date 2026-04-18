# ⚙️ SEM A/B Test Analyzer (Backend API)

**Frontend Repository:** [https://github.com/thit2003/sem-analyzer-ui](https://github.com/thit2003/sem-analyzer-ui)  
**Live Application:** [https://sem-analyzer-ui.vercel.app](https://sem-analyzer-ui.vercel.app)

## Overview
This is the data processing engine and API for the SEM A/B Test Analyzer. Built with Python and FastAPI, this service handles the heavy lifting of parsing marketing data and executing statistical mathematics.

It receives raw `.csv` data from the frontend, uses Pandas to aggregate thousands of rows of ad performance data, and utilizes the `statsmodels` library to run a Two-Proportion Z-Test. This determines whether the difference in Conversion Rate between two ads is statistically significant or just random noise.

## 🚀 Features
* **In-Memory File Processing:** Parses `.csv` uploads on the fly without needing a database, ensuring fast response times and data privacy.
* **Data Aggregation:** Automatically calculates core SEM metrics including Click-Through Rate (CTR) and Conversion Rate (CVR).
* **Statistical Engine:** Evaluates P-Values to declare a definitive campaign winner.
* **RESTful Architecture:** Exposes a clean `/api/analyze` endpoint that returns formatted JSON for easy frontend consumption.

## 💻 Tech Stack
* **Framework:** FastAPI (Python)
* **Server:** Uvicorn
* **Data Science:** Pandas
* **Statistics:** Statsmodels, SciPy
* **Deployment:** Render

## 📡 API Reference

### Analyze Campaign Data
`POST /api/analyze`

**Request:** `multipart/form-data` containing a `.csv` file with columns: `Ad Name`, `Impressions`, `Clicks`, `Conversions`.

**Response (JSON):**
```json
{
  "status": "success",
  "data": {
    "performance_metrics": {
      "Ad A": {
        "Impressions": 12000,
        "Clicks": 450,
        "Conversions": 18,
        "CTR": 3.75,
        "CVR": 4.0
      }
    },
    "analysis": {
      "p_value": 0.0124,
      "is_significant": true,
      "winner": "Ad A"
    }
  }
}
🛠️ How to Run Locally
Clone the repository:

Bash
git clone [https://github.com/thit2003/sem-analyzer-api.git](https://github.com/thit2003/sem-analyzer-api.git)
cd sem-analyzer-api
Install dependencies:
It is recommended to use a virtual environment.

Bash
pip install -r requirements.txt
Run the server:

Bash
uvicorn main:app --reload
Test the API:
Navigate to http://127.0.0.1:8000/docs in your browser to use FastAPI's built-in Swagger UI and test file uploads directly.
