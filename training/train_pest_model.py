import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Set project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
datasets_dir = os.path.join(project_root, 'datasets')
models_dir = os.path.join(project_root, 'models')
visualizations_dir = os.path.join(project_root, 'visualizations')

# 1. Generate synthetic dataset for pest/disease alerts
np.random.seed(42)
N = 20000

crops = ['Wheat', 'Rice', 'Maize', 'Barley', 'Cotton', 'Sugarcane', 'Soybean', 'Groundnut', 'Bajra', 'Jowar']
regions = ['Punjab', 'Haryana', 'UP', 'MP', 'Bihar', 'Maharashtra', 'WB', 'AP', 'TN', 'Gujarat']
pests = ['None', 'Rust Fungus', 'Stem Borer', 'Aphids', 'Blight', 'Root Rot', 'Leaf Curl', 'Wilt', 'Mosaic Virus']

X = pd.DataFrame({
    'crop': np.random.choice(crops, N),
    'region': np.random.choice(regions, N),
    'month': np.random.randint(1, 13, N),
    'temperature': np.random.uniform(10, 40, N),
    'humidity': np.random.uniform(20, 90, N),
    'rainfall': np.random.uniform(20, 300, N)
})

def assign_pest(row):
    if row['crop'] == 'Wheat' and row['month'] in [1, 2, 12]:
        return 'Rust Fungus'
    elif row['crop'] == 'Rice' and row['humidity'] > 70:
        return 'Blight'
    elif row['crop'] == 'Cotton' and row['temperature'] > 30:
        return 'Aphids'
    elif row['rainfall'] > 200:
        return 'Root Rot'
    elif row['crop'] == 'Maize' and row['month'] in [6, 7, 8]:
        return 'Stem Borer'
    else:
        return np.random.choice(pests)

X['pest_alert'] = X.apply(assign_pest, axis=1)

# Save dataset
os.makedirs(datasets_dir, exist_ok=True)
X.to_csv(os.path.join(datasets_dir, 'pest_data.csv'), index=False)

# Encode categorical features
from sklearn.preprocessing import LabelEncoder
le_crop = LabelEncoder()
le_region = LabelEncoder()
le_pest = LabelEncoder()
X['crop_enc'] = le_crop.fit_transform(X['crop'])
X['region_enc'] = le_region.fit_transform(X['region'])
X['pest_enc'] = le_pest.fit_transform(X['pest_alert'])

features = ['crop_enc', 'region_enc', 'month', 'temperature', 'humidity', 'rainfall']
X_train, X_test, y_train, y_test = train_test_split(
    X[features], X['pest_enc'], test_size=0.2, random_state=42, stratify=X['pest_enc']
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
joblib.dump(best_model, os.path.join(models_dir, 'pest_model.pkl'))

# 4. Save visualizations
os.makedirs(visualizations_dir, exist_ok=True)
# Accuracy bar plot
plt.figure(figsize=(8,5))
accs = [results[m]['accuracy'] for m in models]
sns.barplot(x=list(models.keys()), y=accs)
plt.title('Pest/Disease Alert Model Accuracy')
plt.ylabel('Accuracy')
plt.savefig(os.path.join(visualizations_dir, 'pest_accuracy_plot.png'))
plt.close()

# Confusion matrix for best model
plt.figure(figsize=(10,8))
sns.heatmap(results[best_model_name]['confusion_matrix'], annot=True, fmt='d', cmap='Blues')
plt.title(f'{best_model_name} Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig(os.path.join(visualizations_dir, 'pest_confusion_matrix.png'))
plt.close()

# Classification report as heatmap
cr_df = pd.DataFrame(results[best_model_name]['classification_report']).iloc[:-1, :len(pests)]
sns.heatmap(cr_df, annot=True, cmap='YlGnBu')
plt.title(f'{best_model_name} Classification Report')
plt.savefig(os.path.join(visualizations_dir, 'pest_classification_report.png'))
plt.close()

# ROC Curve (One-vs-Rest)
from sklearn.preprocessing import label_binarize
y_test_bin = label_binarize(y_test, classes=range(len(pests)))
if hasattr(best_model, "predict_proba"):
    y_score = best_model.predict_proba(X_test)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(len(pests)):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc[i] = roc_auc_score(y_test_bin[:, i], y_score[:, i])
    plt.figure(figsize=(8,6))
    for i in range(len(pests)):
        plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve (One-vs-Rest)')
    plt.legend()
    plt.savefig(os.path.join(visualizations_dir, 'pest_roc_curve.png'))
    plt.close()

print(f"Best model: {best_model_name} (Accuracy: {results[best_model_name]['accuracy']:.4f})")
print("All outputs and models saved.") 