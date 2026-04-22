import re
from cf import Cloudflare
from logger import logger

cf = Cloudflare()
rules = cf.get_cf_waf_rules()
my_ip = cf.get_my_ip()

def main() -> None:
    for x in rules['result']['rules']:
        try:
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', x['expression'])
            new_ip = x['expression'].replace(ip[0], my_ip)

            cf.update_ip_cf_waf_rule(
                            rule_id=x['id'],
                            description=x['description'],
                            expression=new_ip)
            logger.info(f"IP Address for Rule: {x['description']} updated from {ip[0]} to {my_ip}")
        except IndexError as e:
            logger.error(f"Rule does not contain IP: {x['description']}, {e}")
            pass
        except Exception as e:
            logger.error(f"Error updating IP Address for Rule: {x['description']}, {e}")

if __name__ == "__main__":
    main()
