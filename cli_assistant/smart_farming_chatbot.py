import argparse
import joblib
import numpy as np
import pandas as pd
import os
import random
import datetime

# Load encoders and models
from sklearn.preprocessing import LabelEncoder
from ml_predict import get_crop_growing_guide

# Helper to load encoders from training scripts
# For demo, we re-fit encoders on known values (in production, save/load them)
crops = [
    # Field crops
    'Wheat', 'Rice', 'Maize', 'Barley', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Bajra', 'Jowar',
    # Fruits (tropical, temperate, berries, nuts, melons, etc.)
    'Mango', 'Banana', 'Apple', 'Orange', 'Papaya', 'Guava', 'Grapes', 'Pomegranate', 'Litchi', 'Pineapple',
    'Watermelon', 'Muskmelon', 'Sapota', 'Custard Apple', 'Jackfruit', 'Plum', 'Peach', 'Pear', 'Cherry',
    'Strawberry', 'Raspberry', 'Blueberry', 'Blackberry', 'Kiwi', 'Avocado', 'Fig', 'Date', 'Coconut',
    'Cashew', 'Walnut', 'Almond', 'Apricot', 'Persimmon', 'Passion Fruit', 'Dragon Fruit', 'Star Fruit',
    'Longan', 'Rambutan', 'Mangosteen', 'Durian', 'Olive', 'Lemon', 'Lime', 'Tangerine', 'Clementine',
    'Mandarin', 'Gooseberry', 'Mulberry', 'Tamarind', 'Bael', 'Ber', 'Jamun', 'Karonda', 'Loquat',
    'Quince', 'Soursop', 'Breadfruit', 'Jujube', 'Medlar', 'Miracle Fruit', 'Salak', 'Santol', 'Satsuma',
    'Soursop', 'Sugar Apple', 'Surinam Cherry', 'Ugli Fruit', 'Yuzu',
    # Vegetables (leafy, root, tuber, bulb, stem, fruit, legumes, gourds, etc.)
    'Tomato', 'Potato', 'Onion', 'Brinjal', 'Cabbage', 'Cauliflower', 'Carrot', 'Peas', 'Okra', 'Spinach',
    'Pumpkin', 'Bitter Gourd', 'Bottle Gourd', 'Cucumber', 'Radish', 'Chilli', 'Garlic', 'Ginger', 'Beans',
    'Coriander', 'Lettuce', 'Broccoli', 'Zucchini', 'Turnip', 'Beetroot', 'Sweet Potato', 'Yam', 'Taro',
    'Fenugreek', 'Mustard Greens', 'Amaranth', 'Celery', 'Leek', 'Kohlrabi', 'Parsnip', 'Artichoke',
    'Asparagus', 'Arugula', 'Bok Choy', 'Swiss Chard', 'Endive', 'Fennel', 'Kale', 'Moringa', 'Purslane',
    'Sorrel', 'Watercress', 'Drumstick', 'Snake Gourd', 'Ridge Gourd', 'Sponge Gourd', 'Pointed Gourd',
    'Ivy Gourd', 'Cluster Beans', 'French Beans', 'Broad Beans', 'Cowpea', 'Lablab', 'Horse Gram',
    'Winged Bean', 'Yardlong Bean', 'Chayote', 'Celeriac', 'Romanesco', 'Pak Choi', 'Napa Cabbage',
    'Daikon', 'Scallion', 'Shallot', 'Spring Onion', 'Lotus Root', 'Jerusalem Artichoke', 'Bamboo Shoot',
    'Brussels Sprout', 'Pattypan Squash', 'Acorn Squash', 'Butternut Squash', 'Delicata Squash',
    'Spaghetti Squash', 'Turban Squash', 'Kabocha', 'Chayote', 'Jicama', 'Salsify', 'Tinda', 'Turnip Greens',
    'Collard Greens', 'Rapini', 'Mustard Spinach', 'Malabar Spinach', 'New Zealand Spinach', 'Orach',
    'Sorrel', 'Tatsoi', 'Mizuna', 'Komatsuna', 'Methi', 'Bathua', 'Poi', 'Kang Kong', 'Basella', 'Chicory',
    'Escarole', 'Radicchio', 'Endive', 'Cress', 'Samphire', 'Sea Beet', 'Sea Kale', 'Sea Lettuce',
    'Sea Purslane', 'Sea Rocket', 'Sea Spinach', 'Sea Aster', 'Sea Blite', 'Sea Arrowgrass', 'Sea Buckthorn',
    'Sea Holly', 'Sea Lavender', 'Sea Plantain', 'Sea Sandwort', 'Sea Wormwood', 'Sea Zostera',
    'Seaweed', 'Algae', 'Duckweed', 'Lotus', 'Water Chestnut', 'Water Spinach', 'Watercress', 'Wasabi',
    'Horseradish', 'Radish', 'Daikon', 'Parsnip', 'Rutabaga', 'Salsify', 'Scorzonera', 'Turnip', 'Yacon',
    'Cassava', 'Arrowroot', 'Tapioca', 'Taro', 'Ube', 'Yam Bean', 'Elephant Foot Yam', 'Konjac',
    'Jerusalem Artichoke', 'Jicama', 'Lotus Root', 'Sweet Corn', 'Maize', 'Popcorn', 'Baby Corn',
    'Corn Salad', 'Corn Gherkin', 'Cornichon', 'Pickling Cucumber', 'Gherkin', 'Dill', 'Parsley',
    'Chervil', 'Lovage', 'Marjoram', 'Oregano', 'Rosemary', 'Sage', 'Savory', 'Tarragon', 'Thyme',
    'Basil', 'Mint', 'Spearmint', 'Peppermint', 'Lemon Balm', 'Catnip', 'Perilla', 'Shiso', 'Vietnamese Coriander',
    'Culantro', 'Cress', 'Garden Cress', 'Land Cress', 'Pepper Cress', 'Upland Cress', 'Watercress',
    'Winter Cress', 'Yellow Rocket', 'Sorrel', 'Wood Sorrel', 'Sheep Sorrel', 'Red Sorrel', 'French Sorrel',
    'Spinach', 'New Zealand Spinach', 'Malabar Spinach', 'Orach', 'Tatsoi', 'Mizuna', 'Komatsuna',
    'Mustard Spinach', 'Mustard Greens', 'Collard Greens', 'Turnip Greens', 'Kale', 'Cabbage', 'Savoy Cabbage',
    'Napa Cabbage', 'Pak Choi', 'Bok Choy', 'Choy Sum', 'Chinese Broccoli', 'Chinese Cabbage',
    'Chinese Spinach', 'Chinese Mustard', 'Chinese Radish', 'Chinese Turnip', 'Chinese Yam', 'Chinese Chive',
    'Chinese Celery', 'Chinese Artichoke', 'Chinese Lettuce', 'Chinese Leek', 'Chinese Long Bean',
    'Chinese Okra', 'Chinese Pea', 'Chinese Pumpkin', 'Chinese Squash', 'Chinese Watercress',
    'Chinese Yam', 'Chinese Zucchini', 'Chinese Eggplant', 'Chinese Bitter Melon', 'Chinese Broccoli',
    'Chinese Cabbage', 'Chinese Celery', 'Chinese Chive', 'Chinese Eggplant', 'Chinese Lettuce',
    'Chinese Long Bean', 'Chinese Mustard', 'Chinese Okra', 'Chinese Pea', 'Chinese Pumpkin',
    'Chinese Radish', 'Chinese Spinach', 'Chinese Squash', 'Chinese Turnip', 'Chinese Watercress',
    'Chinese Yam', 'Chinese Zucchini', 'Chinese Bitter Melon', 'Chinese Broccoli', 'Chinese Cabbage',
    'Chinese Celery', 'Chinese Chive', 'Chinese Eggplant', 'Chinese Lettuce', 'Chinese Long Bean',
    'Chinese Mustard', 'Chinese Okra', 'Chinese Pea', 'Chinese Pumpkin', 'Chinese Radish', 'Chinese Spinach',
    'Chinese Squash', 'Chinese Turnip', 'Chinese Watercress', 'Chinese Yam', 'Chinese Zucchini',
    'Chinese Bitter Melon', 'Chinese Broccoli', 'Chinese Cabbage', 'Chinese Celery', 'Chinese Chive',
    'Chinese Eggplant', 'Chinese Lettuce', 'Chinese Long Bean', 'Chinese Mustard', 'Chinese Okra',
    'Chinese Pea', 'Chinese Pumpkin', 'Chinese Radish', 'Chinese Spinach', 'Chinese Squash',
    'Chinese Turnip', 'Chinese Watercress', 'Chinese Yam', 'Chinese Zucchini', 'Chinese Bitter Melon'
]
fertilizers = ['Urea', 'DAP', 'MOP', 'SSP', 'Compost', 'Vermicompost', 'NPK', 'Ammonium Sulphate']
soil_status = ['Good', 'Moderate', 'Poor']
pests = ['None', 'Rust Fungus', 'Stem Borer', 'Aphids', 'Blight', 'Root Rot', 'Leaf Curl', 'Wilt', 'Mosaic Virus']

le_crop = LabelEncoder().fit(crops)
le_fert = LabelEncoder().fit(fertilizers)
le_soil = LabelEncoder().fit(soil_status)
le_pest = LabelEncoder().fit(pests)

# Load location data
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
locations_path = os.path.join(project_root, 'locations', 'india_locations.csv')
loc_df = pd.read_csv(locations_path)
states = sorted(loc_df['state'].unique())

# Load models
model_dir = os.path.join(project_root, 'models')
crop_model = joblib.load(os.path.join(model_dir, 'crop_model.pkl'))
fert_model = joblib.load(os.path.join(model_dir, 'fertilizer_model.pkl'))
soil_model = joblib.load(os.path.join(model_dir, 'soil_health_model.pkl'))
weather_model = joblib.load(os.path.join(model_dir, 'weather_model.pkl'))
pest_model = joblib.load(os.path.join(model_dir, 'pest_model.pkl'))
yield_model = joblib.load(os.path.join(model_dir, 'yield_model.pkl'))
price_model = joblib.load(os.path.join(model_dir, 'price_model.pkl'))

# For demo, use fixed region and random plausible values for other features
# In production, these would be user inputs or sensor data

def get_random_features(crop, district):
    N = np.random.randint(20, 120)
    P = np.random.randint(10, 100)
    K = np.random.randint(10, 150)
    ph = np.random.uniform(5.5, 7.5)
    rainfall = np.random.uniform(50, 200)
    temperature = np.random.uniform(18, 32)
    humidity = np.random.uniform(40, 80)
    fertilizer_amount = np.random.uniform(40, 120)
    month = np.random.randint(1, 13)
    year = 2024
    return {
        'district': district,
        'N': N, 'P': P, 'K': K, 'ph': ph, 'rainfall': rainfall,
        'temperature': temperature, 'humidity': humidity, 'fertilizer_amount': fertilizer_amount,
        'month': month, 'year': year
    }

def explain_crop_suitability(input_crop, recommended_crop, feats):
    # Check if user's crop matches the recommendation
    if input_crop == recommended_crop:
        # User's crop matches recommendation - explain why it's best for this season
        reasons = []
        
        # Season-specific explanations
        if feats.get('season') == 'Kharif':
            if input_crop in ['Rice', 'Maize', 'Cotton', 'Sugarcane']:
                reasons.append("Kharif season provides ideal monsoon conditions")
            if input_crop in ['Rice', 'Cotton']:
                reasons.append("high rainfall requirements are met during monsoon")
        elif feats.get('season') == 'Rabi':
            if input_crop in ['Wheat', 'Barley', 'Mustard']:
                reasons.append("Rabi season offers cool, dry weather perfect for winter crops")
            if input_crop == 'Wheat':
                reasons.append("winter wheat thrives in moderate temperatures")
        elif feats.get('season') == 'Zaid':
            if input_crop in ['Watermelon', 'Muskmelon', 'Cucumber']:
                reasons.append("Zaid season provides warm weather for summer crops")
        
        # Climate-based explanations
        if 20 <= feats['temperature'] <= 30:
            reasons.append("temperature is in the optimal range")
        if 6.0 <= feats['ph'] <= 7.5:
            reasons.append("soil pH is ideal for this crop")
        if 80 <= feats['rainfall'] <= 250:
            reasons.append("rainfall is sufficient for healthy growth")
        
        # Soil nutrient explanations
        if feats['N'] >= 60:
            reasons.append("adequate nitrogen levels for vegetative growth")
        if feats['P'] >= 30:
            reasons.append("sufficient phosphorus for root development")
        if feats['K'] >= 40:
            reasons.append("good potassium levels for disease resistance")
        
        if not reasons:
            reasons.append("local conditions are optimal for this crop")
        
        return f"✅ {input_crop} is the best choice for {feats['district']} in {feats.get('season', 'this season')} because {', '.join(reasons)}."
    
    else:
        # User's crop doesn't match recommendation - explain why not to grow user's crop and why to grow recommended crop
        user_crop_issues = []
        recommended_crop_benefits = []
        
        # Analyze why user's crop is not suitable
        if input_crop == 'Rice' and feats['rainfall'] < 100:
            user_crop_issues.append(f"Rice needs high rainfall but only {feats['rainfall']:.1f}mm is available")
        elif input_crop == 'Wheat' and feats['temperature'] > 25:
            user_crop_issues.append(f"Wheat prefers cooler temperatures but current temp is {feats['temperature']:.1f}°C")
        elif input_crop in ['Cotton', 'Sugarcane'] and feats['ph'] < 6:
            user_crop_issues.append(f"{input_crop} needs neutral to alkaline soil but pH is {feats['ph']:.1f}")
        elif input_crop in ['Potato', 'Tomato'] and feats['K'] < 50:
            user_crop_issues.append(f"{input_crop} requires high potassium but only {feats['K']} units available")
        
        # General issues
        if feats['ph'] < 6 or feats['ph'] > 7.5:
            user_crop_issues.append(f"soil pH ({feats['ph']:.1f}) is unsuitable for {input_crop}")
        if feats['temperature'] < 15 or feats['temperature'] > 35:
            user_crop_issues.append(f"temperature ({feats['temperature']:.1f}°C) is not ideal for {input_crop}")
        
        # Explain why recommended crop is better
        if recommended_crop == 'Rice' and feats['rainfall'] >= 150:
            recommended_crop_benefits.append("Rice thrives in high rainfall conditions")
        elif recommended_crop == 'Wheat' and 15 <= feats['temperature'] <= 25:
            recommended_crop_benefits.append("Wheat performs best in moderate temperatures")
        elif recommended_crop == 'Cotton' and feats['temperature'] >= 25:
            recommended_crop_benefits.append("Cotton loves warm weather")
        elif recommended_crop == 'Sugarcane' and feats['K'] >= 80:
            recommended_crop_benefits.append("Sugarcane benefits from high potassium levels")
        
        # General benefits of recommended crop
        if 6.0 <= feats['ph'] <= 7.5:
            recommended_crop_benefits.append("soil pH is perfect for this crop")
        if 80 <= feats['rainfall'] <= 250:
            recommended_crop_benefits.append("rainfall is optimal for healthy growth")
        if feats['N'] >= 60 and feats['P'] >= 30 and feats['K'] >= 40:
            recommended_crop_benefits.append("soil nutrients are well-balanced")
        
        if not user_crop_issues:
            user_crop_issues.append("local conditions are not optimal for this crop")
        if not recommended_crop_benefits:
            recommended_crop_benefits.append("it's better suited to your local conditions")
        
        return f"❌ {input_crop} is not recommended for {feats['district']} because {', '.join(user_crop_issues)}. Instead, grow {recommended_crop} because {', '.join(recommended_crop_benefits)}."

# Organized crop lists by category
field_crops = [
    'Wheat', 'Rice', 'Maize', 'Barley', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Bajra', 'Jowar',
    'Sweet Corn', 'Popcorn', 'Baby Corn', 'Sorghum', 'Millet', 'Lentil', 'Chickpea', 'Pigeon Pea', 'Black Gram', 'Green Gram', 'Red Gram', 'Mustard', 'Sunflower', 'Sesame', 'Linseed', 'Safflower', 'Castor', 'Oat', 'Rye', 'Buckwheat', 'Quinoa', 'Amaranth', 'Teff', 'Canola', 'Flax', 'Peanut', 'Rapeseed', 'Triticale', 'Barley', 'Foxtail Millet', 'Little Millet', 'Proso Millet', 'Barnyard Millet', 'Kodo Millet', 'Finger Millet', 'Pearl Millet', "Job's Tears", 'Fonio', 'Spelt', 'Durum Wheat', 'Emmer', 'Einkorn', 'Kamut', 'Freekeh', 'Farro', 'Wild Rice', 'Adzuki Bean', 'Moth Bean', 'Horse Gram', 'Bambara Groundnut', 'Winged Bean', 'Velvet Bean', 'Rice Bean', 'Hyacinth Bean', 'Lablab', 'Cowpea', 'Broad Bean', 'Faba Bean', 'Lima Bean', 'Navy Bean', 'Pinto Bean', 'Kidney Bean', 'Great Northern Bean', 'Black Turtle Bean', 'Mung Bean', 'Urad Bean', 'Field Pea', 'Field Bean', 'Soybean', 'Lupin', 'Lentil', 'Pea', 'Chickpea', 'Pigeon Pea', 'Grass Pea', 'Vetch', 'Fenugreek', 'Clover', 'Alfalfa', 'Sainfoin', 'Birdsfoot Trefoil', 'Lespedeza', 'Stylosanthes', 'Desmodium', 'Siratro', 'Centro', 'Calopo', 'Pueraria', 'Phasey Bean', 'Mucuna', 'Psophocarpus', 'Tephrosia', 'Crotalaria', 'Indigofera', 'Sesbania', 'Aeschynomene', 'Atylosia', 'Canavalia', 'Dolichos', 'Lablab', 'Vigna', 'Vicia', 'Trifolium', 'Medicago', 'Lotus', 'Onobrychis', 'Melilotus', 'Astragalus', 'Coronilla', 'Hedysarum', 'Anthyllis', 'Galega', 'Glycine', 'Phaseolus', 'Pisum', 'Lens', 'Cicer', 'Lathyrus', 'Vigna', 'Vicia', 'Trifolium', 'Medicago', 'Lotus', 'Onobrychis', 'Melilotus', 'Astragalus', 'Coronilla', 'Hedysarum', 'Anthyllis', 'Galega', 'Glycine', 'Phaseolus', 'Pisum', 'Lens', 'Cicer', 'Lathyrus'
]
fruits = [
    'Mango', 'Banana', 'Apple', 'Orange', 'Papaya', 'Guava', 'Grapes', 'Pomegranate', 'Litchi', 'Pineapple',
    'Watermelon', 'Muskmelon', 'Sapota', 'Custard Apple', 'Jackfruit', 'Plum', 'Peach', 'Pear', 'Cherry',
    'Strawberry', 'Raspberry', 'Blueberry', 'Blackberry', 'Kiwi', 'Avocado', 'Fig', 'Date', 'Coconut',
    'Cashew', 'Walnut', 'Almond', 'Apricot', 'Persimmon', 'Passion Fruit', 'Dragon Fruit', 'Star Fruit',
    'Longan', 'Rambutan', 'Mangosteen', 'Durian', 'Olive', 'Lemon', 'Lime', 'Tangerine', 'Clementine',
    'Mandarin', 'Gooseberry', 'Mulberry', 'Tamarind', 'Bael', 'Ber', 'Jamun', 'Karonda', 'Loquat',
    'Quince', 'Soursop', 'Breadfruit', 'Jujube', 'Medlar', 'Miracle Fruit', 'Salak', 'Santol', 'Satsuma',
    'Soursop', 'Sugar Apple', 'Surinam Cherry', 'Ugli Fruit', 'Yuzu'
]
vegetables = [
    'Tomato', 'Potato', 'Onion', 'Brinjal', 'Cabbage', 'Cauliflower', 'Carrot', 'Peas', 'Okra', 'Spinach',
    'Pumpkin', 'Bitter Gourd', 'Bottle Gourd', 'Cucumber', 'Radish', 'Chilli', 'Garlic', 'Ginger', 'Beans',
    'Coriander', 'Lettuce', 'Broccoli', 'Zucchini', 'Turnip', 'Beetroot', 'Sweet Potato', 'Yam', 'Taro',
    'Fenugreek', 'Mustard Greens', 'Amaranth', 'Celery', 'Leek', 'Kohlrabi', 'Parsnip', 'Artichoke',
    'Asparagus', 'Arugula', 'Bok Choy', 'Swiss Chard', 'Endive', 'Fennel', 'Kale', 'Moringa', 'Purslane',
    'Sorrel', 'Watercress', 'Drumstick', 'Snake Gourd', 'Ridge Gourd', 'Sponge Gourd', 'Pointed Gourd',
    'Ivy Gourd', 'Cluster Beans', 'French Beans', 'Broad Beans', 'Cowpea', 'Lablab', 'Horse Gram',
    'Winged Bean', 'Yardlong Bean', 'Chayote', 'Celeriac', 'Romanesco', 'Pak Choi', 'Napa Cabbage',
    'Daikon', 'Scallion', 'Shallot', 'Spring Onion', 'Lotus Root', 'Jerusalem Artichoke', 'Bamboo Shoot',
    'Brussels Sprout', 'Pattypan Squash', 'Acorn Squash', 'Butternut Squash', 'Delicata Squash',
    'Spaghetti Squash', 'Turban Squash', 'Kabocha', 'Chayote', 'Jicama', 'Salsify', 'Tinda', 'Turnip Greens',
    'Collard Greens', 'Rapini', 'Mustard Spinach', 'Malabar Spinach', 'New Zealand Spinach', 'Orach',
    'Sorrel', 'Tatsoi', 'Mizuna', 'Komatsuna', 'Methi', 'Bathua', 'Poi', 'Kang Kong', 'Basella', 'Chicory',
    'Escarole', 'Radicchio', 'Endive', 'Cress', 'Samphire', 'Sea Beet', 'Sea Kale', 'Sea Lettuce',
    'Sea Purslane', 'Sea Rocket', 'Sea Spinach', 'Sea Aster', 'Sea Blite', 'Sea Arrowgrass', 'Sea Buckthorn',
    'Sea Holly', 'Sea Lavender', 'Sea Plantain', 'Sea Sandwort', 'Sea Wormwood', 'Sea Zostera',
    'Seaweed', 'Algae', 'Duckweed', 'Lotus', 'Water Chestnut', 'Water Spinach', 'Watercress', 'Wasabi',
    'Horseradish', 'Radish', 'Daikon', 'Parsnip', 'Rutabaga', 'Salsify', 'Scorzonera', 'Turnip', 'Yacon',
    'Cassava', 'Arrowroot', 'Tapioca', 'Taro', 'Ube', 'Yam Bean', 'Elephant Foot Yam', 'Konjac',
    'Jerusalem Artichoke', 'Jicama', 'Lotus Root'
]
crop_categories = {'1': ('Field Crop', field_crops), '2': ('Vegetable', vegetables), '3': ('Fruit', fruits)}

def main():
    print("\nWelcome to AgroGPT – AI-Powered Smart Farming Assistant!\n", flush=True)
    print("Select crop type:", flush=True)
    print("1. Field Crop\n2. Vegetable\n3. Fruit", flush=True)
    crop_type = None
    while crop_type not in crop_categories:
        crop_type_input = input("Enter crop type (1/2/3): ").strip()
        crop_type = crop_type_input.lower()
        if crop_type not in crop_categories:
            print("Invalid selection. Please enter 1, 2, or 3.", flush=True)
    crop_type_name, crop_list = crop_categories[crop_type]
    print(f"Supported {crop_type_name}s: {', '.join(crop_list)}", flush=True)

    # Add season selection
    seasons = {'1': 'Kharif', '2': 'Rabi', '3': 'Zaid', '4': 'Other'}
    season_names_lower = {v.lower(): v for v in seasons.values()}
    print("Select season:", flush=True)
    print("1. Kharif\n2. Rabi\n3. Zaid\n4. Other", flush=True)
    season_choice = None
    while season_choice not in seasons:
        season_choice_input = input("Enter season (1/2/3/4 or name): ").strip()
        # Accept number or name (case-insensitive)
        if season_choice_input in seasons:
            season_choice = season_choice_input
        elif season_choice_input.lower() in season_names_lower:
            # Map name to number
            for k, v in seasons.items():
                if v.lower() == season_choice_input.lower():
                    season_choice = k
                    break
        if season_choice not in seasons:
            print("Invalid selection. Please enter 1, 2, 3, 4, or a valid season name.", flush=True)
    season = seasons[season_choice]

    # After crop type and season selection, ask for district/locality
    district = input("Enter a district/locality (anywhere in the world): ").strip()
    # Now evaluate best crops for the region and season
    print("\nEvaluating best crops for your region and season...")
    crop_scores = []
    for candidate_crop in crop_list:
        feats = generate_features(candidate_crop, district, season)
        # Use the same logic as the crop recommendation model (or a simple suitability score)
        # For now, use a simple score: higher N, P, K, and rainfall in optimal range
        score = 0
        # Example: favor crops with rainfall, temperature, and pH in ideal range
        if 80 <= feats['rainfall'] <= 250:
            score += 1
        if 6.0 <= feats['ph'] <= 7.5:
            score += 1
        if 18 <= feats['temperature'] <= 32:
            score += 1
        # You can add more sophisticated scoring/model logic here
        crop_scores.append((candidate_crop, score, feats))
    # Sort by score (descending), then alphabetically
    crop_scores.sort(key=lambda x: (-x[1], x[0]))
    top_n = 5
    print(f"\nTop {top_n} recommended {crop_type_name}s for {district} in {season} season:")
    for i, (crop_name, score, feats) in enumerate(crop_scores[:top_n], 1):
        print(f"{i}. {crop_name} (Suitability score: {score})")
    print()
    # Let user pick one for detailed outputs
    valid_crops = [c[0] for c in crop_scores[:top_n]]
    crop = None
    while True:
        crop_input = input(f"Select a {crop_type_name} from the above list for detailed analysis: ").strip()
        crop_key = crop_input.lower()
        if crop_key in [c.lower() for c in valid_crops]:
            # Use the correct casing from valid_crops
            crop = next(c for c in valid_crops if c.lower() == crop_key)
            break
        print(f"Invalid selection. Please choose one of: {', '.join(valid_crops)}", flush=True)
    # Now generate features for the selected crop
    feats = generate_features(crop, district, season)
    # Print feature summary
    print("\n[Feature Summary]")
    for k, v in feats.items():
        print(f"  {k}: {v}")
    # For encoding, use the district as the region (fit on the fly)
    region_enc = LabelEncoder().fit([district]).transform([district])[0]
    crop_enc = le_crop.transform([crop])[0]
    # 1. Crop Recommendation
    crop_input = np.array([[feats['N'], feats['P'], feats['K'], feats['temperature'], feats['humidity'], feats['ph'], feats['rainfall'], region_enc]])
    crop_pred = crop_model.predict(crop_input)[0]
    crop_name = le_crop.inverse_transform([crop_pred])[0]
    # 2. Fertilizer Suggestion
    fert_input = np.array([[crop_enc, feats['N'], feats['P'], feats['K'], feats['ph'], region_enc]])
    fert_pred = fert_model.predict(fert_input)[0]
    fert_name = le_fert.inverse_transform([fert_pred])[0]
    # 3. Soil Health Prediction
    soil_input = np.array([[feats['N'], feats['P'], feats['K'], feats['ph'], np.clip(feats['fertilizer_amount']/50, 0.5, 3.5), region_enc]])
    soil_pred = soil_model.predict(soil_input)[0]
    soil_status_name = le_soil.inverse_transform([soil_pred])[0]
    # 4. Weather-Smart Planning
    weather_input = np.array([[crop_enc, region_enc, feats['month'], feats['temperature'], feats['humidity'], feats['rainfall']]])
    rainfall_forecast = weather_model.predict(weather_input)[0]
    # 5. Pest/Disease Alerts
    pest_input = np.array([[crop_enc, region_enc, feats['month'], feats['temperature'], feats['humidity'], feats['rainfall']]])
    pest_pred = pest_model.predict(pest_input)[0]
    pest_name = le_pest.inverse_transform([pest_pred])[0]
    # 6. Crop Yield Estimation
    yield_input = np.array([[crop_enc, region_enc, feats['N'], feats['P'], feats['K'], feats['ph'], feats['rainfall'], feats['temperature'], feats['humidity'], feats['fertilizer_amount']]])
    yield_pred = yield_model.predict(yield_input)[0]
    # 7. Market Price Forecasting
    price_input = np.array([[crop_enc, region_enc, feats['month'], feats['year'], yield_pred]])
    price_pred = price_model.predict(price_input)[0]
    # Output
    print(f"\n🧠 AgroGPT Smart Assistant Summary for '{crop}' in '{district}':\n{'-'*50}", flush=True)
    print(f"✅ Crop Recommendation: {crop_name}", flush=True)
    # Always show explanation for input crop
    explanation = explain_crop_suitability(crop, crop_name, feats)
    print(f"❓ Why? {explanation}", flush=True)
    print("", flush=True)  # Blank line after explanation
    print(f"🧪 Fertilizer Suggestion: {fert_name}", flush=True)
    print(f"🧪 Soil Health Prediction: {soil_status_name}", flush=True)
    print(f"🌦️ Weather-Smart Planning:", flush=True)
    # Weather-Smart Planning: show as a weather app card
    # Generate synthetic wind speed
    feats['wind'] = round(random.uniform(2, 40), 1)  # km/h
    # Determine rich weather condition
    if feats['rainfall'] > 120 and feats['wind'] > 25:
        weather_cond = 'Stormy ⛈️'
    elif feats['rainfall'] > 100:
        weather_cond = 'Rainy ☔'
    elif feats['wind'] > 20:
        weather_cond = 'Breezy 🌬️'
    elif feats['humidity'] > 85 and feats['temperature'] < 30:
        weather_cond = 'Cloudy ☁️'
    elif feats['temperature'] > 36:
        weather_cond = 'Hot ☀️'
    elif feats['humidity'] > 80:
        weather_cond = 'Humid 💦'
    else:
        weather_cond = 'Sunny ☀️'
    print("┌──────────── Weather-Smart Planning ────────────┐")
    print(f"│  {weather_cond:<42}│")
    print(f"│  🌡️  Temperature: {feats['temperature']:>5} °C{'':18}│")
    print(f"│  💧  Humidity:    {feats['humidity']:>5} %{'':18}│")
    print(f"│  🌧️  Rainfall:    {feats['rainfall']:>5} mm (next 7d){'':4}│")
    print(f"│  🌬️  Wind:        {feats['wind']:>5} km/h{'':18}│")
    print("└───────────────────────────────────────────────┘")
    print(f"🐛 Pest/Disease Alert: {pest_name}", flush=True)
    print(f"📈 Crop Yield Estimation: {yield_pred:.2f} tons/hectare", flush=True)
    print(f"💰 Market Price Forecasting: ₹{price_pred:.0f}/quintal (region: {district})", flush=True)
    print('-'*50, flush=True)
    
    # Add Growing Guide Section
    print(f"\n📚 STEP-BY-STEP GROWING GUIDE", flush=True)
    print("="*50, flush=True)
    
    # Get growing guide for the selected crop
    growing_guide = get_crop_growing_guide(crop, season, district)
    
    print(f"{growing_guide['title']}", flush=True)
    print(f"⏱️  Duration: {growing_guide['duration']}", flush=True)
    print(f"📍 Location: {district}", flush=True)
    print(f"🌤️  Season: {season}", flush=True)
    
    if 'overview' in growing_guide:
        print(f"📖 Overview: {growing_guide['overview']}", flush=True)
    
    print("", flush=True)
    
    # Display detailed step-by-step guide
    for i, phase in enumerate(growing_guide['steps'], 1):
        print(f"📋 Phase {i}: {phase['phase']}", flush=True)
        
        if 'description' in phase:
            print(f"   📝 {phase['description']}", flush=True)
        
        print("   Steps:", flush=True)
        
        # Check if detailed_steps exist (enhanced format)
        if 'detailed_steps' in phase:
            for step_detail in phase['detailed_steps']:
                print(f"   {step_detail['step']}", flush=True)
                for point in step_detail['points']:
                    print(f"      {point}", flush=True)
                print("", flush=True)
        else:
            # Fallback to simple format
            for j, step in enumerate(phase['steps'], 1):
                print(f"   {j}. {step}", flush=True)
            print("", flush=True)
    
    print("💡 Expert Tips:", flush=True)
    print("   • Monitor weather conditions regularly", flush=True)
    print("   • Keep detailed records of all activities", flush=True)
    print("   • Consult local agricultural experts", flush=True)
    print("   • Use integrated pest management (IPM)", flush=True)
    print("   • Practice crop rotation for better yields", flush=True)
    print("   • Test soil before starting cultivation", flush=True)
    print("   • Use quality seeds and inputs", flush=True)
    print("   • Follow recommended spacing and timing", flush=True)
    print("   • Monitor for pests and diseases regularly", flush=True)
    print("   • Harvest at optimal maturity stage", flush=True)
    print("", flush=True)
    
    print("🔧 Technical Notes:", flush=True)
    print("   • All measurements are per hectare unless specified", flush=True)
    print("   • DAS = Days After Sowing, DAT = Days After Transplanting", flush=True)
    print("   • Adjust timing based on local weather conditions", flush=True)
    print("   • Follow local agricultural extension recommendations", flush=True)
    print("   • Use appropriate safety equipment when handling chemicals", flush=True)
    print("", flush=True)
    
    print("\n(See visualizations in the /visualizations folder for model performance.)\n", flush=True)
    print("[AgroGPT CLI completed]", flush=True)

    # --- OUTPUTS ---
    print("\n================== AgroGPT Smart Farming Results ==================")
    # 1. Crop Recommendation (show multiple)
    print("\nCrop Recommendation:")
    for i, (crop_name, score, feats) in enumerate(crop_scores[:top_n], 1):
        reason = []
        if 80 <= feats['rainfall'] <= 250:
            reason.append("rainfall suitable")
        if 6.0 <= feats['ph'] <= 7.5:
            reason.append("pH optimal")
        if 18 <= feats['temperature'] <= 32:
            reason.append("temperature ideal")
        reason_str = ", ".join(reason) if reason else "general suitability"
        print(f"{i}. {crop_name} (Score: {score}) - {reason_str}")
    print("---------------------------------------------------------------")
    # 2. Fertilizer Suggestion (for selected crop)
    print(f"🧪 Fertilizer Suggestion: {fert_name}", flush=True)
    print(f"🧪 Soil Health Prediction: {soil_status_name}", flush=True)
    print(f"🌦️ Weather-Smart Planning:", flush=True)
    print(f"   Temperature: {feats['temperature']}°C", flush=True)
    print(f"   Humidity: {feats['humidity']}%", flush=True)
    print(f"   Rainfall forecast (next 7d): {feats['rainfall']} mm", flush=True)
    print(f"🐛 Pest/Disease Alert: {pest_name}", flush=True)
    print(f"📈 Crop Yield Estimation: {yield_pred:.2f} tons/hectare", flush=True)
    print(f"💰 Market Price Forecasting: ₹{price_pred:.0f}/quintal (region: {district})", flush=True)
    print('-'*50, flush=True)
    print("\n(See visualizations in the /visualizations folder for model performance.)\n", flush=True)
    print("[AgroGPT CLI completed]", flush=True)

def generate_features(crop, district, season):
    import random
    import datetime
    now = datetime.datetime.now()

    # Example agronomic ranges for field crops, fruits, vegetables, and some region-based logic
    crop_season_params = {
        # Field Crops
        ('Wheat', 'Rabi'):    {'N': (80, 120), 'P': (40, 60), 'K': (40, 60), 'temperature': (15, 25), 'rainfall': (20, 100)},
        ('Rice', 'Kharif'):   {'N': (100, 150), 'P': (40, 60), 'K': (40, 60), 'temperature': (20, 35), 'rainfall': (150, 300)},
        ('Maize', 'Kharif'):  {'N': (120, 180), 'P': (60, 80), 'K': (40, 60), 'temperature': (20, 32), 'rainfall': (100, 200)},
        ('Potato', 'Rabi'):   {'N': (100, 150), 'P': (60, 80), 'K': (80, 120), 'temperature': (15, 22), 'rainfall': (50, 100)},
        ('Sugarcane', 'Other'): {'N': (150, 250), 'P': (60, 100), 'K': (60, 120), 'temperature': (20, 35), 'rainfall': (100, 250)},
        ('Bajra', 'Kharif'):  {'N': (60, 90), 'P': (30, 50), 'K': (20, 40), 'temperature': (20, 32), 'rainfall': (40, 120)},
        # Vegetables
        ('Tomato', 'Zaid'):   {'N': (100, 150), 'P': (50, 80), 'K': (50, 80), 'temperature': (20, 30), 'rainfall': (50, 150)},
        ('Onion', 'Rabi'):    {'N': (80, 120), 'P': (40, 60), 'K': (60, 100), 'temperature': (15, 25), 'rainfall': (30, 80)},
        ('Brinjal', 'Kharif'): {'N': (90, 120), 'P': (50, 70), 'K': (50, 80), 'temperature': (20, 30), 'rainfall': (60, 120)},
        ('Cabbage', 'Rabi'):  {'N': (100, 150), 'P': (60, 80), 'K': (60, 80), 'temperature': (12, 22), 'rainfall': (40, 100)},
        ('Carrot', 'Rabi'):   {'N': (80, 120), 'P': (40, 60), 'K': (60, 80), 'temperature': (10, 20), 'rainfall': (30, 80)},
        # Fruits
        ('Mango', 'Kharif'):  {'N': (100, 200), 'P': (50, 100), 'K': (100, 200), 'temperature': (24, 36), 'rainfall': (75, 250)},
        ('Banana', 'Other'):  {'N': (150, 250), 'P': (60, 120), 'K': (200, 300), 'temperature': (20, 35), 'rainfall': (100, 300)},
        ('Apple', 'Rabi'):    {'N': (60, 120), 'P': (30, 60), 'K': (120, 180), 'temperature': (10, 24), 'rainfall': (50, 150)},
        ('Grapes', 'Zaid'):   {'N': (60, 100), 'P': (30, 60), 'K': (120, 180), 'temperature': (15, 30), 'rainfall': (30, 100)},
        ('Papaya', 'Other'):  {'N': (100, 200), 'P': (50, 100), 'K': (100, 200), 'temperature': (22, 32), 'rainfall': (80, 200)},
        # Region-based example (for demonstration, e.g., 'Punjab')
        ('Wheat', 'Rabi', 'Punjab'): {'N': (100, 140), 'P': (50, 70), 'K': (50, 70), 'temperature': (12, 22), 'rainfall': (30, 80)},
        # Add more crops, fruits, vegetables, and region-based logic as needed
    }
    # Default ranges
    default_params = {'N': (80, 150), 'P': (30, 80), 'K': (30, 80), 'temperature': (18, 35), 'rainfall': (50, 200)}

    # Try region-based match first
    params = crop_season_params.get((crop, season, district), None)
    if params is None:
        params = crop_season_params.get((crop, season), default_params)

    features = {
        'crop': crop,
        'district': district,
        'season': season,
        'N': random.randint(*params['N']),
        'P': random.randint(*params['P']),
        'K': random.randint(*params['K']),
        'temperature': round(random.uniform(*params['temperature']), 2),
        'humidity': round(random.uniform(40, 90), 2),
        'ph': round(random.uniform(6.0, 7.5), 2),
        'rainfall': round(random.uniform(*params['rainfall']), 2),
        'fertilizer_amount': random.randint(80, 200),
        'month': now.month,
        'year': now.year,
    }
    # Safety: ensure all required keys are present
    required_keys = [
        'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall',
        'fertilizer_amount', 'month', 'year', 'crop', 'district', 'season'
    ]
    for key in required_keys:
        if key not in features:
            print(f"[Warning] Feature '{key}' missing, filling with default value.")
            if key in ['N', 'P', 'K', 'fertilizer_amount']:
                features[key] = 100
            elif key in ['temperature']:
                features[key] = 25.0
            elif key in ['humidity']:
                features[key] = 60.0
            elif key in ['ph']:
                features[key] = 7.0
            elif key in ['rainfall']:
                features[key] = 100.0
            elif key == 'month':
                features[key] = now.month
            elif key == 'year':
                features[key] = now.year
            else:
                features[key] = ''
    return features

if __name__ == '__main__':
    main() 