import requests

def get_public_key(address):
    url = f"https://blockchain.info/q/pubkeyaddr/{address}"
    try:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            public_key = response.text
            return public_key
        else:
            return f"Error: Unable to retrieve data (status code: {response.status_code})"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main program loop
if __name__ == "__main__":
    bitcoin_address = input("Enter the Bitcoin address: ")
    public_key = get_public_key(bitcoin_address)
    print(f"Public Key: {public_key}")
