import requests
def remove_double_newlines(text):
    return text.replace('\\n\\n', '\n')

# Test the function
response = requests.get(f"http://192.168.100.78:5000/generate_content/{'give me 10 colors'}").text
response = response[1:-2] 
print(remove_double_newlines(response))