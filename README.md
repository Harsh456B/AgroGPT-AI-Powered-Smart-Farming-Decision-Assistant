# AgroGPT - AI-Powered Smart Farming Decision Assistant

## 🌱 Overview

AgroGPT is an intelligent farming assistant that leverages machine learning to provide farmers with data-driven insights for better agricultural decisions. The platform offers crop recommendations, fertilizer suggestions, pest management advice, yield predictions, and market price forecasting.

## 🚀 Features

- **Crop Recommendation**: AI-powered suggestions for optimal crop selection based on soil and climate data
- **Fertilizer Management**: Personalized fertilizer recommendations for different crops and soil conditions
- **Pest Detection**: Early warning system for pest identification and management strategies
- **Yield Prediction**: Advanced ML models to predict crop yields based on historical data
- **Price Forecasting**: Market price predictions to help with selling decisions
- **Weather Integration**: Real-time weather data integration for farming decisions
- **Soil Health Analysis**: Comprehensive soil health assessment and recommendations

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Machine Learning**: Scikit-learn, XGBoost, Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Deployment**: Render, Gunicorn, WhiteNoise
- **Database**: SQLite (development), PostgreSQL (production ready)

## 📊 ML Models

The project includes trained models for:
- Crop recommendation (Random Forest)
- Fertilizer recommendation (Random Forest)
- Pest detection (Random Forest)
- Yield prediction (XGBoost)
- Price forecasting (Linear Regression)
- Weather prediction (Linear Regression)
- Soil health assessment (Random Forest)

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

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000/`

### Production Deployment

The application is configured for deployment on Render:

1. **Fork/Clone the repository**
2. **Connect to Render**
3. **Deploy automatically** - Render will detect the `render.yaml` configuration

## 📁 Project Structure

```
AgroGPTWeb/
├── agrogpt_web/          # Django project settings
├── website/              # Main Django app
│   ├── templates/        # HTML templates
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   └── urls.py           # URL routing
├── datasets/             # Training datasets
├── models/               # Trained ML models
├── training/             # Model training scripts
├── visualizations/       # Model performance plots
├── cli_assistant/        # Command-line tools
└── requirements.txt      # Python dependencies
```

## 🤖 ML Model Training

To retrain the models with new data:

```bash
# Train crop recommendation model
python training/train_crop_model.py

# Train fertilizer model
python training/train_fertilizer_model.py

# Train pest detection model
python training/train_pest_model.py

# Train yield prediction model
python training/train_yield_model.py

# Train price forecasting model
python training/train_price_model.py

# Train weather prediction model
python training/train_weather_model.py

# Train soil health model
python training/train_soil_health_model.py
```

## 📈 Model Performance

The models have been trained and validated with the following performance metrics:
- **Crop Recommendation**: High accuracy with comprehensive classification reports
- **Fertilizer Recommendation**: Optimized for different soil conditions
- **Pest Detection**: Early warning system with high precision
- **Yield Prediction**: R² scores showing strong predictive power
- **Price Forecasting**: Market trend analysis with confidence intervals

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key (auto-generated in production)
- `DEBUG`: Set to 'False' in production
- `DATABASE_URL`: Database connection string (for production)

### Static Files

Static files are automatically collected and served using WhiteNoise middleware.

## 📊 Data Sources

The application uses various agricultural datasets including:
- Crop recommendation data
- Fertilizer requirement data
- Pest identification data
- Historical yield data
- Market price data
- Weather patterns
- Soil health indicators

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Agricultural research institutions for datasets
- Open-source ML community for tools and libraries
- Farmers and agricultural experts for domain knowledge

## 📞 Support

For support and questions, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for the farming community** 