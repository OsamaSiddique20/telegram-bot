import requests
import socket

def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip", timeout=5)
        response.raise_for_status()
        public_ip = response.json()["origin"]

        # Get local IP using a dummy socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        print("Public IP Address:", public_ip)
        print("Local IP Address:", local_ip)
        return public_ip, local_ip

    except requests.exceptions.RequestException as e:
        print(f"Unable to retrieve public IP address. Error: {e}")
        return None, None
    except Exception as e:
        print(f"Unable to retrieve local IP address. Error: {e}")
        return None, None

if __name__ == '__main__':
    public_ip, local_ip = get_public_ip()

    if public_ip:
        print("Public IP:", public_ip)
        print("Local IP:", local_ip)
    else:
        print("Could not retrieve IP addresses.")
