from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Zapier Webhook URL for client checking
ZAPIER_WEBHOOK_URL = "" # your webhook URL


# Endpoint to handle Dialogflow webhook and Zapier response
@app.route('/webhook1', methods=['POST'])
def webhook():
    # Get data from the request (either from Dialogflow or Zapier)
    request_data = request.json
    print(request_data)
    
    # Case 1: Check if the data has 'sessionInfo' -> Request is from Dialogflow
    if 'sessionInfo' in request_data:
        # Handle Dialogflow request with phone number
        parameters = request_data['sessionInfo']['parameters']
        
        if 'phone_number' in parameters:
            phone_number = parameters.get('phone_number')
            
            # Send phone number to Zapier to check if client exists
            zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json={'phone_number': phone_number})
            zapier_data = zapier_response.json()
            print(f"Response from Zapier: {zapier_data}")
            
            if zapier_data.get('request_id'):
                return jsonify({
                    'fulfillment_response': {
                        'messages': [{
                            'text': {
                                'text': ["Checking"]
                            }
                        }]
                    }
                })
            # else:
            #     return jsonify({
            #         'fulfillment_response': {
            #             'messages': [{
            #                 'text': {
            #                     'text': ["Client not found. Please provide more details to create a new client."]
            #                 }
            #             }]
            #         }
            #     })
    
    # Case 2: Request is from Zapier (when `first_name` and `last_name` are present)
    elif 'first_name' in request_data and 'last_name' in request_data:
        first_name = request_data.get('first_name')
        last_name = request_data.get('last_name')
        
        # Handle Zapier response
        print(f"Client Found: {first_name} {last_name}")
        

        return jsonify({"status": "success"}), 200
    
    # Default case: When neither Dialogflow nor Zapier-specific data is present
    # else:
    #     return jsonify({
    #         'fulfillment_response': {
    #             'messages': [{
    #                 'text': {
    #                     'text': ["Invalid data received. Please try again."]
    #                 }
    #             }]
    #         }
    #     })



# Handle user data for creating new client
@app.route('/create_client', methods=['POST'])
def create_client():
    # Get data from Dialogflow
    dialogflow_data = request.json
    first_name = dialogflow_data.get('sessionInfo').get('parameters').get('first-name')
    print(first_name)
    last_name = dialogflow_data.get('sessionInfo').get('parameters').get('last-name')
    print(last_name)
    email = dialogflow_data.get('sessionInfo').get('parameters').get('email')
    print(email)
    phone_number = dialogflow_data.get('sessionInfo').get('parameters').get('phone_number')
    print(phone_number)
    address = dialogflow_data.get('sessionInfo').get('parameters').get('address')
    print(address)
    business_name = dialogflow_data.get('sessionInfo').get('parameters').get('business-name')
    print(business_name)

    ZAPIER_WEBHOOK_URL = "" #your webhook URL
    # Send data to Zapier to create a new client
    zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json={
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number' : phone_number,
        'address' : address,
        'business_name' : business_name
    })

    print(zapier_response.json())

    # Response back to Dialogflow after creating the client
    return jsonify({
        'fulfillment_response': {
            'messages': [{
                'text': {
                    'text': ["Client has been created successfully. How can we assist you further?"]
                }
            }]
        }
    })



if __name__ == '__main__':
    app.run(port=5000, debug=True)
