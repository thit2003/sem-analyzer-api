from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import io

# Initialize the application
app = FastAPI(title="SEM A/B Test Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_ab_test(file: UploadFile = File(...)):
    # Security check: Ensure the user uploaded a CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
        
    try:
        # 1. Read the uploaded file into memory
        contents = await file.read()
        
        # Pandas expects a file path, but we have raw bytes in memory.
        # We wrap it in io.BytesIO() to trick Pandas into reading it like a file.
        df = pd.read_csv(io.BytesIO(contents))
        
        # 2. Run the Phase 1 Aggregation Logic
        metrics = df.groupby('Ad Name')[['Impressions', 'Clicks', 'Conversions']].sum()
        metrics['CTR'] = (metrics['Clicks'] / metrics['Impressions']) * 100
        metrics['CVR'] = (metrics['Conversions'] / metrics['Clicks']) * 100
        
        # 3. Run the Statistical Test
        conversions = metrics['Conversions'].values
        clicks = metrics['Clicks'].values
        ad_names = metrics.index.tolist()
        
        if len(ad_names) != 2:
            raise HTTPException(status_code=400, detail="The dataset must contain exactly two ad variations.")
            
        stat, p_value = proportions_ztest(count=conversions, nobs=clicks)
        
        # Standard marketing significance threshold (95%)
        is_significant = bool(p_value < 0.05)
        
        winner_name = None
        if is_significant:
            winner_idx = metrics['CVR'].argmax()
            winner_name = ad_names[winner_idx]
            
        # 4. Return the data as a Python dictionary
        # FastAPI will automatically serialize this into clean JSON for your React frontend
        return {
            "status": "success",
            "data": {
                # orient="index" formats the Pandas dataframe nicely for JSON
                "performance_metrics": metrics.to_dict(orient="index"),
                "analysis": {
                    "p_value": round(p_value, 4),
                    "is_significant": is_significant,
                    "winner": winner_name
                }
            }
        }
        
    except Exception as e:
        # Catch any parsing errors and return a clean 500 error
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")