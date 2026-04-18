import csv
import random
from datetime import datetime, timedelta

def generate_fake_ads_data(filename="mock_google_ads_data5.csv", days=400):
    # These headers mimic a standard Google Ads report export
    headers = ["Date", "Campaign", "Ad Group", "Ad Name", "Impressions", "Clicks", "Conversions", "Cost"]
    
    # We define the "true" performance metrics for our A/B test variations
    # Notice that Variant B has slightly higher ranges, making it the mathematical "winner"
    ad_variants = {
        "Control Ad (Version A)": {
            "ctr_range": (0.055, 0.075), # 1.5% to 3.5% CTR
            "cvr_range": (0.080, 0.110), # 4.0% to 7.0% CVR
            "cpc_range": (1.50, 3.00)    # Cost Per Click between $1.50 and $3.00
        },
        "Variant Ad (Version B)": {
            "ctr_range": (0.060, 0.085), # 2.0% to 4.5% CTR
            "cvr_range": (0.100, 0.130), # 6.0% to 9.0% CVR
            "cpc_range": (1.20, 2.80)    # Slightly cheaper Cost Per Click
        }
    }
    
    start_date = datetime.now() - timedelta(days=days)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        # Generate data for each day in the specified range
        for day_offset in range(days):
            current_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            
            for ad_name, metrics in ad_variants.items():
                # 1. Start with a randomized number of impressions
                impressions = random.randint(800, 3500)
                
                # 2. Derive clicks using a randomized CTR within the ad's specific range
                ctr = random.uniform(*metrics["ctr_range"])
                clicks = int(impressions * ctr)
                
                # 3. Derive conversions using a randomized CVR within the ad's specific range
                cvr = random.uniform(*metrics["cvr_range"])
                conversions = int(clicks * cvr)
                
                # 4. Calculate total cost for the day based on CPC
                cpc = random.uniform(*metrics["cpc_range"])
                cost = round(clicks * cpc, 2)
                
                # Write the row to the CSV
                writer.writerow([
                    current_date, 
                    "Q3_Software_Promo", 
                    "Competitor_Keywords", 
                    ad_name, 
                    impressions, 
                    clicks, 
                    conversions, 
                    cost
                ])
                
    print(f"Success! Generated '{filename}' with {days * len(ad_variants)} rows of realistic SEM data.")

if __name__ == "__main__":
    # You can change the number of days to generate a larger or smaller dataset
    generate_fake_ads_data(days=800)