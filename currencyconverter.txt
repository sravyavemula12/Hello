import requests

API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
BASE_URL = 'https://v6.exchangerate-api.com/v6/'

def get_exchange_rate(base_currency, target_currency):
    url = f"{BASE_URL}{API_KEY}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rate']
    else:
        raise Exception('Error fetching exchange rate')

def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    return amount * exchange_rate

def main():
    print("Welcome to the Currency Converter!")
    amount = float(input("Enter the amount: "))
    base_currency = input("Enter the base currency (e.g., USD): ").upper()
    target_currency = input("Enter the target currency (e.g., EUR): ").upper()
    
    try:
        converted_amount = convert_currency(amount, base_currency, target_currency)
        print(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
