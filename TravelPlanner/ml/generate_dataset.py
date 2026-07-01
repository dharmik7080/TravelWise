import os
import pandas as pd
import numpy as np

def generate_data():
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(ml_dir)
    
    dest_file = os.path.join(project_dir, 'destinations.csv')
    pkg_file = os.path.join(project_dir, 'packages.csv')
    
    # 1. Read real destinations to get real average cost profiles
    if os.path.exists(dest_file):
        dest_df = pd.read_csv(dest_file)
        destinations = dest_df['destination_name'].tolist()
        cost_map = dict(zip(dest_df['destination_name'], dest_df['average_cost_per_day']))
    else:
        # Fallback values
        destinations = ['Srinagar', 'Gulmarg', 'Pahalgam', 'Leh', 'Manali', 'Shimla', 'Jaipur', 'Udaipur']
        cost_map = {d: 3000.0 for d in destinations}

    # 2. Package Type choices from Package model values
    if os.path.exists(pkg_file):
        pkg_df = pd.read_csv(pkg_file)
        package_types = pkg_df['package_type'].dropna().unique().tolist()
    else:
        package_types = ['Budget', 'Standard', 'Luxury']
        
    seasons = ['Summer', 'Winter', 'Monsoon', 'Spring', 'Autumn']
    
    # Seed for deterministic generation
    np.random.seed(42)
    
    n_samples = 4000
    data = []
    
    for _ in range(n_samples):
        dest = np.random.choice(destinations)
        base_cost_per_day = cost_map.get(dest, 3000.0)
        
        days = int(np.random.randint(1, 15))
        travelers = int(np.random.randint(1, 9))
        pkg = np.random.choice(package_types)
        season = np.random.choice(seasons)
        
        # Traveler Factor
        if travelers == 1:
            traveler_factor = 1.0
        elif travelers == 2:
            traveler_factor = 1.6
        elif travelers == 3:
            traveler_factor = 2.2
        elif travelers == 4:
            traveler_factor = 2.7
        else:
            traveler_factor = 1.0 + 0.5 * travelers
            
        # Package Factor
        if pkg == 'Budget':
            package_factor = 0.75
        elif pkg == 'Luxury':
            package_factor = 1.60
        else:
            package_factor = 1.00
            
        # Season Factor
        if season in ['Winter', 'Summer']:
            season_factor = 1.20
        elif season == 'Monsoon':
            season_factor = 0.80
        else:
            season_factor = 1.00
            
        # Cost Formula
        base_trip_cost = base_cost_per_day * days
        cost = base_trip_cost * traveler_factor * package_factor * season_factor
        
        # Add a small realistic noise (up to +/- 5% of cost)
        noise = np.random.normal(0, cost * 0.02)
        cost_estimated = round(cost + noise, 2)
        
        data.append({
            'Destination': dest,
            'Number of Travelers': travelers,
            'Number of Days': days,
            'Package Type': pkg,
            'Season': season,
            'Estimated Cost': max(100.0, cost_estimated)  # ensure positive
        })
        
    df = pd.DataFrame(data)
    
    # Save to ml/datasets/trip_cost_dataset.csv
    datasets_dir = os.path.join(ml_dir, 'datasets')
    os.makedirs(datasets_dir, exist_ok=True)
    out_file = os.path.join(datasets_dir, 'trip_cost_dataset.csv')
    df.to_csv(out_file, index=False)
    print(f"Dataset successfully saved to: {out_file} (Shape: {df.shape})")

if __name__ == '__main__':
    generate_data()
