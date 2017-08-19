import picamera
import datetime
##from threading import thread
from time import sleep

import time
import openalpr_api
from openalpr_api.rest import ApiException
from pprint import pprint


def GetJsonDict(plates_next, plates_prev):
    if not plates_next:  # If there is a plate number
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


def IsLeaving(plates_next):
    if not plates_next:
        return True
    else:
        return False

def IsChanged(plates_next, plates_prev):
    if plates_next != plates_prev:
        return True
    else:
        return False
def Isnone(result,pre_result):
    if  (result==False) and (pre_result == False):
        return 1
    if   result==False:
        return 2
    if  pre_result == False:
        return 3
    else :
        return 0
def ParkAPI(IsLeaving, resultdict):
    payload = resultdict
    headers = {'content-type': 'application/json'}
    if IsLeaving:
        url = 'api/parking/leave'
    else:
        url = 'api/parking/start'
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
def jug(result,prev_result):

    if Isnone(result,prev_result) == 1 :
        return 0
    if Isnone(result,prev_result) == 2 :##leaving
        print('leaving')
        apidata=GetJsonDict()
        ParkAPI(1,apidata)
        return 1
    if Isnone(result,prev_result) == 3 :
        ##coming
        print('coming')
        apidata=GetJsonDict()
        ParkAPI(0,apidata)
        return 1
    else :
        return 0

pre_result=[]
camera = picamera.PiCamera()
i=1
for i in range(3):

    s='image {counter} {timestamp}'
    now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    s=s.format(counter=i,timestamp=now)
    i=i+1
    camera.capture(s+'.jpg')
    sleep(2)

    ##camera.stop_preview()
    ##API part

    # create an instance of the API class
    api_instance = openalpr_api.DefaultApi()
    # file | The image file that you wish to analyze
    image = '/home/pi/fuck/'+s+'.jpg'
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
        ##pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->recognize_file: %s\n" % e)

    ##pprint(api_response.results)

    # %%
    unpacklist = api_response.results
    result = []

    for c in unpacklist:
        result.append(c.plate)
    if result:
        print(result,'gg')
    else:
        print('can\'t recognize')
        
    print(jug(result,pre_result))
    prev_result=result
    
    '''
    if result == False:
        print('no one')
        continue
    '''
    '''
    print('123')
    if Isnone(result,pre_result) == 0
        
        

    
    if (pre_result == False) and (result == False):
        print('nonononono')
        continue
    else:
        print('pass')
        if pre_result == False:
            print('pass 1')
            if result != False:         ##coming
                print('coming')
                apidata=GetJsonDict()
                ParkAPI(0,apidata)
                prev_result=result
                continue
            else:
                print('boring')
                continue                    ##not thing 
        else:
            print('pass 2')
            if result == False   :           ##leaving
                print('leaving')
                apidata=GetJsonDict()
                ParkAPI(1,apidata)
                prev_result=result
                continue
            if result[0] != pre_result[0]:      ##none pass or non-change pass
                print('car change')
            
                prev_result=result
                continue
            else:
                print('boring')
                continue
    '''
   




    ##gg=camera.AWB_MODES
    ##print(gg)
camera.close









# %%

# import urllib2
#
# req = urllib2.Request('api/parking/' + result[0])
# req.add_header('Content-Type', 'application/json')
#
# response = urllib2.urlopen(req)
