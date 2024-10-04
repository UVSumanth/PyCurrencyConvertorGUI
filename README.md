# PyCurrencyConvertorGUI
Python Currency Convertor App

**IMPORTANT - To run the provided program successfully, need to follow below**

1. pip install requests [requests: Used for making HTTP requests]
2. pip install pandas   [pandas: Used for handling data and exporting to Excel.]
3. pip install openpyxl [openpyxl: Python library for reading and writing Excel files (xlsx)]
api_url = https://api.exchangerate-api.com/v4/latest/USD
---------------------------------------------------------------------------------------------------------------------------------
Currency Converter Application - 

This Python application allows users to perform currency conversions using real-time exchange rates. The application
features a graphical user interface (GUI) built using the Tkinter library.

Usage:
    Run the script, and a graphical window will appear with a notebook interface containing various tabs:
    - Dashboard: Welcome message and navigation buttons.
    - Convert Currency: Allows users to input an amount, source currency, and target currency for conversion.
    - View Conversion History: Displays a history of recent currency conversions.
    - 1 USD to Target Currency: Shows the exchange rate for 1 USD to various target currencies.
    - View Currency Name for Currency Code: Retrieves and displays the full name of a currency based on its code.

Functionality:
    - Automatic exchange rate update when the internet is available.
    - Ability to perform currency conversion and view conversion history.
    - Display of exchange rates for 1 USD to various currencies.
    - Retrieval of currency names based on currency codes.

File Usage:
    - exchange_rates.json: Cache file storing the latest exchange rates fetched from the API.
    - conversion_history.json: Log file storing recent conversion history.
    - exchange_rates_export.xlsx: Excel file for exporting exchange rates.

Methods:

1.	def is_internet_available():
    - is_internet_available is a function designed to check if the internet connection is available.

2.	initialize_with_internet(self)
    - Initializes the application when the internet is available, Creates tabs, fetches exchange rates, and sets up the UI components.

3.	initialize_without_internet(self)
    - Initializes the application when there is no internet connection, Creates tabs, sets up UI components, and uses cached exchange rates.

4.	go_to_dashboard(self)
    - Navigates to the Dashboard tab within the application.

5.	create_dashboard_tab(self)
    - Creates widgets for the Dashboard tab, Includes buttons for navigation to other tabs.

6.	create_convert_currency_tab(self)
    - Creates widgets for the "Convert Currency" tab, Includes entry fields for amount, source currency, and target currency.

7.	clear_entries(self)
    - Clears the entry fields in the "Convert Currency" tab.

8.	create_view_conversion_history_tab(self)
    - Creates widgets for the "View Conversion History" tab, Displays a text widget showing the conversion history.

9.	create_display_exchange_rates_tab(self)
    - Creates widgets for the "1 USD to Target Currency" tab, Displays exchange rates in a Treeview widget.

10.	create_view_currency_name_tab(self)
    - Creates widgets for the "View Currency Name for Currency Code" tab, Allows users to enter a currency code and retrieves the corresponding currency name.

11.	fetch_exchange_rates(self)
    - Fetches exchange rates from an API or uses cached rates. Saves the rates to a JSON file.

12.	load_exchange_rates_from_file(self)
    - Loads exchange rates from a JSON file.

13.	convert_currency(self)
    - Converts currency based on user input. Fetches or uses cached exchange rates.

14.	is_valid_currency(self, currency_code)
    - Checks if a currency code is valid.

15.	log_conversion_history(self, from_currency, to_currency, amount, converted_amount)
    - Logs conversion history entries to a JSON file.

16.	update_conversion_history_tab(self)
    - Updates the "View Conversion History" tab with the latest conversion history.

17.	update_exchange_rates(self)
    - Updates exchange rates from the API.

18.	export_to_excel(self)
    - Exports exchange rates to an Excel file.

19.	get_currency_name(self)
    - Retrieves the currency name based on user input.

20.	get_currency_name_by_code(self, currency_code)
    - Retrieves the currency name for a given currency code.

21.	display_exchange_rates_table(self)
    - Clears and updates the exchange rates displayed in the Treeview widget.

22.	get_exchange_rate(self, currency_code)
    - Retrieves the exchange rate for a given currency code.

23.	main()
    - Entry point of the program. Creates the Tkinter root window and the CurrencyConverterApp instance.
---------------------------------------------------------------------------------------------------------------------------------
Notes:
-> The program relies on external APIs for currency data, so internet connectivity is necessary for the most up-to-date information.
-> If no internet connection is available, the app will use cached exchange rates from the 'exchange_rates.json' file
-> It uses a local JSON file ('exchange_rates.json') to store exchange rates data to avoid frequent API calls when there is no internet connection.
-> The script uses the pandas library for exporting the exchange rates table to an Excel file.

References:
1. API Used : https://api.exchangerate-api.com/v4/latest/USD
2. https://data-flair.training/blogs/currency-converter-python/
3. https://www.geeksforgeeks.org/currency-converter-in-python/
4. https://www.freecodecamp.org/news/how-to-build-a-currency-converter-gui-with-tkinter/
5. Chatgpt.
