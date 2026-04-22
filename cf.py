import requests
import json
from settings import Settings

settings = Settings(_env_file=".env")

class Cloudflare:
    def __init__(self):
        self.cf_api_url = settings.cf_api_url
        self.token = settings.token.get_secret_value()
        self.zone_id = settings.zone_id
        self.ruleset = settings.ruleset

    def get_cf_waf_rules(self):
        api_url = f"{self.cf_api_url}/zones/{self.zone_id}/rulesets/{self.ruleset}"
        request_headers={"Authorization": f"Bearer {self.token}" ,"Content-Type":"application/json"}

        return requests.get(api_url, headers=request_headers).json()


    def update_ip_cf_waf_rule(self, rule_id, description, expression):
        api_url = f"{self.cf_api_url}/zones/{self.zone_id}/rulesets/{self.ruleset}/rules/{rule_id}"
        request_headers={"Authorization": f"Bearer {self.token}" ,"Content-Type":"application/json"}
        data = {"action": "block", "description": f"{description}",
                "expression": f"{expression}"}

        return requests.patch(api_url, headers=request_headers, data=json.dumps(data)).json()

    @staticmethod
    def get_my_ip() -> str:
        my_ip = requests.get("http://ifconfig.me").text
        return my_ip
