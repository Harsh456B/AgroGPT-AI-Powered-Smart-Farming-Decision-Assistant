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

# 1. Generate synthetic dataset for soil health prediction
np.random.seed(42)
N = 20000

regions = ['Punjab', 'Haryana', 'UP', 'MP', 'Bihar', 'Maharashtra', 'WB', 'AP', 'TN', 'Gujarat']
soil_status = ['Good', 'Moderate', 'Poor']

X = pd.DataFrame({
    'N': np.random.randint(0, 140, N),
    'P': np.random.randint(5, 145, N),
    'K': np.random.randint(5, 205, N),
    'ph': np.random.uniform(4, 9, N),
    'organic_matter': np.random.uniform(0.5, 3.5, N),
    'region': np.random.choice(regions, N)
})

def assign_soil_status(row):
    if row['organic_matter'] > 2.5 and 6 < row['ph'] < 7.5:
        return 'Good'
    elif row['organic_matter'] > 1.5:
        return 'Moderate'
    else:
        return 'Poor'

X['soil_status'] = X.apply(assign_soil_status, axis=1)

# Save dataset
os.makedirs(datasets_dir, exist_ok=True)
X.to_csv(os.path.join(datasets_dir, 'soil_health_data.csv'), index=False)

# Encode categorical features
from sklearn.preprocessing import LabelEncoder
le_region = LabelEncoder()
le_status = LabelEncoder()
X['region_enc'] = le_region.fit_transform(X['region'])
X['soil_status_enc'] = le_status.fit_transform(X['soil_status'])

features = ['N', 'P', 'K', 'ph', 'organic_matter', 'region_enc']
X_train, X_test, y_train, y_test = train_test_split(
    X[features], X['soil_status_enc'], test_size=0.2, random_state=42, stratify=X['soil_status_enc']
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
joblib.dump(best_model, os.path.join(models_dir, 'soil_health_model.pkl'))

# 4. Save visualizations
os.makedirs(visualizations_dir, exist_ok=True)
# Accuracy bar plot
plt.figure(figsize=(8,5))
accs = [results[m]['accuracy'] for m in models]
sns.barplot(x=list(models.keys()), y=accs)
plt.title('Soil Health Prediction Model Accuracy')
plt.ylabel('Accuracy')
plt.savefig(os.path.join(visualizations_dir, 'soil_health_accuracy_plot.png'))
plt.close()

# Confusion matrix for best model
plt.figure(figsize=(8,6))
sns.heatmap(results[best_model_name]['confusion_matrix'], annot=True, fmt='d', cmap='Blues')
plt.title(f'{best_model_name} Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig(os.path.join(visualizations_dir, 'soil_health_confusion_matrix.png'))
plt.close()

# Classification report as heatmap
cr_df = pd.DataFrame(results[best_model_name]['classification_report']).iloc[:-1, :len(soil_status)]
sns.heatmap(cr_df, annot=True, cmap='YlGnBu')
plt.title(f'{best_model_name} Classification Report')
plt.savefig(os.path.join(visualizations_dir, 'soil_health_classification_report.png'))
plt.close()

# ROC Curve (One-vs-Rest)
from sklearn.preprocessing import label_binarize
y_test_bin = label_binarize(y_test, classes=range(len(soil_status)))
if hasattr(best_model, "predict_proba"):
    y_score = best_model.predict_proba(X_test)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(len(soil_status)):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc[i] = roc_auc_score(y_test_bin[:, i], y_score[:, i])
    plt.figure(figsize=(8,6))
    for i in range(len(soil_status)):
        plt.plot(fpr[i], tpr[i], label=f'Class {i} (AUC = {roc_auc[i]:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve (One-vs-Rest)')
    plt.legend()
    plt.savefig(os.path.join(visualizations_dir, 'soil_health_roc_curve.png'))
    plt.close()

print(f"Best model: {best_model_name} (Accuracy: {results[best_model_name]['accuracy']:.4f})")
print("All outputs and models saved.") 