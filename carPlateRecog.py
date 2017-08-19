# %%
import time
import openalpr_api
from openalpr_api.rest import ApiException
from pprint import pprint

# %%


def CallAPI(image_path):
    """
    Input image path
    return plate number
    """
# create an instance of the API class
    api_instance = openalpr_api.DefaultApi()
    # file | The image file that you wish to analyze
    image = image_path
    # str | The secret key used to authenticate your account.  You can view your  secret key by visiting  https://cloud.openalpr.com/
    secret_key = 'sk_5ea09962b11521cae432ecfe'
    country = 'au'  # str | Defines the training data used by OpenALPR.  \"us\" analyzes  North-American style plates.  \"eu\" analyzes European-style plates.  This field is required if using the \"plate\" task  You may use multiple datasets by using commas between the country  codes.  For example, 'au,auwide' would analyze using both the  Australian plate styles.  A full list of supported country codes  can be found here https://github.com/openalpr/openalpr/tree/master/runtime_data/config
    # int | If set to 1, the vehicle will also be recognized in the image This requires an additional credit per request  (optional) (default to 0)
    recognize_vehicle = 0
    # str | Corresponds to a US state or EU country code used by OpenALPR pattern  recognition.  For example, using \"md\" matches US plates against the  Maryland plate patterns.  Using \"fr\" matches European plates against  the French plate patterns.  (optional) (default to )
    state = ''
    # int | If set to 1, the image you uploaded will be encoded in base64 and  sent back along with the response  (optional) (default to 0)
    return_image = 0
    # int | The number of results you would like to be returned for plate  candidates and vehicle classifications  (optional) (default to 10)
    topn = 10
    # str | Prewarp configuration is used to calibrate the analyses for the  angle of a particular camera.  More information is available here http://doc.openalpr.com/accuracy_improvements.html#calibration  (optional) (default to )
    prewarp = ''

    try:
        api_response = api_instance.recognize_file(
            image, secret_key, country, recognize_vehicle=recognize_vehicle, state=state, return_image=return_image, topn=topn, prewarp=prewarp)
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->recognize_file: %s\n" % e)

    # pprint(api_response.results)
    unpacklist = api_response.results
    result = []

    for i in unpacklist:
        result.append(i.plate)

    return result[0]

    # resultdict = {'carNum': result[0],
    #               'parkingLotNum': '001'}

# %%


def GetJsonDict(plates_prev, plates_next):
    """
    Return: dictionary
    If plates_next is empty string, return previous plates as leaving plate.
    Otherwise return as parking plate
    """
    if plates_next:  # If there is a plate number
        resultdict = {
            'carNum': plates_next,
            'parkingLotNum': '001',
        }
    else:
        resultdict = {
            'carNum': plates_prev,
            'parkingLotNum': '001',
        }
    return resultdict


def Sendconflict(plates_prev, plates_next):
    """
    Resolve conflict
    """
    leavingDict = {
        'carNum': plates_prev,
        'parkingLotNum': '001',
    }
    startingDict = {
        'carNum': plates_next,
        'parkingLotNum': '001',
    }
    # Leaving
    ParkAPI(True, leavingDict)
    # Starting
    ParkAPI(False, startingDict)


def IsLeaving(plates_next):
    """
    Return: Boolean
    If a car is leaving, return True. Otherwise return False.
    """
    if not plates_next:
        return True
    else:
        return False


def IsChanged(plates_next, plates_prev):
    """
    Return: Boolean
    If plate is changed, return True. Otherwise return False.
    """
    if plates_next != plates_prev:
        return True
    else:
        return False


def ParkAPI(IsLeaving, resultdict):
    """
    POST resultdict to start/leaving based on Boolean IsLeaving
    """
    payload = resultdict
    headers = {'content-type': 'application/json'}
    if IsLeaving:
        url = 'http://10.1.0.154:8000/api/parking/leave'
    else:
        url = 'http://10.1.0.154:8000/api/parking/start'
    response = requests.post(url, data=json.dumps(payload), headers=headers)


# %% Test
Testcase1 = '/Users/benjamin/codeExample/unihackhardware/aussie.jpg'
testNum1 = CallAPI(Testcase1)
Testcase2 = '/Users/benjamin/codeExample/unihackhardware/west.jpg'
testNum2 = CallAPI(Testcase2)
TestNumEmpty = ''
print(testNum1, testNum2)
# Test IsChanged
print(IsChanged(testNum1, testNum2))
# Test IsLeaving
print(IsLeaving(TestNumEmpty))
# Test GetJsonDict (Leaving)
Num1Leaving = GetJsonDict(testNum1, TestNumEmpty)
Num1Parking = GetJsonDict(TestNumEmpty, testNum1)
Num1LeavingFlag = IsLeaving(TestNumEmpty)
Num1ParkingFlag = IsLeaving(testNum1)
# Test GetJsonDict (Start parking)
Num2Parking = GetJsonDict(TestNumEmpty, testNum2)
Num2Leaving = GetJsonDict(testNum2, TestNumEmpty)
Num2ParkingFlag = IsLeaving(testNum2)
Num2LeavingFlag = IsLeaving(TestNumEmpty)

# Test if end works

testNum3 = 'TESTEND'
Num3Leaving = GetJsonDict(testNum3, TestNumEmpty)
Num3Parking = GetJsonDict(TestNumEmpty, testNum3)
Num3LeavingFlag = IsLeaving(TestNumEmpty)
Num3ParkingFlag = IsLeaving(testNum3)

# %% New Test
# New transaction Car 1 parking leaving
Num1ParkingFlag
Num1LeavingFlag
ParkAPI(Num1ParkingFlag, Num1Parking)
ParkAPI(Num1LeavingFlag, Num1Leaving)
# New transaction Car 2 parking leaving
Num2ParkingFlag
Num2LeavingFlag
ParkAPI(Num2ParkingFlag, Num2Parking)
ParkAPI(Num2LeavingFlag, Num2Leaving)
# New transaction Car3
Num3ParkingFlag
Num3LeavingFlag
ParkAPI(Num3ParkingFlag, Num3Parking)
ParkAPI(Num3LeavingFlag, Num3Leaving)

# %%
# Test conflict
ParkAPI(Num1ParkingFlag, Num1Parking)
Sendconflict(testNum1, testNum2)
