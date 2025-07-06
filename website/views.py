from django.shortcuts import render
import os
import joblib
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.preprocessing import LabelEncoder
from django.core.mail import send_mail
from django.conf import settings
import json
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

# Create your views here.

# Define crops list first
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

# Initialize LabelEncoder
le_crop = LabelEncoder()
le_crop.fit(crops)

def load_crop_model():
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'crop_model.pkl')
    return joblib.load(model_path)

@csrf_exempt
def predict_crop(request):
    if request.method == 'POST':
        try:
            crop_name = request.POST.get('crop_name', '')
            season = request.POST.get('season', '')
            location = request.POST.get('location', '')
            
            if not all([crop_name, season, location]):
                return render(request, 'website/result.html', {'error': 'Please fill all fields'})
            
            # Generate realistic data based on season and location
            weather_data = generate_weather_data(season, location)
            
            # Load models with error handling
            try:
                crop_model = load_crop_model()
                fert_model = joblib.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'fertilizer_model.pkl'))
                soil_model = joblib.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'soil_health_model.pkl'))
            except Exception as e:
                return render(request, 'website/result.html', {'error': f'Model loading error: {str(e)}'})
            
            # Make predictions with generated data
            crop_input = np.array([[
                weather_data['N'], weather_data['P'], weather_data['K'],
                weather_data['temperature'], weather_data['humidity'],
                weather_data['ph'], weather_data['rainfall'], weather_data['region_enc']
            ]])
            
            crop_pred = crop_model.predict(crop_input)[0]
            predicted_crop = crops[int(crop_pred)] if int(crop_pred) < len(crops) else f"Crop #{crop_pred}"
            
            # Fertilizer prediction
            try:
                crop_enc = le_crop.transform([crop_name])[0] if crop_name in crops else 0
                fert_input = np.array([[crop_enc, weather_data['N'], weather_data['P'], weather_data['K'], weather_data['ph'], weather_data['region_enc']]])
                fert_pred = fert_model.predict(fert_input)[0]
                fertilizers = ['Urea', 'DAP', 'MOP', 'SSP', 'Compost', 'Vermicompost', 'NPK', 'Ammonium Sulphate']
                fertilizer_name = fertilizers[int(fert_pred)] if int(fert_pred) < len(fertilizers) else "NPK"
            except:
                fertilizer_name = "NPK"
            
            # Soil health prediction
            try:
                soil_input = np.array([[weather_data['N'], weather_data['P'], weather_data['K'], weather_data['ph'], np.clip(100/50, 0.5, 3.5), weather_data['region_enc']]])
                soil_pred = soil_model.predict(soil_input)[0]
                soil_status = ['Good', 'Moderate', 'Poor']
                soil_health = soil_status[int(soil_pred)] if int(soil_pred) < len(soil_status) else "Good"
            except:
                soil_health = "Good"
            
            # Suitability analysis
            suitability_score = analyze_crop_suitability(crop_name, predicted_crop, weather_data)
            
            # Get weather dashboard
            weather_dashboard = get_weather_dashboard(location, season)
            
            context = {
                'selected_crop': crop_name,
                'predicted_crop': predicted_crop,
                'season': season,
                'location': location,
                'fertilizer': fertilizer_name,
                'soil_health': soil_health,
                'suitability_score': suitability_score,
                'weather_data': weather_data,
                'weather_dashboard': weather_dashboard,
                'analysis': get_crop_analysis(crop_name, season, location, weather_data)
            }
            
            return render(request, 'website/result.html', context)
        except Exception as e:
            return render(request, 'website/result.html', {'error': f'Prediction error: {str(e)}'})
    elif request.method == 'GET':
        try:
            crop_name = request.GET.get('crop_name', '')
            season = request.GET.get('season', '')
            location = request.GET.get('location', '')
            
            if not all([crop_name, season, location]):
                return JsonResponse({'error': 'Missing required parameters'})
            
            weather_data = generate_weather_data(season, location)
            crop_model = load_crop_model()
            crop_input = np.array([[
                weather_data['N'], weather_data['P'], weather_data['K'],
                weather_data['temperature'], weather_data['humidity'],
                weather_data['ph'], weather_data['rainfall'], weather_data['region_enc']
            ]])
            crop_pred = crop_model.predict(crop_input)[0]
            predicted_crop = crops[int(crop_pred)] if int(crop_pred) < len(crops) else f"Crop #{crop_pred}"
            
            return JsonResponse({
                'selected_crop': crop_name,
                'predicted_crop': predicted_crop,
                'weather_data': weather_data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only GET and POST methods are allowed.'})

def generate_weather_data(season, location):
    """Generate realistic weather and soil data based on season and location"""
    import random
    
    # Season-based temperature ranges
    season_temps = {
        'Kharif': (25, 35),
        'Rabi': (15, 25),
        'Zaid': (30, 40),
        'Spring': (20, 30),
        'Summer': (30, 40),
        'Autumn': (15, 25),
        'Winter': (10, 20)
    }
    
    # Season-based rainfall ranges
    season_rainfall = {
        'Kharif': (150, 300),
        'Rabi': (50, 150),
        'Zaid': (20, 100),
        'Spring': (80, 200),
        'Summer': (100, 250),
        'Autumn': (60, 180),
        'Winter': (30, 120)
    }
    
    temp_range = season_temps.get(season, (20, 30))
    rainfall_range = season_rainfall.get(season, (100, 200))
    
    return {
        'N': random.randint(80, 150),
        'P': random.randint(30, 80),
        'K': random.randint(30, 80),
        'temperature': round(random.uniform(*temp_range), 1),
        'humidity': round(random.uniform(40, 90), 1),
        'ph': round(random.uniform(6.0, 7.5), 1),
        'rainfall': round(random.uniform(*rainfall_range), 1),
        'region_enc': random.randint(0, 10)
    }

def analyze_crop_suitability(selected_crop, predicted_crop, weather_data):
    """Analyze how suitable the selected crop is for the given conditions"""
    if selected_crop == predicted_crop:
        return "Excellent"
    elif selected_crop in crops and predicted_crop in crops:
        return "Good"
    else:
        return "Moderate"

def get_crop_analysis(crop_name, season, location, weather_data):
    """Get detailed analysis for the crop"""
    return [
        {
            'title': '🌱 Planting Guide',
            'description': f'Plant {crop_name} seeds 2-3 cm deep in well-drained soil. Space plants 30-45 cm apart for optimal growth. Best planting time: {get_planting_time(season)}.'
        },
        {
            'title': '💧 Watering Schedule',
            'description': f'Water deeply but infrequently. Allow soil to dry slightly between waterings. Current rainfall: {weather_data["rainfall"]}mm - {"Adequate" if weather_data["rainfall"] > 100 else "Supplemental irrigation needed"}.'
        },
        {
            'title': '🌡️ Temperature Management',
            'description': f'Optimal temperature range for {crop_name}: 20-30°C. Current temperature: {weather_data["temperature"]}°C - {"Optimal" if 20 <= weather_data["temperature"] <= 30 else "Monitor closely"}.'
        },
        {
            'title': '🛡️ Pest Control',
            'description': f'Monitor for common pests like aphids, caterpillars, and beetles. Use organic pesticides when necessary. Current humidity: {weather_data["humidity"]}% - {"High pest risk" if weather_data["humidity"] > 80 else "Moderate risk"}.'
        },
        {
            'title': '🌿 Fertilization',
            'description': f'Apply balanced fertilizer at planting and flowering stages. Soil pH: {weather_data["ph"]} - {"Optimal" if 6.0 <= weather_data["ph"] <= 7.0 else "Consider pH adjustment"}.'
        },
        {
            'title': '📅 Harvest Timeline',
            'description': f'Expected harvest time: {get_harvest_time(season)}. Monitor crop maturity indicators for optimal harvest timing.'
        }
    ]

def get_planting_time(season):
    """Get optimal planting time for the season"""
    planting_times = {
        'Kharif': 'June-July',
        'Rabi': 'October-November',
        'Zaid': 'March-April',
        'Spring': 'March-April',
        'Summer': 'May-June',
        'Autumn': 'September-October',
        'Winter': 'December-January'
    }
    return planting_times.get(season, 'Year-round')

def get_harvest_time(season):
    """Get harvest time based on season"""
    harvest_times = {
        'Kharif': 'October-November',
        'Rabi': 'March-April',
        'Zaid': 'May-June',
        'Spring': 'May-June',
        'Summer': 'August-September',
        'Autumn': 'November-December',
        'Winter': 'February-March'
    }
    return harvest_times.get(season, '90-120 days after planting')

def get_weather_dashboard(location, season):
    """Generate a comprehensive weather dashboard for the location and season"""
    import random
    
    weather_data = generate_weather_data(season, location)
    
    # Generate additional weather metrics
    wind_speed = round(random.uniform(5, 25), 1)
    uv_index = random.randint(1, 11)
    air_quality = random.choice(['Good', 'Moderate', 'Poor'])
    visibility = random.randint(5, 15)
    
    # Season-specific insights
    season_insights = {
        'Kharif': {
            'description': 'Monsoon season with high humidity and rainfall',
            'tips': ['Ensure proper drainage', 'Monitor for fungal diseases', 'Use disease-resistant varieties'],
            'risks': ['Flooding', 'Pest outbreaks', 'Disease spread']
        },
        'Rabi': {
            'description': 'Winter season with moderate temperatures',
            'tips': ['Protect from frost', 'Use cold-resistant varieties', 'Maintain soil moisture'],
            'risks': ['Frost damage', 'Water scarcity', 'Cold stress']
        },
        'Zaid': {
            'description': 'Summer season with high temperatures',
            'tips': ['Provide shade', 'Increase irrigation', 'Use heat-tolerant varieties'],
            'risks': ['Heat stress', 'Water evaporation', 'Pest pressure']
        }
    }
    
    insight = season_insights.get(season, {
        'description': 'Moderate growing conditions',
        'tips': ['Monitor soil moisture', 'Regular pest control', 'Balanced fertilization'],
        'risks': ['Weather variability', 'Pest pressure', 'Nutrient deficiency']
    })
    
    return {
        'current_temp': weather_data['temperature'],
        'humidity': weather_data['humidity'],
        'rainfall': weather_data['rainfall'],
        'wind_speed': wind_speed,
        'uv_index': uv_index,
        'air_quality': air_quality,
        'visibility': visibility,
        'season_insight': insight,
        'forecast': generate_weather_forecast(season)
    }

def generate_weather_forecast(season):
    """Generate a 7-day weather forecast"""
    import random
    
    forecast = []
    base_temp = {'Kharif': 30, 'Rabi': 20, 'Zaid': 35, 'Spring': 25, 'Summer': 35, 'Autumn': 20, 'Winter': 15}.get(season, 25)
    
    for day in range(7):
        temp_variation = random.uniform(-5, 5)
        temp = round(base_temp + temp_variation, 1)
        humidity = random.randint(40, 90)
        rainfall_chance = random.randint(0, 100)
        wind = round(random.uniform(3, 20), 1)
        
        forecast.append({
            'day': f'Day {day + 1}',
            'temperature': temp,
            'humidity': humidity,
            'rainfall_chance': rainfall_chance,
            'wind_speed': wind,
            'condition': get_weather_condition(temp, humidity, rainfall_chance)
        })
    
    return forecast

def get_weather_condition(temp, humidity, rainfall_chance):
    """Determine weather condition based on parameters"""
    if rainfall_chance > 70:
        return 'Rainy'
    elif temp > 35:
        return 'Hot'
    elif temp < 10:
        return 'Cold'
    elif humidity > 80:
        return 'Humid'
    else:
        return 'Clear'

def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def facts(request):
    return render(request, 'website/facts.html')

def gallery(request):
    return render(request, 'website/gallery.html')

def features(request):
    return render(request, 'website/features.html')

@csrf_exempt
def send_contact_email(request):
    """
    Handle contact form submissions and send emails
    """
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Extract form data
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            subject = data.get('subject', '').strip()
            message = data.get('message', '').strip()
            
            # Validate required fields
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required.'
                }, status=400)
            
            # Validate email format
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_regex, email):
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a valid email address.'
                }, status=400)
            
            # Validate field lengths
            if len(name) < 2:
                return JsonResponse({
                    'success': False,
                    'message': 'Name must be at least 2 characters long.'
                }, status=400)
            
            if len(subject) < 5:
                return JsonResponse({
                    'success': False,
                    'message': 'Subject must be at least 5 characters long.'
                }, status=400)
            
            if len(message) < 10:
                return JsonResponse({
                    'success': False,
                    'message': 'Message must be at least 10 characters long.'
                }, status=400)
            
            # Send email to admin
            try:
                # For console backend, we'll use a simple email format
                admin_email_subject = f"AgroGPT Contact Form: {subject}"
                admin_email_body = f"""
New contact form submission from AgroGPT website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This email was sent from the AgroGPT contact form.
                """
                
                send_mail(
                    subject=admin_email_subject,
                    message=admin_email_body,
                    from_email='noreply@agrogpt.com',
                    recipient_list=['admin@agrogpt.com'],  # This will show in console
                    fail_silently=False,
                )
                
                # Send confirmation email to user
                confirmation_subject = "Thank you for contacting AgroGPT"
                confirmation_body = f"""
Dear {name},

Thank you for contacting AgroGPT! We have received your message and will get back to you as soon as possible.

Your message details:
Subject: {subject}
Message: {message}

We typically respond within 24-48 hours.

Best regards,
The AgroGPT Team

---
This is an automated response. Please do not reply to this email.
                """
                
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_body,
                    from_email='noreply@agrogpt.com',
                    recipient_list=[email],
                    fail_silently=True,  # Don't fail if user email fails
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Message sent successfully! We\'ll get back to you soon.'
                })
                
            except Exception as e:
                print(f"Email sending error: {e}")
                return JsonResponse({
                    'success': False,
                    'message': f'Email configuration error: {str(e)}'
                }, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid data format.'
            }, status=400)
        except Exception as e:
            print(f"Contact form error: {e}")
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

