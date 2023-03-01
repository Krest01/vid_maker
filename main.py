import oauth2
import requests
import json
auth_key = requests.get('https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=dold7hl7sxyqktqr5e17iq605p83ec')
response = requests.get('https://www.twitch.tv/xntentacion/clips?filter=clips&range=24hr', auth=auth_key)


