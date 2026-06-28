# CTI Integration Architecture

## Overview
The CRM supports Asterisk and FreePBX integration using AMI and SIP trunks for click-to-call, incoming-call popups, call monitoring, recording, transfer, and conference capabilities.

## AMI Events
- NewChannel
- DialBegin
- BridgeEnter
- Hangup

## Flow
1. SIP trunk receives inbound or outbound call.
2. Asterisk/FreePBX emits AMI events.
3. Backend endpoint receives events and creates a call log.
4. Frontend softphone widget receives the event and displays an incoming popup.
5. Recording is uploaded and stored as a CRM recording.

## Sample Asterisk Integration
```python
from asterisk.ami import AMIClient

client = AMIClient(address='127.0.0.1', port=5038)
client.login(username='admin', secret='password')

client.add_event_listener('NewChannel', lambda event: print(event))
client.add_event_listener('Hangup', lambda event: print(event))
```

## Sample WhatsApp Integration
```python
import requests

requests.post(
    'https://graph.facebook.com/v18.0/whatsapp_business_account/messages',
    headers={'Authorization': 'Bearer TOKEN'},
    json={"messaging_product": "whatsapp", "to": "919999999999", "type": "text", "text": {"body": "Hello from EduCRM"}},
)
```
