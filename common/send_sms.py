import africastalking
username = "sandbox"
api_key = "71ff11abb324c6ada2759141f51739fb05ca0c95b1f6f9bf28dc0a193f988e9b"
africastalking.initialize(username, api_key)

sms = africastalking.SMS

def send():
    recipients = ["+254727531734"]
    message = "Assalaam aleikum"
    sender = "SMS-SALAD"
    try:
        response = sms.send(message,recipients,)
        print (response)
    except Exception as e:
        print (f'Hello, we have a problem: {e}')
send()