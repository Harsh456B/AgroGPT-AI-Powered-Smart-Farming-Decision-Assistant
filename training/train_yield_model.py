import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Set project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datasets_dir = os.path.join(project_root, 'datasets')
models_dir = os.path.join(project_root, 'models')
visualizations_dir = os.path.join(project_root, 'visualizations')

# 1. Generate synthetic dataset for crop yield estimation
np.random.seed(42)
N = 20000

crops = ['Wheat', 'Rice', 'Maize', 'Barley', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Bajra', 'Jowar']
regions = ['Punjab', 'Haryana', 'UP', 'MP', 'Bihar', 'Maharashtra', 'WB', 'AP', 'TN', 'Gujarat']

X = pd.DataFrame({
    'crop': np.random.choice(crops, N),
    'region': np.random.choice(regions, N),
    'N': np.random.randint(0, 140, N),
    'P': np.random.randint(5, 145, N),
    'K': np.random.randint(5, 205, N),
    'ph': np.random.uniform(4, 9, N),
    'rainfall': np.random.uniform(20, 300, N),
    'temperature': np.random.uniform(10, 40, N),
    'humidity': np.random.uniform(20, 90, N),
    'fertilizer_amount': np.random.uniform(20, 200, N)
})

# Target: yield (tons/hectare)
def assign_yield(row):
    base = 2.0 + 0.01 * row['N'] + 0.008 * row['P'] + 0.005 * row['K']
    base += 0.02 * row['fertilizer_amount']
    base += 0.01 * (row['rainfall'] - 100)
    base -= 0.05 * abs(row['ph'] - 7)
    base += np.random.normal(0, 0.5)
    return max(0.5, base)

X['yield'] = X.apply(assign_yield, axis=1)

# Save dataset
os.makedirs(datasets_dir, exist_ok=True)
X.to_csv(os.path.join(datasets_dir, 'yield_data.csv'), index=False)

# Encode categorical features
from sklearn.preprocessing import LabelEncoder
le_crop = LabelEncoder()
le_region = LabelEncoder()
X['crop_enc'] = le_crop.fit_transform(X['crop'])
X['region_enc'] = le_region.fit_transform(X['region'])

features = ['crop_enc', 'region_enc', 'N', 'P', 'K', 'ph', 'rainfall', 'temperature', 'humidity', 'fertilizer_amount']
X_train, X_test, y_train, y_test = train_test_split(
    X[features], X['yield'], test_size=0.2, random_state=42
)

# 2. Train multiple regression models
models = {
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(random_state=42),
    'SVR': SVR(),
    'KNN': KNeighborsRegressor(),
    'LinearRegression': LinearRegression()
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    results[name] = {'model': model, 'r2': r2, 'mse': mse, 'y_pred': y_pred}
    print(f"{name} R2 Score: {r2:.4f}, MSE: {mse:.2f}")

# 3. Save best model
best_model_name = max(results, key=lambda k: results[k]['r2'])
best_model = results[best_model_name]['model']
os.makedirs(models_dir, exist_ok=True)
joblib.dump(best_model, os.path.join(models_dir, 'yield_model.pkl'))

# 4. Save visualizations
os.makedirs(visualizations_dir, exist_ok=True)
# R2 bar plot
plt.figure(figsize=(8,5))
r2s = [results[m]['r2'] for m in models]
sns.barplot(x=list(models.keys()), y=r2s)
plt.title('Yield Model R2 Score')
plt.ylabel('R2 Score')
plt.savefig(os.path.join(visualizations_dir, 'yield_r2_plot.png'))
plt.close()

# Actual vs Predicted for best model
plt.figure(figsize=(8,6))
plt.scatter(y_test, results[best_model_name]['y_pred'], alpha=0.3)
plt.xlabel('Actual Yield (tons/ha)')
plt.ylabel('Predicted Yield (tons/ha)')
plt.title(f'{best_model_name} Actual vs Predicted')
plt.savefig(os.path.join(visualizations_dir, 'yield_actual_vs_pred.png'))
plt.close()

print(f"Best model: {best_model_name} (R2: {results[best_model_name]['r2']:.4f})")
print("All outputs and models saved.") 