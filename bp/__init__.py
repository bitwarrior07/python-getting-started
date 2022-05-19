
def checkPressure(bp):
    if 'systolic' == 130 & 'distolic' == 89:
        data = "You have Prehypertension "
    elif 'systolic' == 140 & 'diastolic' == 90:
        data = "You have HBP Stage1 "
    elif 'systolic' == 120 & 'diastolic' == 80:
        data = "Your blood pressure is normal"
    return data
