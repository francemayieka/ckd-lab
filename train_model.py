# train_model.py
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('data/kidney_disease.csv')
df.drop('id', axis=1, errors='ignore', inplace=True)

# Rename columns
df.columns = ['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba',
              'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv',
              'wc', 'rc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane', 'class']

# Fix types
df['pcv'] = pd.to_numeric(df['pcv'], errors='coerce')
df['wc'] = pd.to_numeric(df['wc'], errors='coerce')
df['rc'] = pd.to_numeric(df['rc'], errors='coerce')

# Clean
df['dm'].replace({'\tno': 'no', '\tyes': 'yes', ' yes': 'yes'}, inplace=True)
df['cad'].replace('\tno', 'no', inplace=True)
df['class'].replace({'ckd\t': 'ckd', 'notckd': 'not ckd'}, inplace=True)
df['class'] = df['class'].map({'ckd': 1, 'not ckd': 0})

# Encode
cat_cols = [col for col in df.columns if df[col].dtype == 'object']
for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)
    df[col] = LabelEncoder().fit_transform(df[col])

df.fillna(df.mean(), inplace=True)

# Train
X = df.drop('class', axis=1)
y = df['class']
X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=0)
model = XGBClassifier()
model.fit(X_train, y_train)

# Save
joblib.dump(model, 'app/model/xgboost_ckd_model.pkl')
print("✅ Model re-trained and saved successfully.")
