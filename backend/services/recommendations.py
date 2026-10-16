"""General wellness guidance only - not medical advice or treatment."""


def build_recommendations(inputs: dict, risk: dict, accel: float) -> list:
    recs = []
    bmi, act, sleep, smoke = inputs["BMXBMI"], inputs["Physical_Activity"], inputs["Sleep_Category"], inputs["Smoking_Status"]
    sys_, dia, chol = inputs["Mean_Systolic_BP"], inputs["Mean_Diastolic_BP"], inputs["LBXTC"]

    diet = "Maintain a balanced, Mediterranean-style diet rich in vegetables, fruit, whole grains and healthy fats."
    if bmi >= 25 or chol >= 200:
        diet += " Reducing sugary drinks, fried food and processed meat can support healthy weight and cholesterol."
    recs.append(("DIET", diet))

    if act in ("Sedentary", "Lightly Active"):
        recs.append(("EXERCISE", "Build up gradually towards about 150 minutes of moderate activity per week, such as brisk walking, plus 2 strength sessions."))
    else:
        recs.append(("EXERCISE", "Keep up your current activity and add 2 resistance-training sessions per week for muscle and bone health."))

    if sleep in ("Less than 5 hours", "5–7 hours"):
        recs.append(("SLEEP", "Aim for 7–8 hours: keep a regular bedtime, limit screens and caffeine late in the day."))
    elif sleep == "More than 8 hours":
        recs.append(("SLEEP", "Long sleep can be normal, but keep a consistent schedule and mention persistent tiredness to a health professional."))
    else:
        recs.append(("SLEEP", "Protect your current sleep schedule - it is within a healthy range."))

    recs.append(("STRESS", "Try short daily relaxation habits such as breathing exercises, walking outdoors or time with friends."))

    if smoke != "Not at all":
        recs.append(("SMOKING & ALCOHOL", "Reducing or quitting smoking is one of the most helpful changes you can make. Keep alcohol within recommended limits or avoid it."))
    else:
        recs.append(("SMOKING & ALCOHOL", "Staying smoke-free is great. Keep alcohol within recommended limits or avoid it."))

    if sys_ >= 130 or dia >= 80:
        recs.append(("BLOOD PRESSURE", "Your blood pressure entry is above the optimal range. Limit salt and re-check it with a validated monitor."))
    if accel > 2:
        recs.append(("BIOLOGICAL AGE", "Your estimate is above your actual age. Small, steady improvements in activity, sleep and diet are the usual starting points."))

    if risk["label"] in ("High Risk", "Very High Risk"):
        recs.append(("CONSULT A PROFESSIONAL", "Your risk indicator is high. Please consult a qualified healthcare professional to review these values."))
    else:
        recs.append(("CHECK-UPS", "Keep up regular health check-ups so you can track these values over time."))
    return recs
