# AgroGPT - AI-Powered Smart Farming Decision Assistant

## 🌱 Overview

AgroGPT is an intelligent farming assistant that leverages machine learning to provide farmers with data-driven recommendations for crop selection, fertilizer usage, pest management, and yield prediction. The system combines multiple AI models to offer comprehensive agricultural insights.

## 🚀 Features

### Core AI Capabilities
- **Crop Recommendation**: Suggests optimal crops based on soil conditions and climate
- **Fertilizer Prediction**: Recommends appropriate fertilizers and application rates
- **Pest Detection**: Identifies potential pest threats and provides management strategies
- **Yield Prediction**: Forecasts crop yields based on historical data and current conditions
- **Price Forecasting**: Predicts crop prices to help with market timing
- **Soil Health Analysis**: Assesses soil quality and provides improvement recommendations
- **Weather Impact Analysis**: Analyzes weather patterns and their effect on farming decisions

### Technical Features
- **Multi-Model AI System**: Combines multiple machine learning models for comprehensive analysis
- **Real-time Processing**: Instant recommendations and predictions
- **User-friendly Interface**: Clean, responsive web interface
- **Data Visualization**: Interactive charts and graphs for better understanding
- **Mobile Responsive**: Works seamlessly on all devices

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: scikit-learn, XGBoost, pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Deployment**: Render, Gunicorn, WhiteNoise
- **Database**: SQLite (development), PostgreSQL (production ready)

## 📊 AI Models Included

1. **Crop Recommendation Model** - Classification model for crop selection
2. **Fertilizer Prediction Model** - Regression model for fertilizer recommendations
3. **Pest Detection Model** - Classification model for pest identification
4. **Yield Prediction Model** - Regression model for yield forecasting
5. **Price Prediction Model** - Time series model for price forecasting
6. **Soil Health Model** - Classification model for soil quality assessment
7. **Weather Impact Model** - Regression model for weather-based predictions

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Harsh456B/AgroGPT-AI-Powered-Smart-Farming-Decision-Assistant.git
   cd AgroGPT-AI-Powered-Smart-Farming-Decision-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000/`

### Production Deployment

The application is configured for deployment on Render:

1. **Fork/Clone this repository**
2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the configuration

3. **Environment Variables** (automatically set by Render):
   - `SECRET_KEY`: Auto-generated
   - `DEBUG`: Set to `False`
   - `ALLOWED_HOSTS`: Configured for `.onrender.com`

## 📁 Project Structure

```
AgroGPTWeb/
├── agrogpt_web/          # Django project settings
├── website/              # Main Django app
│   ├── templates/        # HTML templates
│   ├── static/          # CSS, JS, images
│   └── views.py         # View logic
├── models/              # Trained ML models
├── datasets/            # Training datasets
├── training/            # Model training scripts
├── visualizations/      # Model performance plots
├── cli_assistant/       # Command-line tools
└── requirements.txt     # Python dependencies
```

## 🤖 AI Models Training

The project includes training scripts for all AI models:

- `training/train_crop_model.py` - Crop recommendation model
- `training/train_fertilizer_model.py` - Fertilizer prediction model
- `training/train_pest_model.py` - Pest detection model
- `training/train_yield_model.py` - Yield prediction model
- `training/train_price_model.py` - Price forecasting model
- `training/train_soil_health_model.py` - Soil health model
- `training/train_weather_model.py` - Weather impact model

## 📈 Model Performance

All models have been trained and validated with performance metrics available in the `visualizations/` directory:

- Accuracy plots
- Confusion matrices
- ROC curves
- R² plots for regression models

## 🌐 Live Demo

Visit the deployed application: [AgroGPT on Render](https://agrogpt-web.onrender.com)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset sources: Various agricultural datasets
- ML libraries: scikit-learn, XGBoost
- Web framework: Django
- Deployment platform: Render

## 📞 Support

For support and questions, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for the farming community** 