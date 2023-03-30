import json

flavour = ['chocolate', 'strawberry', 'caramel']
quantity = ['half', 'one']
name =[]
contact = []


def validate_order(slots):
    # Validate Name
    if not slots['Name']:
        print('Validating Name Slot')

        return {
            'isValid': False,
            'invalidSlot': 'Name'
        }

    if slots['Name']['value']['originalValue'] is None:
        print('Invalid Name')

        return {
            'isValid': False,
            'invalidSlot': 'Name',
            'message': 'Please provide a name.'.format(", ".join(name))
        }
    # Validate Flavour
    if not slots['Flavour']:
        print('Validating Flavour Slot')

        return {
            'isValid': False,
            'invalidSlot': 'Flavour'
        }

    if slots['Flavour']['value']['originalValue'].lower() not in flavour:
        print('Invalid Flavour')

        return {
            'isValid': False,
            'invalidSlot': 'Flavour',
            'message': 'Please select different flavour from the list.'.format(", ".join(flavour))
        }

    # Validate BurgerFranchise
    if not slots['Quantity']:
        print('Validating Quantity Slot')

        return {
            'isValid': False,
            'invalidSlot': 'Quantity'
        }

    if slots['Quantity']['value']['originalValue'].lower() not in quantity:
        print('Invalid Quantity')

        return {
            'isValid': False,
            'invalidSlot': 'Quantity',
            'message': 'We do have only the listed quantity.Please select from the list.'.format(", ".join(quantity))
        }
        
    # Validate Contact
    if not slots['Contact']:
        print('Validating Contact Slot')

        return {
            'isValid': False,
            'invalidSlot': 'Contact'
        }

    if slots['Contact']['value']['originalValue'] is None:
        print('Invalid Contact')

        return {
            'isValid': False,
            'invalidSlot': 'Name',
            'message': 'Please provide a contact number.'.format(", ".join(contact))
        }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order.Your order ID is #34454."
                }
            ]
        }

    print(response)
    return response

