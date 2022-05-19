
def checkPressure(bpDict):
    print(bpDict)
    if bpDict['systolic'] == 130 and bpDict['diastolic'] == 89:
        result = "You have Prehypertension. Please Consult a doctor. "
    elif 131 <= bpDict['systolic'] <= 140 and 90 <= bpDict['diastolic'] <= 100:
        result = "You have HBP Stage1. Please Consult a doctor. "
    elif 120 <= bpDict['systolic'] <= 129 and 60 <= bpDict['diastolic'] <= 80:
        result = "Your blood pressure is normal"
    return result
