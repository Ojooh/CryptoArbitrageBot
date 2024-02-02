import os, json
import requests

class ExchangeAPIManager:
    def __init__(self, config_file_name='exchange_data.json'):
        # Load configuration from the JSON file
        self.config_file_path = self.get_data_file_path(config_file_name)
        with open(self.config_file_path, 'r') as file:
            self.config = json.load(file)
            
    def get_data_file_path(self, data_file_name):
        # Get the absolute path of the directory containing the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get the absolute path of the 'data' directory relative to the script directory
        data_dir = os.path.join(script_dir, '..', 'data')

        # Construct the absolute path of the JSON file
        data_file_path = os.path.join(data_dir, data_file_name)

        return data_file_path
            
    def get_available_exchanges(self):
        return list(self.config.keys())
    
    def _get_exchange_config(self, exchange_identifier):
        # Helper method to retrieve the configuration for a specific exchange
        exchange_config = self.config.get(exchange_identifier)
        if not exchange_config:
            raise ValueError(f"Exchange '{exchange_identifier}' not found in the configuration.")
        return exchange_config
    
    def _get_nested_value(self, data, keys):
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data
    
    def generate_market_symbol(self, exchange_identifier, base_currency, quote_currency):
        # Get the exchange configuration
        exchange_config = self._get_exchange_config(exchange_identifier)

        # Extract symbol format information
        symbol_format = exchange_config.get('symbol_format', {})
        case = symbol_format.get('case', 'UPPER').upper()
        delimiter = symbol_format.get('delimiter', '_')

        # Format base and quote currency based on the symbol format
        if case == 'UPPER':
            base_currency = base_currency.upper()
            quote_currency = quote_currency.upper()
        elif case == 'LOWER':
            base_currency = base_currency.lower()
            quote_currency = quote_currency.lower()

        # Generate the market symbol using the specified delimiter
        market_symbol = f"{base_currency}{delimiter}{quote_currency}"

        return market_symbol

    async def fetch_current_price(self, exchange_identifier, base_currency, quote_currency):
        market = self.generate_market_symbol(exchange_identifier, base_currency, quote_currency)
        # Get the API details for the specified exchange
        exchange_config = self._get_exchange_config(exchange_identifier)

        # Make API request to get the current price for the specified market
        api_url = exchange_config['fetch_market_price_url'].replace("%", market)
        response = requests.get(f"{api_url}")
        data = response.json()

        # Extract relevant information from the API response
        nested_keys = exchange_config['price_api_key'].split('.')
        current_price = self._get_nested_value(data, nested_keys)
        buy_order_fee = exchange_config['buy_order_fee_percentage']
        sell_order_fee = exchange_config['sell_order_fee_percentage']

        # Return the result as a dictionary
        return {
            'current_price': current_price,
            'buy_order_fee': buy_order_fee,
            'sell_order_fee': sell_order_fee,
            'exchange_name': exchange_config["exchange_name"]
        }


   

# Example usage:
# manager = ExchangeAPIManager()
# result = manager.fetch_current_price('binance', 'BTC/USDT')
# print(result)
