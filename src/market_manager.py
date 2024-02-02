import json, os

class MarketManager:
    def __init__(self, file_name='markets.json'):
        self.file_name = file_name
        self.file_path  = self.get_data_file_path(file_name)
        self.markets = self._load_markets()
        
    def get_data_file_path(self, data_file_name):
        # Get the absolute path of the directory containing the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get the absolute path of the 'data' directory relative to the script directory
        data_dir = os.path.join(script_dir, '..', 'data')

        # Construct the absolute path of the JSON file
        data_file_path = os.path.join(data_dir, data_file_name)

        return data_file_path

    def _load_markets(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_markets(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.markets, file, indent=2)

    def add_market(self, base_currency, quote_currency, base_network='btc', quote_network='bep20'):
        market_name = f"{base_currency.upper()}_{quote_currency.upper()}"
        new_market = {
            'name': market_name,
            'base_currency': base_currency.upper(),
            'quote_currency': quote_currency.upper(),
            'base_network': base_network,
            'quote_network': quote_network
        }

        self.markets.append(new_market)
        self._save_markets()

    def update_market(self, market_name, new_base_currency=None, new_quote_currency=None,
                      new_base_network=None, new_quote_network=None):
        for market in self.markets:
            if market['name'] == market_name:
                if new_base_currency:
                    market['base_currency'] = new_base_currency.upper()
                if new_quote_currency:
                    market['quote_currency'] = new_quote_currency.upper()
                if new_base_network:
                    market['base_network'] = new_base_network
                if new_quote_network:
                    market['quote_network'] = new_quote_network

                self._save_markets()
                return True  # Market updated successfully

        return False  # Market not found

    def delete_market(self, market_id_name):
        market = self.get_market(market_id_name)
        print(market)
        
        if market is not None:
            self.markets.remove(market)
            self._save_markets()
            return True
        
        return False

    def list_all_markets(self):
        return [market['name'] for market in self.markets]

    def get_market_symbol(self, input_param):
        for market in self.markets:
            if input_param.upper() == market['name'] or str(input_param) == str(self.markets.index(market) + 1):
                return market

        return None  # Market not found
    
    def get_market(self, input_param):
        try:
            if isinstance(int(input_param), int):
                return self.markets[input_param - 1]
            elif isinstance(input_param, str):
                return self.get_market_symbol(input_param)
            else:
                return None
        except:
            return self.get_market_symbol(input_param)


# # Creating an instance of MarketManager
# market_manager = MarketManager()
# print(market_manager.get_market("1"))

# # Adding a market
# market_manager.add_market('BTC', 'USDT')
# market_manager.add_market('ETH', 'USDT', 'erc20')
# market_manager.add_market('TRX', 'USDT', 'TRC20',)
# market_manager.add_market('FAKE', 'USDT', 'TRC20',)


# # Listing all markets
# all_markets = market_manager.list_all_markets()
# for i, market_symbol in enumerate(all_markets, start=1):
#     print(f"{i}. {market_symbol}")

