import asyncio
from arbitrage_opportunity_finder import ArbitrageOpportunityFinder
from exchange_api_manager import ExchangeAPIManager
from market_manager import MarketManager
from logger import Logger 

class CryptoArbitrageBot:
    def __init__(self):
        self.exchange_manager       = ExchangeAPIManager()
        self.market_manager         = MarketManager()
        self.available_exchanges    = []
        self.available_markets      = []
        self.logger                 = Logger()
        self.market                 = None

    def welcome_message(self):
        self.logger.log("Welcome to Crypto Arbitrage Bot!", status='info')
        self.logger.log("A bot to find arbitrage opportunities across multiple cryptocurrency exchanges.", status='info')
        self.logger.log("Available Exchanges:", status='info')

    def display_available_exchanges(self):
        print("\n \n")
        self.available_exchanges = self.exchange_manager.get_available_exchanges()
        for i, exchange in enumerate(self.available_exchanges, start=1):
            self.logger.log(f"{i}. {exchange}", status='info')
            
    def display_available_markets(self):
        self.available_markets = self.market_manager.list_all_markets()
        for i, market_symbol in enumerate(self.available_markets, start=1):
            self.logger.log(f"{i}. {market_symbol}")

    async def run(self):
        # Step 1: Welcome message and select market
        self.welcome_message()
        
        self.display_available_markets()
        
        while True:
            use_random = input("\n \n Enter the ID or the name of the market to trade in: ")
            self.market = self.market_manager.get_market(use_random)
            if self.market is not None:
                break
            else:
                self.logger.log("Invalid input. Please enter the ID or the name of the market to trade in from the list above", status='error')

        self.logger.log(f"Trading in {self.market['name']} Market.......", status='info')
        # Step 2: Display the number of exchanges and show them in a list
        self.display_available_exchanges()

        # Step 3: Provide an option to randomly select n number of exchanges
        while True:
            use_random = input("\n \n Do you want to randomly select exchanges? (yes/no): ").lower()
            if use_random in ['yes', 'no']:
                break
            else:
                self.logger.log("Invalid input. Please enter 'yes' or 'no'.", status='error')

        if use_random == 'yes':
            while True:
                try:
                    num_exchanges = int(input("Enter the number of exchanges to randomly select: "))
                    if 1 < num_exchanges <= len(self.available_exchanges):
                        break
                    else:
                        self.logger.log(f"Invalid input. Please enter a number between 1 and {len(self.available_exchanges)}.", status='error')
                except ValueError:
                    self.logger.log("Invalid input. Please enter a valid number.", status='error')
        else:
            while True:
                try:
                    selected_numbers = input("Enter the numbers of the exchanges (separated by commas): ")
                    selected_numbers = [int(num.strip()) for num in selected_numbers.split(',')]
                    if all(1 <= num <= len(self.available_exchanges) for num in selected_numbers):
                        break
                    else:
                        self.logger.log(f"Invalid input. Please enter valid numbers between 1 and {len(self.available_exchanges)}.", status='error')
                except ValueError:
                    self.logger.log("Invalid input. Please enter valid numbers.", status='error')

            num_exchanges = len(selected_numbers)

        # Step 5: Get exchange names based on user input
        selected_exchanges = (
            self.available_exchanges if use_random
            else [self.available_exchanges[num - 1] for num in selected_numbers]
        )

        # Step 6: Pass user input to ArbitrageOpportunityFinder class
        opportunity_finder = ArbitrageOpportunityFinder(
            num_exchanges=num_exchanges,
            exchange_names_or_ids=selected_exchanges,
            use_random=use_random,
            base_currency=self.market["base_currency"],
            quote_currency=self.market["quote_currency"],
        )

        # Search for arbitrage oppurtunity
        print("\n \n")
        await opportunity_finder.find_arbitrage_opportunity(5, self.logger)
    
    def start_bot(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run()) 

# Example usage:
bot = CryptoArbitrageBot()
bot.start_bot()
