# app/utils/knowledge_based_ckd_checker.py

def knowledge_based_ckd_checker(inputs):
    """
    knowledge-based Chronic Kidney Disease checker using medically accepted thresholds.
    Returns:
        - 'CKD' or 'Not CKD'
        - List of reasons (violated clinical indicators)
    """

    abnormal_flags = 0
    reasons = []

    # 1. Serum Creatinine [Normal: ~0.6 – 1.2 mg/dL]
    if inputs['serum_creatinine'] > 1.2:
        abnormal_flags += 1
        reasons.append("High Serum Creatinine (>1.2 mg/dL)")

    # 2. Specific Gravity [Normal: 1.005 – 1.030]
    if inputs['specific_gravity'] < 1.005 or inputs['specific_gravity'] > 1.030:
        abnormal_flags += 1
        reasons.append("Abnormal Urine Specific Gravity (Outside 1.005–1.030)")

    # 3. Albumin [Normal: 3.4 – 5.4 g/dL]
    if inputs['albumin'] < 3.4:
        abnormal_flags += 1
        reasons.append("Low Albumin (<3.4 g/dL)")

    # 4. Haemoglobin [Normal: ≥13.5 g/dL for men, ≥12 g/dL for women]
    # Assuming average threshold for both sexes:
    if inputs['haemoglobin'] < 12.0:
        abnormal_flags += 1
        reasons.append("Low Hemoglobin (<12 g/dL)")

    # 5. Red Blood Cell Count [Normal: ~4.7 – 6.1 million cells/µL for men]
    if inputs['red_blood_cell_count'] < 4.7:
        abnormal_flags += 1
        reasons.append("Low RBC Count (<4.7 million/µL)")

    # 6. Packed Cell Volume [Normal: 40–50% (men), 35–45% (women)]
    if inputs['packed_cell_volume'] < 35:
        abnormal_flags += 1
        reasons.append("Low Packed Cell Volume (<35%)")

    # 7. Blood Urea (BUN) [Normal: 7 – 20 mg/dL]
    if inputs['blood_urea'] > 20:
        abnormal_flags += 1
        reasons.append("High Blood Urea (>20 mg/dL)")

    # 8. Blood Glucose Random [Normal: 70 – 140 mg/dL]
    if inputs['blood_glucose_random'] > 200:
        abnormal_flags += 1
        reasons.append("Very High Random Blood Glucose (>200 mg/dL)")

    # 9. Diabetes Mellitus
    if inputs['diabetes_mellitus'] == 1:
        abnormal_flags += 1
        reasons.append("Diabetes Present")

    # Final knowledge: if 3 or more abnormal indicators are present
    if abnormal_flags >= 3:
        return "CKD", reasons
    else:
        return "Not CKD", reasons
