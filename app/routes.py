import os
import joblib
import numpy as np
import random
from flask import Blueprint, request, render_template, session
from app.knowledge_based import knowledge_based_ckd_checker

main = Blueprint('main', __name__)

# Load model
model_path = os.path.join('app', 'model', 'xgboost_ckd_model.pkl')
model = joblib.load(model_path)

@main.route('/', methods=['GET'])
def home():
    names = ["John Chege", "Lucy Mwangi", "Brian Otieno", "Faith Wanjiku", "Kevin Kiptoo"]
    form_values = {
        "patient_name": random.choice(names),
        "age": random.randint(18, 75),
        "serum_creatinine": round(random.uniform(0.6, 2.5), 2),
        "specific_gravity": round(random.uniform(1.005, 1.030), 3),
        "albumin": round(random.uniform(2.0, 5.5), 1),
        "haemoglobin": round(random.uniform(10.0, 17.0), 1),
        "diabetes_mellitus": random.choice([0, 1]),
        "red_blood_cell_count": round(random.uniform(3.5, 6.1), 2),
        "packed_cell_volume": round(random.uniform(30.0, 50.0), 1),
        "blood_glucose_random": random.randint(70, 200),
        "blood_urea": random.randint(7, 45)
    }
    return render_template("index.html", form_values=form_values)


@main.route('/predict', methods=['POST'])
def predict():
    try:
        # Default values
        default_values = {
            'age': 40, 'blood_pressure': 80, 'specific_gravity': 1.02, 'albumin': 0, 'sugar': 0,
            'red_blood_cells': 1, 'pus_cell': 1, 'pus_cell_clumps': 0, 'bacteria': 0,
            'blood_glucose_random': 100, 'blood_urea': 30, 'serum_creatinine': 1.1, 'sodium': 135,
            'potassium': 4.5, 'haemoglobin': 15, 'packed_cell_volume': 42,
            'white_blood_cell_count': 8000, 'red_blood_cell_count': 5.0, 'hypertension': 0,
            'diabetes_mellitus': 0, 'coronary_artery_disease': 0, 'appetite': 1,
            'peda_edema': 0, 'aanemia': 0
        }

        # Get form data
        patient_name = request.form.get('patient_name', 'Unknown')
        patient_age = float(request.form.get('age', 0))

        form_updates = {
            'serum_creatinine': float(request.form.get('serum_creatinine', 0)),
            'specific_gravity': float(request.form.get('specific_gravity', 0)),
            'albumin': float(request.form.get('albumin', 0)),
            'haemoglobin': float(request.form.get('haemoglobin', 0)),
            'diabetes_mellitus': int(request.form.get('diabetes_mellitus', 0)),
            'red_blood_cell_count': float(request.form.get('red_blood_cell_count', 0)),
            'packed_cell_volume': float(request.form.get('packed_cell_volume', 0)),
            'blood_glucose_random': float(request.form.get('blood_glucose_random', 0)),
            'blood_urea': float(request.form.get('blood_urea', 0)),
            'age': patient_age
        }

        default_values.update(form_updates)

        # Knowledge-based logic
        knowledge_result, knowledge_reasons = knowledge_based_ckd_checker(default_values)

        # Model prediction
        input_data = np.array([[default_values[f] for f in default_values]])
        model_pred = model.predict(input_data)[0]
        model_result = "CKD" if model_pred == 0 else "Not CKD"
        final_decision = knowledge_result

        decision_msg = "✅ Chronic Kidney Disease (CKD)" if final_decision == "CKD" else "🟢 Not CKD (Normal)"
        display_values = [(k.replace('_', ' ').title(), default_values[k]) for k in form_updates]

        # Save to session
        session['patient_name'] = patient_name
        session['patient_age'] = patient_age
        session['prediction'] = decision_msg
        session['values'] = display_values
        session['knowledge_based_reasons'] = knowledge_reasons
        session['model_decision'] = model_result

        return render_template(
            'result.html',
            prediction=decision_msg,
            values=display_values,
            patient_name=patient_name,
            patient_age=patient_age,
            knowledge_based_reasons=knowledge_reasons,
            model_decision=model_result
        )

    except Exception as e:
        return render_template(
            'result.html',
            prediction=f"❌ Error: {str(e)}",
            values=[], patient_name="", patient_age="", knowledge_based_reasons=[], model_decision="Unknown"
        )


@main.route('/explain', methods=['GET'])
def explain():
    reasons = session.get('knowledge_based_reasons', [])
    patient_name = session.get('patient_name', 'Unknown')
    return render_template('explain.html', reasons=reasons, patient_name=patient_name)
