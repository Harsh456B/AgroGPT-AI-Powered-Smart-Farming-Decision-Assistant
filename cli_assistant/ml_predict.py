import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import random
import datetime

# Load encoders and models
crops = [
    'Wheat', 'Rice', 'Maize', 'Barley', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Bajra', 'Jowar',
    'Mango', 'Banana', 'Apple', 'Orange', 'Papaya', 'Guava', 'Grapes', 'Pomegranate', 'Litchi', 'Pineapple',
    'Watermelon', 'Muskmelon', 'Sapota', 'Custard Apple', 'Jackfruit', 'Plum', 'Peach', 'Pear', 'Cherry',
    'Strawberry', 'Raspberry', 'Blueberry', 'Blackberry', 'Kiwi', 'Avocado', 'Fig', 'Date', 'Coconut',
    'Cashew', 'Walnut', 'Almond', 'Apricot', 'Persimmon', 'Passion Fruit', 'Dragon Fruit', 'Star Fruit',
    'Longan', 'Rambutan', 'Mangosteen', 'Durian', 'Olive', 'Lemon', 'Lime', 'Tangerine', 'Clementine',
    'Mandarin', 'Gooseberry', 'Mulberry', 'Tamarind', 'Bael', 'Ber', 'Jamun', 'Karonda', 'Loquat',
    'Quince', 'Soursop', 'Breadfruit', 'Jujube', 'Medlar', 'Miracle Fruit', 'Salak', 'Santol', 'Satsuma',
    'Soursop', 'Sugar Apple', 'Surinam Cherry', 'Ugli Fruit', 'Yuzu',
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
    'Chinese Squash', 'Chinese Turnip', 'Chinese Watercress', 'Chinese Yam', 'Chinese Zucchini', 'Chinese Bitter Melon'
]
fertilizers = ['Urea', 'DAP', 'MOP', 'SSP', 'Compost', 'Vermicompost', 'NPK', 'Ammonium Sulphate']
soil_status = ['Good', 'Moderate', 'Poor']
pests = ['None', 'Rust Fungus', 'Stem Borer', 'Aphids', 'Blight', 'Root Rot', 'Leaf Curl', 'Wilt', 'Mosaic Virus']

le_crop = LabelEncoder().fit(crops)
le_fert = LabelEncoder().fit(fertilizers)
le_soil = LabelEncoder().fit(soil_status)
le_pest = LabelEncoder().fit(pests)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_dir = os.path.join(project_root, 'models')

crop_model = joblib.load(os.path.join(model_dir, 'crop_model.pkl'))
fert_model = joblib.load(os.path.join(model_dir, 'fertilizer_model.pkl'))
soil_model = joblib.load(os.path.join(model_dir, 'soil_health_model.pkl'))
weather_model = joblib.load(os.path.join(model_dir, 'weather_model.pkl'))
pest_model = joblib.load(os.path.join(model_dir, 'pest_model.pkl'))
yield_model = joblib.load(os.path.join(model_dir, 'yield_model.pkl'))
price_model = joblib.load(os.path.join(model_dir, 'price_model.pkl'))

# Feature generation for demo (can be replaced with real user input)
def generate_features(crop, district, season):
    now = datetime.datetime.now()
    default_params = {'N': (80, 150), 'P': (30, 80), 'K': (30, 80), 'temperature': (18, 35), 'rainfall': (50, 200)}
    features = {
        'crop': crop,
        'district': district,
        'season': season,
        'N': random.randint(*default_params['N']),
        'P': random.randint(*default_params['P']),
        'K': random.randint(*default_params['K']),
        'temperature': round(random.uniform(*default_params['temperature']), 2),
        'humidity': round(random.uniform(40, 90), 2),
        'ph': round(random.uniform(6.0, 7.5), 2),
        'rainfall': round(random.uniform(*default_params['rainfall']), 2),
        'fertilizer_amount': random.randint(80, 200),
        'month': now.month,
        'year': now.year,
    }
    return features

# Example: Crop recommendation prediction
def predict_crop(features):
    region_enc = LabelEncoder().fit([features['district']]).transform([features['district']])[0]
    crop_input = np.array([[features['N'], features['P'], features['K'], features['temperature'], features['humidity'], features['ph'], features['rainfall'], region_enc]])
    crop_pred = crop_model.predict(crop_input)[0]
    crop_name = le_crop.inverse_transform([crop_pred])[0]
    return crop_name

def predict_fertilizer(features):
    crop_enc = le_crop.transform([features['crop']])[0]
    region_enc = LabelEncoder().fit([features['district']]).transform([features['district']])[0]
    fert_input = np.array([[crop_enc, features['N'], features['P'], features['K'], features['ph'], region_enc]])
    fert_pred = fert_model.predict(fert_input)[0]
    fert_name = le_fert.inverse_transform([fert_pred])[0]
    return fert_name

def predict_soil_health(features):
    region_enc = LabelEncoder().fit([features['district']]).transform([features['district']])[0]
    soil_input = np.array([[features['N'], features['P'], features['K'], features['ph'], np.clip(features['fertilizer_amount']/50, 0.5, 3.5), region_enc]])
    soil_pred = soil_model.predict(soil_input)[0]
    soil_status_name = le_soil.inverse_transform([soil_pred])[0]
    return soil_status_name

def predict_pest(features):
    crop_enc = le_crop.transform([features['crop']])[0]
    region_enc = LabelEncoder().fit([features['district']]).transform([features['district']])[0]
    pest_input = np.array([[crop_enc, region_enc, features['month'], features['temperature'], features['humidity'], features['rainfall']]])
    pest_pred = pest_model.predict(pest_input)[0]
    pest_name = le_pest.inverse_transform([pest_pred])[0]
    return pest_name

def predict_yield(features):
    crop_enc = le_crop.transform([features['crop']])[0]
    region_enc = LabelEncoder().fit([features['district']]).transform([features['district']])[0]
    yield_input = np.array([[crop_enc, region_enc, features['N'], features['P'], features['K'], features['ph'], features['rainfall'], features['temperature'], features['humidity'], features['fertilizer_amount']]])
    yield_pred = yield_model.predict(yield_input)[0]
    return yield_pred

def predict_price(features, yield_pred):
    crop_enc = le_crop.transform([features['crop']])[0]
    region_enc = LabelEncoder().fit([features['district']]).transform([features['district']])[0]
    price_input = np.array([[crop_enc, region_enc, features['month'], features['year'], yield_pred]])
    price_pred = price_model.predict(price_input)[0]
    return price_pred

def get_crop_growing_guide(crop_name, season, location):
    """
    Provides comprehensive step-by-step growing process guide for different crops
    """
    
    # Comprehensive growing guides with detailed point-wise instructions
    growing_guides = {
        'Rice': {
            'title': '🌾 Rice Cultivation Guide - Complete Process',
            'duration': '120-150 days',
            'overview': 'Rice is a staple food crop that requires careful water management and proper timing for optimal yields.',
            'steps': [
                {
                    'phase': '🌱 Phase 1: Land Preparation (Week 1-2)',
                    'description': 'Proper land preparation is crucial for rice cultivation as it affects water management and root development.',
                    'detailed_steps': [
                        {
                            'step': '1.1 Initial Field Assessment',
                            'points': [
                                '• Survey the field for proper drainage',
                                '• Check soil type and pH (ideal: 6.0-7.0)',
                                '• Measure field dimensions for planning',
                                '• Identify any existing bunds or irrigation channels'
                            ]
                        },
                        {
                            'step': '1.2 Deep Plowing',
                            'points': [
                                '• Use tractor-mounted plow for deep tilling (15-20 cm)',
                                '• Plow in both directions (cross-plowing)',
                                '• Break large soil clods into smaller pieces',
                                '• Remove any crop residues or weeds'
                            ]
                        },
                        {
                            'step': '1.3 Leveling and Grading',
                            'points': [
                                '• Use laser leveler for precise field leveling',
                                '• Ensure uniform slope (0.1-0.2%) for water flow',
                                '• Create micro-basins for water retention',
                                '• Mark field boundaries clearly'
                            ]
                        },
                        {
                            'step': '1.4 Manure Application',
                            'points': [
                                '• Apply 10-15 tons of farmyard manure per hectare',
                                '• Spread manure evenly across the field',
                                '• Mix manure with top 10-15 cm of soil',
                                '• Allow 7-10 days for manure decomposition'
                            ]
                        },
                        {
                            'step': '1.5 Bund Construction',
                            'points': [
                                '• Build bunds 20-25 cm high around field',
                                '• Maintain bund width of 30-40 cm',
                                '• Compact bunds properly to prevent water leakage',
                                '• Create inlet and outlet channels for water management'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 2: Seed Preparation & Nursery (Week 2-3)',
                    'description': 'Quality seed preparation and nursery management are critical for healthy seedling development.',
                    'detailed_steps': [
                        {
                            'step': '2.1 Seed Selection',
                            'points': [
                                '• Choose certified seeds from reliable sources',
                                '• Select seeds based on local climate and soil conditions',
                                '• Ensure seed purity and germination rate (>85%)',
                                '• Calculate seed requirement (40-50 kg/ha for direct sowing)'
                            ]
                        },
                        {
                            'step': '2.2 Seed Treatment',
                            'points': [
                                '• Soak seeds in clean water for 24 hours',
                                '• Treat with fungicide (Carbendazim 2g/kg seed)',
                                '• Apply biofertilizers (Azospirillum 600g/ha)',
                                '• Dry seeds in shade for 2-3 hours before sowing'
                            ]
                        },
                        {
                            'step': '2.3 Nursery Bed Preparation',
                            'points': [
                                '• Prepare raised beds (1m width, 10-15cm height)',
                                '• Mix fine soil with farmyard manure',
                                '• Apply 2-3 kg DAP per 100 sq.m of nursery',
                                '• Maintain proper spacing between beds (30cm)'
                            ]
                        },
                        {
                            'step': '2.4 Seed Sowing in Nursery',
                            'points': [
                                '• Sow seeds at 1-2 cm depth',
                                '• Maintain 5-10 cm spacing between seeds',
                                '• Cover seeds with fine soil',
                                '• Maintain 2-3 cm water level in nursery'
                            ]
                        },
                        {
                            'step': '2.5 Nursery Management',
                            'points': [
                                '• Monitor water level daily',
                                '• Apply urea (1kg/100 sq.m) at 10 days after sowing',
                                '• Control weeds by hand weeding',
                                '• Protect from birds and pests'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 3: Transplanting (Week 4-5)',
                    'description': 'Careful transplanting ensures proper establishment and uniform crop stand.',
                    'detailed_steps': [
                        {
                            'step': '3.1 Seedling Preparation',
                            'points': [
                                '• Uproot 25-30 day old seedlings carefully',
                                '• Wash roots to remove soil',
                                '• Trim roots to 2-3 cm length',
                                '• Bundle seedlings in groups of 50-100'
                            ]
                        },
                        {
                            'step': '3.2 Field Preparation for Transplanting',
                            'points': [
                                '• Maintain 3-5 cm water level in main field',
                                '• Mark transplanting lines using rope',
                                '• Apply first dose of nitrogen fertilizer',
                                '• Ensure uniform water distribution'
                            ]
                        },
                        {
                            'step': '3.3 Transplanting Process',
                            'points': [
                                '• Transplant at 20x15 cm spacing',
                                '• Plant 2-3 seedlings per hill',
                                '• Insert seedlings 2-3 cm deep',
                                '• Ensure proper root-soil contact'
                            ]
                        },
                        {
                            'step': '3.4 Post-Transplanting Care',
                            'points': [
                                '• Maintain 3-5 cm water level for 3-5 days',
                                '• Apply first dose of nitrogen (25% of total)',
                                '• Monitor for any gaps and replant if needed',
                                '• Control early weed growth'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 4: Vegetative Growth Management (Week 6-10)',
                    'description': 'This phase focuses on tillering, root development, and early pest management.',
                    'detailed_steps': [
                        {
                            'step': '4.1 Water Management',
                            'points': [
                                '• Maintain 5-7 cm water level during vegetative phase',
                                '• Allow field to dry for 2-3 days before next irrigation',
                                '• Monitor water quality and temperature',
                                '• Ensure proper drainage during heavy rains'
                            ]
                        },
                        {
                            'step': '4.2 Fertilizer Application',
                            'points': [
                                '• Apply second dose of nitrogen (50% of total) at 25-30 DAT',
                                '• Apply phosphorus (60 kg P2O5/ha) if not applied earlier',
                                '• Apply potassium (40 kg K2O/ha) for better tillering',
                                '• Use split application method for better efficiency'
                            ]
                        },
                        {
                            'step': '4.3 Weed Control',
                            'points': [
                                '• Conduct first weeding at 15-20 DAT',
                                '• Use herbicides (Butachlor 1.5 kg/ha) if needed',
                                '• Manual weeding at 30-35 DAT',
                                '• Remove aquatic weeds regularly'
                            ]
                        },
                        {
                            'step': '4.4 Pest Monitoring',
                            'points': [
                                '• Monitor for stem borer (weekly scouting)',
                                '• Check for leaf folder and leaf hopper',
                                '• Use light traps for pest monitoring',
                                '• Apply neem-based products for early control'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 5: Reproductive Phase (Week 11-14)',
                    'description': 'Critical phase for panicle development, flowering, and grain formation.',
                    'detailed_steps': [
                        {
                            'step': '5.1 Water Management',
                            'points': [
                                '• Maintain 3-4 cm water level during flowering',
                                '• Avoid water stress during panicle initiation',
                                '• Control water to prevent lodging',
                                '• Ensure proper drainage for grain filling'
                            ]
                        },
                        {
                            'step': '5.2 Nutrient Management',
                            'points': [
                                '• Apply third dose of nitrogen (25% of total) at booting',
                                '• Apply micronutrients if deficiency symptoms appear',
                                '• Monitor leaf color for nutrient status',
                                '• Avoid over-fertilization to prevent lodging'
                            ]
                        },
                        {
                            'step': '5.3 Disease Management',
                            'points': [
                                '• Monitor for blast disease (leaf and neck)',
                                '• Check for bacterial blight symptoms',
                                '• Apply fungicides if disease pressure is high',
                                '• Maintain proper field hygiene'
                            ]
                        },
                        {
                            'step': '5.4 Growth Monitoring',
                            'points': [
                                '• Count tillers per square meter',
                                '• Monitor panicle development',
                                '• Check for uniform flowering',
                                '• Assess crop health and vigor'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 6: Maturity & Harvesting (Week 15-20)',
                    'description': 'Proper timing and method of harvesting ensure maximum yield and quality.',
                    'detailed_steps': [
                        {
                            'step': '6.1 Maturity Assessment',
                            'points': [
                                '• Monitor grain color change (green to golden yellow)',
                                '• Check grain moisture content (20-25%)',
                                '• Assess panicle maturity (80-85% grains mature)',
                                '• Plan harvest timing based on weather forecast'
                            ]
                        },
                        {
                            'step': '6.2 Pre-Harvest Preparation',
                            'points': [
                                '• Stop irrigation 7-10 days before harvest',
                                '• Prepare harvesting equipment and storage facilities',
                                '• Arrange labor for manual harvesting',
                                '• Plan post-harvest handling procedures'
                            ]
                        },
                        {
                            'step': '6.3 Harvesting Process',
                            'points': [
                                '• Harvest when 80-85% grains turn golden yellow',
                                '• Use combine harvester or manual methods',
                                '• Cut crop close to ground level',
                                '• Handle harvested crop carefully to minimize losses'
                            ]
                        },
                        {
                            'step': '6.4 Post-Harvest Handling',
                            'points': [
                                '• Thresh immediately to prevent grain loss',
                                '• Clean grains to remove impurities',
                                '• Dry grains to 12-14% moisture content',
                                '• Store in proper conditions to prevent spoilage'
                            ]
                        }
                    ]
                }
            ]
        },
        
        'Wheat': {
            'title': '🌾 Wheat Cultivation Guide - Complete Process',
            'duration': '110-130 days',
            'overview': 'Wheat is a winter crop that requires proper timing, temperature management, and nutrient balance for optimal yields.',
            'steps': [
                {
                    'phase': '🌱 Phase 1: Land Preparation (Week 1)',
                    'description': 'Proper land preparation ensures good seed-soil contact and uniform crop establishment.',
                    'detailed_steps': [
                        {
                            'step': '1.1 Field Assessment',
                            'points': [
                                '• Check soil moisture and texture',
                                '• Test soil pH (ideal: 6.5-7.5)',
                                '• Assess previous crop residues',
                                '• Plan field layout and irrigation system'
                            ]
                        },
                        {
                            'step': '1.2 Primary Tillage',
                            'points': [
                                '• Plow field 2-3 times to fine tilth',
                                '• Use disc plow for heavy soils',
                                '• Break soil clods to 2-3 cm size',
                                '• Remove crop residues and weeds'
                            ]
                        },
                        {
                            'step': '1.3 Manure Application',
                            'points': [
                                '• Apply 10-15 tons farmyard manure per hectare',
                                '• Spread manure evenly across field',
                                '• Mix manure with top 15-20 cm soil',
                                '• Allow 7-10 days for decomposition'
                            ]
                        },
                        {
                            'step': '1.4 Final Land Preparation',
                            'points': [
                                '• Level field for uniform irrigation',
                                '• Prepare seedbed with proper moisture',
                                '• Create furrows for irrigation (if needed)',
                                '• Mark field boundaries and pathways'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 2: Sowing (Week 2)',
                    'description': 'Proper sowing ensures uniform crop stand and optimal plant population.',
                    'detailed_steps': [
                        {
                            'step': '2.1 Seed Preparation',
                            'points': [
                                '• Select certified seeds with >85% germination',
                                '• Treat seeds with fungicide (Carbendazim 2g/kg)',
                                '• Apply biofertilizers (Azotobacter 600g/ha)',
                                '• Calculate seed rate (100-125 kg/ha)'
                            ]
                        },
                        {
                            'step': '2.2 Sowing Method',
                            'points': [
                                '• Use seed drill for uniform sowing',
                                '• Sow at 2-3 cm depth',
                                '• Maintain 20-22 cm row spacing',
                                '• Ensure proper seed-soil contact'
                            ]
                        },
                        {
                            'step': '2.3 Initial Fertilization',
                            'points': [
                                '• Apply first dose of nitrogen (25% of total)',
                                '• Apply full dose of phosphorus (60 kg P2O5/ha)',
                                '• Apply full dose of potassium (40 kg K2O/ha)',
                                '• Place fertilizers 5-7 cm below seed'
                            ]
                        },
                        {
                            'step': '2.4 Post-Sowing Care',
                            'points': [
                                '• Apply light irrigation if soil is dry',
                                '• Monitor for uniform germination',
                                '• Control early weed growth',
                                '• Protect from birds and pests'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 3: Vegetative Growth (Week 3-8)',
                    'description': 'This phase focuses on tillering, root development, and early crop management.',
                    'detailed_steps': [
                        {
                            'step': '3.1 Irrigation Management',
                            'points': [
                                '• Apply first irrigation at crown root initiation (21 DAS)',
                                '• Maintain 5-7 day irrigation intervals',
                                '• Avoid waterlogging in heavy soils',
                                '• Monitor soil moisture regularly'
                            ]
                        },
                        {
                            'step': '3.2 Fertilizer Application',
                            'points': [
                                '• Apply second dose of nitrogen (50% of total) at tillering',
                                '• Apply micronutrients if deficiency appears',
                                '• Use split application for better efficiency',
                                '• Monitor leaf color for nutrient status'
                            ]
                        },
                        {
                            'step': '3.3 Weed Control',
                            'points': [
                                '• Apply pre-emergence herbicides if needed',
                                '• Conduct manual weeding at 30-35 DAS',
                                '• Remove broad-leaved and grassy weeds',
                                '• Maintain weed-free field until flowering'
                            ]
                        },
                        {
                            'step': '3.4 Pest Monitoring',
                            'points': [
                                '• Monitor for aphids and termites',
                                '• Check for rust diseases (leaf, stem, stripe)',
                                '• Use yellow sticky traps for pest monitoring',
                                '• Apply preventive sprays if needed'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 4: Reproductive Phase (Week 9-12)',
                    'description': 'Critical phase for spike development, flowering, and grain formation.',
                    'detailed_steps': [
                        {
                            'step': '4.1 Water Management',
                            'points': [
                                '• Apply irrigation at flowering stage',
                                '• Maintain adequate moisture during grain filling',
                                '• Avoid water stress during critical stages',
                                '• Control irrigation to prevent lodging'
                            ]
                        },
                        {
                            'step': '4.2 Nutrient Management',
                            'points': [
                                '• Apply third dose of nitrogen (25% of total) at booting',
                                '• Monitor for micronutrient deficiencies',
                                '• Avoid late nitrogen application',
                                '• Assess crop health and vigor'
                            ]
                        },
                        {
                            'step': '4.3 Disease Management',
                            'points': [
                                '• Monitor for Karnal bunt and loose smut',
                                '• Check for powdery mildew',
                                '• Apply fungicides if disease pressure is high',
                                '• Maintain proper field hygiene'
                            ]
                        },
                        {
                            'step': '4.4 Growth Monitoring',
                            'points': [
                                '• Count tillers per square meter',
                                '• Monitor spike development',
                                '• Check for uniform flowering',
                                '• Assess crop health and vigor'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 5: Maturity & Harvesting (Week 13-16)',
                    'description': 'Proper timing and method of harvesting ensure maximum yield and quality.',
                    'detailed_steps': [
                        {
                            'step': '5.1 Maturity Assessment',
                            'points': [
                                '• Monitor grain color change (green to golden)',
                                '• Check grain moisture content (20-25%)',
                                '• Assess spike maturity (grains hard and dry)',
                                '• Plan harvest timing based on weather'
                            ]
                        },
                        {
                            'step': '5.2 Pre-Harvest Preparation',
                            'points': [
                                '• Stop irrigation 10-15 days before harvest',
                                '• Prepare harvesting equipment',
                                '• Arrange labor for manual harvesting',
                                '• Plan post-harvest handling'
                            ]
                        },
                        {
                            'step': '5.3 Harvesting Process',
                            'points': [
                                '• Harvest when grains are hard and straw is dry',
                                '• Use combine harvester or manual methods',
                                '• Cut crop close to ground level',
                                '• Handle harvested crop carefully'
                            ]
                        },
                        {
                            'step': '5.4 Post-Harvest Handling',
                            'points': [
                                '• Thresh using combine or traditional methods',
                                '• Clean grains to remove impurities',
                                '• Dry grains to 12-14% moisture content',
                                '• Store in proper conditions'
                            ]
                        }
                    ]
                }
            ]
        },
        
        'Maize': {
            'title': '🌽 Maize Cultivation Guide',
            'duration': '90-120 days',
            'steps': [
                {
                    'phase': '🌱 Land Preparation (Week 1)',
                    'steps': [
                        'Plow the field 2-3 times to fine tilth',
                        'Apply 10-15 tons of farmyard manure per hectare',
                        'Level the field for uniform irrigation',
                        'Prepare ridges and furrows for better drainage'
                    ]
                },
                {
                    'phase': '🌱 Sowing (Week 2)',
                    'steps': [
                        'Treat seeds with fungicide and biofertilizers',
                        'Sow at 3-4 cm depth in ridges',
                        'Maintain 60x20 cm spacing',
                        'Apply first dose of nitrogen fertilizer'
                    ]
                },
                {
                    'phase': '🌱 Vegetative Growth (Week 3-6)',
                    'steps': [
                        'Apply irrigation at knee-high stage',
                        'Apply second dose of nitrogen at 25 DAS',
                        'Control weeds by hand weeding or herbicides',
                        'Monitor for fall armyworm and stem borer'
                    ]
                },
                {
                    'phase': '🌱 Flowering & Grain Formation (Week 7-10)',
                    'steps': [
                        'Apply irrigation at tasseling and silking',
                        'Apply third dose of nitrogen at tasseling',
                        'Control water to prevent lodging',
                        'Monitor for diseases like leaf blight and rust'
                    ]
                },
                {
                    'phase': '🌱 Maturity & Harvesting (Week 11-14)',
                    'steps': [
                        'Stop irrigation 10-15 days before harvest',
                        'Harvest when grains are hard and moisture is 20-25%',
                        'Remove husks and dry cobs in sunlight',
                        'Store grains at 12-14% moisture content'
                    ]
                }
            ]
        },
        
        'Cotton': {
            'title': '🧵 Cotton Cultivation Guide',
            'duration': '150-180 days',
            'steps': [
                {
                    'phase': '🌱 Land Preparation (Week 1-2)',
                    'steps': [
                        'Plow the field 2-3 times to fine tilth',
                        'Apply 10-15 tons of farmyard manure per hectare',
                        'Level the field for uniform irrigation',
                        'Prepare ridges and furrows for better drainage'
                    ]
                },
                {
                    'phase': '🌱 Sowing (Week 3)',
                    'steps': [
                        'Treat seeds with fungicide and biofertilizers',
                        'Sow at 2-3 cm depth in ridges',
                        'Maintain 90x30 cm spacing',
                        'Apply first dose of nitrogen fertilizer'
                    ]
                },
                {
                    'phase': '🌱 Vegetative Growth (Week 4-8)',
                    'steps': [
                        'Apply irrigation at 25-30 day intervals',
                        'Apply second dose of nitrogen at 40 DAS',
                        'Control weeds by hand weeding or herbicides',
                        'Monitor for bollworm and sucking pests'
                    ]
                },
                {
                    'phase': '🌱 Flowering & Boll Formation (Week 9-16)',
                    'steps': [
                        'Apply irrigation at flowering and boll formation',
                        'Apply third dose of nitrogen at flowering',
                        'Control water to prevent boll shedding',
                        'Monitor for diseases like leaf curl virus'
                    ]
                },
                {
                    'phase': '🌱 Maturity & Harvesting (Week 17-24)',
                    'steps': [
                        'Stop irrigation 15-20 days before harvest',
                        'Harvest when bolls are fully mature and open',
                        'Pick cotton manually or using mechanical picker',
                        'Gin cotton to separate fiber from seeds'
                    ]
                }
            ]
        },
        
        'Sugarcane': {
            'title': '🎋 Sugarcane Cultivation Guide',
            'duration': '12-18 months',
            'steps': [
                {
                    'phase': '🌱 Land Preparation (Week 1-2)',
                    'steps': [
                        'Deep plow the field 2-3 times',
                        'Apply 20-25 tons of farmyard manure per hectare',
                        'Level the field for uniform irrigation',
                        'Prepare furrows at 90-120 cm spacing'
                    ]
                },
                {
                    'phase': '🌱 Planting (Week 3-4)',
                    'steps': [
                        'Select healthy setts from disease-free plants',
                        'Treat setts with fungicide and biofertilizers',
                        'Plant setts in furrows at 2-3 cm depth',
                        'Apply first dose of nitrogen fertilizer'
                    ]
                },
                {
                    'phase': '🌱 Vegetative Growth (Month 2-6)',
                    'steps': [
                        'Apply irrigation at 10-15 day intervals',
                        'Apply second dose of nitrogen at 60 DAP',
                        'Control weeds by hand weeding or herbicides',
                        'Monitor for top borer and stem borer'
                    ]
                },
                {
                    'phase': '🌱 Grand Growth (Month 7-12)',
                    'steps': [
                        'Apply irrigation at 7-10 day intervals',
                        'Apply third dose of nitrogen at grand growth',
                        'Control water to prevent lodging',
                        'Monitor for diseases like red rot and smut'
                    ]
                },
                {
                    'phase': '🌱 Maturity & Harvesting (Month 13-18)',
                    'steps': [
                        'Stop irrigation 15-20 days before harvest',
                        'Harvest when cane is mature (12-18 months)',
                        'Cut cane close to ground level',
                        'Transport to sugar mill within 24-48 hours'
                    ]
                }
            ]
        },
        
        'Tomato': {
            'title': '🍅 Tomato Cultivation Guide',
            'duration': '90-120 days',
            'steps': [
                {
                    'phase': '🌱 Nursery Preparation (Week 1-2)',
                    'steps': [
                        'Prepare nursery beds with fine soil',
                        'Treat seeds with fungicide and biofertilizers',
                        'Sow seeds at 1 cm depth, 5 cm apart',
                        'Maintain proper moisture in nursery'
                    ]
                },
                {
                    'phase': '🌱 Transplanting (Week 3-4)',
                    'steps': [
                        'Uproot 25-30 day old seedlings carefully',
                        'Transplant at 60x45 cm spacing',
                        'Apply first dose of nitrogen fertilizer',
                        'Provide support with stakes or trellis'
                    ]
                },
                {
                    'phase': '🌱 Vegetative Growth (Week 5-8)',
                    'steps': [
                        'Apply irrigation at 3-5 day intervals',
                        'Apply second dose of nitrogen at 30 DAT',
                        'Control weeds by hand weeding',
                        'Monitor for fruit borer and leaf miner'
                    ]
                },
                {
                    'phase': '🌱 Flowering & Fruit Formation (Week 9-12)',
                    'steps': [
                        'Apply irrigation at 2-3 day intervals',
                        'Apply third dose of nitrogen at flowering',
                        'Control water to prevent fruit cracking',
                        'Monitor for diseases like early blight and late blight'
                    ]
                },
                {
                    'phase': '🌱 Maturity & Harvesting (Week 13-16)',
                    'steps': [
                        'Harvest fruits when fully mature and red',
                        'Pick fruits carefully to avoid damage',
                        'Grade fruits by size and quality',
                        'Store at 10-12°C for longer shelf life'
                    ]
                }
            ]
        },
        
        'Potato': {
            'title': '🥔 Potato Cultivation Guide',
            'duration': '90-120 days',
            'steps': [
                {
                    'phase': '🌱 Land Preparation (Week 1)',
                    'steps': [
                        'Plow the field 2-3 times to fine tilth',
                        'Apply 15-20 tons of farmyard manure per hectare',
                        'Level the field for uniform irrigation',
                        'Prepare ridges at 60 cm spacing'
                    ]
                },
                {
                    'phase': '🌱 Planting (Week 2)',
                    'steps': [
                        'Select healthy seed tubers (30-40 g each)',
                        'Treat tubers with fungicide and biofertilizers',
                        'Plant tubers at 10-12 cm depth in ridges',
                        'Apply first dose of nitrogen fertilizer'
                    ]
                },
                {
                    'phase': '🌱 Vegetative Growth (Week 3-8)',
                    'steps': [
                        'Apply irrigation at 7-10 day intervals',
                        'Apply second dose of nitrogen at 30 DAP',
                        'Control weeds by hand weeding or herbicides',
                        'Monitor for potato tuber moth and aphids'
                    ]
                },
                {
                    'phase': '🌱 Tuber Formation (Week 9-12)',
                    'steps': [
                        'Apply irrigation at 5-7 day intervals',
                        'Apply third dose of nitrogen at tuber formation',
                        'Control water to prevent tuber rot',
                        'Monitor for diseases like late blight and bacterial wilt'
                    ]
                },
                {
                    'phase': '🌱 Maturity & Harvesting (Week 13-16)',
                    'steps': [
                        'Stop irrigation 10-15 days before harvest',
                        'Harvest when vines start drying',
                        'Dig tubers carefully to avoid damage',
                        'Store tubers at 8-10°C for longer shelf life'
                    ]
                }
            ]
        },
        
        'Onion': {
            'title': '🧅 Onion Cultivation Guide',
            'duration': '90-120 days',
            'steps': [
                {
                    'phase': '🌱 Land Preparation (Week 1)',
                    'steps': [
                        'Plow the field 2-3 times to fine tilth',
                        'Apply 10-15 tons of farmyard manure per hectare',
                        'Level the field for uniform irrigation',
                        'Prepare raised beds for better drainage'
                    ]
                },
                {
                    'phase': '🌱 Planting (Week 2)',
                    'steps': [
                        'Select healthy bulbs or seedlings',
                        'Treat with fungicide and biofertilizers',
                        'Plant at 15x10 cm spacing',
                        'Apply first dose of nitrogen fertilizer'
                    ]
                },
                {
                    'phase': '🌱 Vegetative Growth (Week 3-8)',
                    'steps': [
                        'Apply irrigation at 5-7 day intervals',
                        'Apply second dose of nitrogen at 30 DAP',
                        'Control weeds by hand weeding',
                        'Monitor for thrips and onion maggot'
                    ]
                },
                {
                    'phase': '🌱 Bulb Formation (Week 9-12)',
                    'steps': [
                        'Apply irrigation at 3-5 day intervals',
                        'Apply third dose of nitrogen at bulb formation',
                        'Control water to prevent bulb rot',
                        'Monitor for diseases like purple blotch and downy mildew'
                    ]
                },
                {
                    'phase': '🌱 Maturity & Harvesting (Week 13-16)',
                    'steps': [
                        'Stop irrigation 7-10 days before harvest',
                        'Harvest when tops start falling',
                        'Cure bulbs in sunlight for 3-5 days',
                        'Store bulbs in well-ventilated place'
                    ]
                }
            ]
        }
    }
    
    # Get guide for the specific crop
    guide = growing_guides.get(crop_name, None)
    
    if not guide:
        # Return a comprehensive generic guide for unknown crops
        guide = {
            'title': f'🌱 {crop_name} Cultivation Guide - Complete Process',
            'duration': '90-120 days',
            'overview': f'{crop_name} cultivation requires proper planning, timely operations, and careful management for optimal yields.',
            'steps': [
                {
                    'phase': '🌱 Phase 1: Land Preparation (Week 1)',
                    'description': 'Proper land preparation ensures good seed-soil contact and uniform crop establishment.',
                    'detailed_steps': [
                        {
                            'step': '1.1 Field Assessment',
                            'points': [
                                '• Check soil moisture and texture',
                                '• Test soil pH and nutrient status',
                                '• Assess previous crop residues',
                                '• Plan field layout and irrigation'
                            ]
                        },
                        {
                            'step': '1.2 Soil Preparation',
                            'points': [
                                '• Plow field 2-3 times to fine tilth',
                                '• Break soil clods to appropriate size',
                                '• Remove crop residues and weeds',
                                '• Level field for uniform irrigation'
                            ]
                        },
                        {
                            'step': '1.3 Manure Application',
                            'points': [
                                '• Apply 10-15 tons farmyard manure per hectare',
                                '• Spread manure evenly across field',
                                '• Mix manure with top soil layer',
                                '• Allow time for decomposition'
                            ]
                        },
                        {
                            'step': '1.4 Final Preparation',
                            'points': [
                                '• Prepare seedbed with proper moisture',
                                '• Create irrigation channels if needed',
                                '• Mark field boundaries clearly',
                                '• Ensure uniform field conditions'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 2: Sowing/Planting (Week 2)',
                    'description': 'Proper sowing/planting ensures uniform crop stand and optimal plant population.',
                    'detailed_steps': [
                        {
                            'step': '2.1 Seed/Planting Material Preparation',
                            'points': [
                                '• Select quality seeds or planting material',
                                '• Treat with appropriate chemicals',
                                '• Apply biofertilizers if needed',
                                '• Calculate proper seed rate'
                            ]
                        },
                        {
                            'step': '2.2 Sowing/Planting Method',
                            'points': [
                                '• Use appropriate sowing/planting method',
                                '• Maintain proper depth and spacing',
                                '• Ensure good seed-soil contact',
                                '• Apply initial fertilizers'
                            ]
                        },
                        {
                            'step': '2.3 Initial Care',
                            'points': [
                                '• Apply light irrigation if needed',
                                '• Monitor for uniform germination',
                                '• Control early weed growth',
                                '• Protect from pests and birds'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 3: Vegetative Growth (Week 3-8)',
                    'description': 'This phase focuses on plant growth, root development, and early management.',
                    'detailed_steps': [
                        {
                            'step': '3.1 Irrigation Management',
                            'points': [
                                '• Apply irrigation at appropriate intervals',
                                '• Maintain proper soil moisture',
                                '• Avoid waterlogging or drought stress',
                                '• Monitor soil moisture regularly'
                            ]
                        },
                        {
                            'step': '3.2 Fertilizer Application',
                            'points': [
                                '• Apply fertilizers at recommended stages',
                                '• Use split application for better efficiency',
                                '• Monitor for nutrient deficiencies',
                                '• Apply micronutrients if needed'
                            ]
                        },
                        {
                            'step': '3.3 Weed Control',
                            'points': [
                                '• Apply herbicides or manual weeding',
                                '• Remove weeds at early stages',
                                '• Maintain weed-free field',
                                '• Monitor for new weed growth'
                            ]
                        },
                        {
                            'step': '3.4 Pest and Disease Monitoring',
                            'points': [
                                '• Monitor for common pests and diseases',
                                '• Use appropriate control measures',
                                '• Apply preventive sprays if needed',
                                '• Maintain proper field hygiene'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 4: Reproductive Phase (Week 9-12)',
                    'description': 'Critical phase for flowering, fruit formation, and yield development.',
                    'detailed_steps': [
                        {
                            'step': '4.1 Water Management',
                            'points': [
                                '• Apply irrigation at critical growth stages',
                                '• Maintain adequate moisture during flowering',
                                '• Avoid water stress during fruit formation',
                                '• Control irrigation to prevent lodging'
                            ]
                        },
                        {
                            'step': '4.2 Nutrient Management',
                            'points': [
                                '• Apply fertilizers at recommended stages',
                                '• Monitor for nutrient deficiencies',
                                '• Avoid late fertilizer application',
                                '• Assess crop health and vigor'
                            ]
                        },
                        {
                            'step': '4.3 Disease and Pest Management',
                            'points': [
                                '• Monitor for diseases and pests',
                                '• Apply appropriate control measures',
                                '• Maintain proper field hygiene',
                                '• Use integrated pest management'
                            ]
                        },
                        {
                            'step': '4.4 Growth Monitoring',
                            'points': [
                                '• Monitor plant growth and development',
                                '• Check for uniform flowering',
                                '• Assess crop health and vigor',
                                '• Plan harvesting operations'
                            ]
                        }
                    ]
                },
                {
                    'phase': '🌱 Phase 5: Maturity & Harvesting (Week 13-16)',
                    'description': 'Proper timing and method of harvesting ensure maximum yield and quality.',
                    'detailed_steps': [
                        {
                            'step': '5.1 Maturity Assessment',
                            'points': [
                                '• Monitor maturity indicators',
                                '• Check moisture content',
                                '• Assess harvest readiness',
                                '• Plan harvest timing'
                            ]
                        },
                        {
                            'step': '5.2 Pre-Harvest Preparation',
                            'points': [
                                '• Stop irrigation before harvest',
                                '• Prepare harvesting equipment',
                                '• Arrange labor and storage',
                                '• Plan post-harvest handling'
                            ]
                        },
                        {
                            'step': '5.3 Harvesting Process',
                            'points': [
                                '• Harvest at appropriate maturity stage',
                                '• Use appropriate harvesting method',
                                '• Handle harvested produce carefully',
                                '• Minimize harvest losses'
                            ]
                        },
                        {
                            'step': '5.4 Post-Harvest Handling',
                            'points': [
                                '• Clean and grade produce',
                                '• Dry to appropriate moisture content',
                                '• Store in proper conditions',
                                '• Prevent post-harvest losses'
                            ]
                        }
                    ]
                }
            ]
        }
    
    return guide

def explain_crop_suitability(input_crop, recommended_crop, feats):
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