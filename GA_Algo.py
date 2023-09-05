import pandas as pd
import random
import math

# Load data
data = pd.ExcelFile('norm_score.xlsx')
ads_df = pd.read_excel(data, sheet_name='ads', header=0)
mods_df = pd.read_excel(data, sheet_name='mods', header=0)

# Check ad's market is in moderator's market
def is_market_match(moderator_market, ad_country, ad_queue_market):
    return ad_country in moderator_market or any(country in moderator_market for country in ad_queue_market)

# Calculate the objective value (proximity) of a solution
def calculate_proximity(solution):
    total_proximity = 0
    for moderator, allocated_ads in solution.items():
        moderator_score = mods_df.loc[mods_df['moderator'] == moderator, 'normalized_score'].values[0]
        ad_scores = [ads_df.loc[ads_df['ad_id'] == ad, 'normalized_score'].values[0] for ad in allocated_ads]
        ad_proximity = sum([abs(moderator_score - ad_score) for ad_score in ad_scores])
        total_proximity += ad_proximity
    return total_proximity

# Simulated Annealing Parameters
initial_temperature = 1000
final_temperature = 1
cooling_rate = 0.9
num_iterations = 10

# Initialization
current_solution = {moderator: [] for moderator in mods_df['moderator']}
for ad_id in ads_df['ad_id']:
    moderator = random.choice(mods_df['moderator'].tolist())
    current_solution[moderator].append(ad_id)

current_proximity = calculate_proximity(current_solution)
best_solution = current_solution
best_proximity = current_proximity

current_temperature = initial_temperature

# Simulated Annealing
while current_temperature > final_temperature:
    for _ in range(num_iterations):
        
        # Generate a neighboring solution by moving one ad to another moderator
        neighbor_solution = current_solution.copy()
        ad_to_move = random.choice(list(ads_df['ad_id']))
        current_moderator = next((moderator for moderator, ads in current_solution.items() if ad_to_move in ads), None)
        available_moderators = [moderator for moderator in mods_df['moderator'] if
                                ad_to_move in neighbor_solution[moderator]]
        new_moderator = random.choice(available_moderators)
        neighbor_solution[current_moderator].remove(ad_to_move)
        neighbor_solution[new_moderator].append(ad_to_move)
        
        # Calculate proximity of the neighboring solution
        neighbor_proximity = calculate_proximity(neighbor_solution)
        
        # Calculate change in proximity
        proximity_change = neighbor_proximity - current_proximity
        
        # Accept the neighboring solution with a probability
        if proximity_change < 0 or random.random() < math.exp(-proximity_change / current_temperature):
            current_solution = neighbor_solution
            current_proximity = neighbor_proximity
            
            # Update best solution
            if current_proximity < best_proximity:
                best_solution = current_solution
                best_proximity = current_proximity
    
    # Reduce the temperature
    current_temperature *= cooling_rate

# Save results
output_file = "allocation_results.txt"

with open(output_file, "w") as f:
    f.write("Best Solution:\n")
    for moderator, allocated_ads in best_solution.items():
        f.write(f"Moderator: {moderator}\n")
        for ad in allocated_ads:
            f.write(f"  Ad ID: {ad}\n")

print(f"Results have been saved to {output_file}")