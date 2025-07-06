import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Set project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datasets_dir = os.path.join(project_root, 'datasets')
models_dir = os.path.join(project_root, 'models')
visualizations_dir = os.path.join(project_root, 'visualizations')

# 1. Generate synthetic dataset for fertilizer suggestion
np.random.seed(42)
N = 20000

fertilizers = ['Urea', 'DAP', 'MOP', 'SSP', 'Compost', 'Vermicompost', 'NPK', 'Ammonium Sulphate']
crops = ['Wheat', 'Rice', 'Maize', 'Barley', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Bajra', 'Jowar']
regions = ['Punjab', 'Haryana', 'UP', 'MP', 'Bihar', 'Maharashtra', 'WB', 'AP', 'TN', 'Gujarat']

X = pd.DataFrame({
    'crop': np.random.choice(crops, N),
    'N': np.random.randint(0, 140, N),
    'P': np.random.randint(5, 145, N),
    'K': np.random.randint(5, 205, N),
    'ph': np.random.uniform(4, 9, N),
    'region': np.random.choice(regions, N)
})

def assign_fertilizer(row):
    if row['crop'] == 'Wheat' and row['N'] < 50:
        return 'Urea'
    elif row['crop'] == 'Rice' and row['P'] < 30:
        return 'DAP'
    elif row['crop'] == 'Cotton' and row['K'] < 60:
        return 'MOP'
    elif row['ph'] < 6:
        return 'SSP'
    elif row['crop'] in ['Soybean', 'Groundnut']:
        return 'Compost'
    elif row['crop'] == 'Sugarcane':
        return 'Ammonium Sulphate'
    else:
        return np.random.choice(fertilizers)

X['fertilizer'] = X.apply(assign_fertilizer, axis=1)

# Save dataset
os.makedirs(datasets_dir, exist_ok=True)
X.to_csv(os.path.join(datasets_dir, 'fertilizer_data.csv'), index=False)

# Encode categorical features
from sklearn.preprocessing import LabelEncoder
le_crop = LabelEncoder()
le_region = LabelEncoder()
le_fert = LabelEncoder()
X['crop_enc'] = le_crop.fit_transform(X['crop'])
X['region_enc'] = le_region.fit_transform(X['region'])
X['fertilizer_enc'] = le_fert.fit_transform(X['fertilizer'])

features = ['crop_enc', 'N', 'P', 'K', 'ph', 'region_enc']
X_train, X_test, y_train, y_test = train_test_split(
    X[features], X['fertilizer_enc'], test_size=0.2, random_state=42, stratify=X['fertilizer_enc']
)

# 2. Train multiple models
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'KNN': KNeighborsClassifier(),
    'LogisticRegression': LogisticRegression(max_iter=200, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred, output_dict=True)
    results[name] = {'model': model, 'accuracy': acc, 'confusion_matrix': cm, 'classification_report': cr}
    print(f"{name} Accuracy: {acc:.4f}")

# 3. Save best model
best_model_name = max(results, key=lambda k: results[k]['accuracy'])
best_model = results[best_model_name]['model']
os.makedirs(models_dir, exist_ok=True)
joblib.dump(best_model, os.path.join(models_dir, 'fertilizer_model.pkl'))

# 4. Save visualizations
os.makedirs(visualizations_dir, exist_ok=True)
# Accuracy bar plot
plt.figure(figsize=(8,5))
accs = [results[m]['accuracy'] for m in models]
sns.barplot(x=list(models.keys()), y=accs)
plt.title('Fertilizer Suggestion Model Accuracy')
plt.ylabel('Accuracy')
plt.savefig(os.path.join(visualizations_dir, 'fertilizer_accuracy_plot.png'))
plt.close()

# Confusion matrix for best model
plt.figure(figsize=(10,8))
sns.heatmap(results[best_model_name]['confusion_matrix'], annot=True, fmt='d', cmap='Blues')
plt.title(f'{best_model_name} Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig(os.path.join(visualizations_dir, 'fertilizer_confusion_matrix.png'))
plt.close()

# Classification report as heatmap
cr_df = pd.DataFrame(results[best_model_name]['classification_report']).iloc[:-1, :len(fertilizers)]
sns.heatmap(cr_df, annot=True, cmap='YlGnBu')
plt.title(f'{best_model_name} Classification Report')
plt.savefig(os.path.join(visualizations_dir, 'fertilizer_classification_report.png'))
plt.close()

print(f"Best model: {best_model_name} (Accuracy: {results[best_model_name]['accuracy']:.4f})")
print("All outputs and models saved.") 