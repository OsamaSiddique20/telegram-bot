import requests

def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        response.raise_for_status()
        public_ip = response.json()["origin"]
        print("Public IP Address:", public_ip)
        return public_ip
    except requests.exceptions.RequestException as e:
        print(f"Unable to retrieve public IP address. Error: {e}")
        return None

# Example usage:
public_ip = get_public_ip()

if public_ip:
    print("Public IP Address:", public_ip)
else:
    print("No public IP address found.")

