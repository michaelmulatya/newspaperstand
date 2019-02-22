import base64
import requests
from requests.auth import HTTPBasicAuth
import datetime



class Mpesa():

    consumer_key = "7l3YMnOYrmI6fz3y9GGqwGin0kunyWtB"
    consumer_secret = "yJpiDMnfdMVU9OQN"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    def __init__(self,domain,till_number):
        self.domain = domain
        self.till_number = till_number


    def register_token(self):
        r = requests.get(self.api_URL, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret)).json()
        token = r.get('access_token')
        print(token)
        return token

    def encodeb64(self):
        time = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        str = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + "20180409093002"
        print(str)
        print('')
        str2 = str.encode('utf-8')
        string = base64.b64encode(str2)
        encoded_string = string.decode('utf-8')
        print(encoded_string)
        return encoded_string



    def reg_urls(self):
        access_token = self.register_token()
        api_url = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = { "ShortCode": "600000",
            "ResponseType": "Completed",
            "ConfirmationURL": "https://"+self.domain+"/c2b/confirmation",
            "ValidationURL": "https://"+self.domain+"/c2b/validation"}
        print('b4 request')
        print(access_token)
        print(request.keys())
        print(request.values())
        print(headers.keys(),headers.values())
        response = requests.post(api_url, json = request, headers=headers)

        print(response.text)
        return response.text

    def transaction(self,amount,phonenumber):
        print(phonenumber)
        access_token = self.register_token()
        password = self.encodeb64()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = { "Authorization": "Bearer %s" % access_token }
        request = {
          "BusinessShortCode": ""+"174379",
          "Password": ""+password,
          "Timestamp": ""+"20180409093002",
          "TransactionType": "CustomerPayBillOnline",
          "Amount": ""+str(amount),
          "PartyA": ""+phonenumber,
          "PartyB": ""+'174379',
          "PhoneNumber": ""+phonenumber,
          "CallBackURL": "https://"+self.domain+"/callback",
          "AccountReference": "Ebook Payment",
          "TransactionDesc": "housing Agent Fee "
        }

        response = requests.post(api_url, json = request, headers=headers)

        print (response.text)

        print (response.text)



# m = Mpesa('http://3b4d7671.ngrok.io:5000',600000)
# m.reg_urls()


