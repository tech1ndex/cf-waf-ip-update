import re
from typing import Any

from cf import Cloudflare
from logger import logger

cf = Cloudflare()

def update_ip(rule: Any) -> None:
        my_ip = cf.get_my_ip()
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', rule['expression'])
        if not ip:
            logger.error(f"Rule does not contain IP: {rule['description']}")
            return

        new_ip = rule['expression'].replace(ip[0], my_ip)
        print(ip)
        print(new_ip)
        if new_ip == my_ip:
            logger.info(f"Rule {rule['description']} matched IP: {ip[0]}, skipping")

        cf.update_ip_cf_waf_rule(
                        rule_id=rule['id'],
                        description=rule['description'],
                        expression=new_ip)
        logger.info(f"IP Address for Rule: {rule['description']} updated from {ip[0]} to {my_ip}")

def main() -> None:
    rules = cf.get_cf_waf_rules()
    for rule in rules['result']['rules']:
        update_ip(rule)

if __name__ == "__main__":
    main()
