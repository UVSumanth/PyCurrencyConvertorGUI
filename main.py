import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import os

# Color Scheme
PRIMARY_COLOR = "#3498db"  # Blue
SECONDARY_COLOR = "#2ecc71"  # Green
ACCENT_COLOR = "#e74c3c"  # Red
BACKGROUND_COLOR = "#ecf0f1"  # Light Gray
TEXT_COLOR = "#2c3e50"  # Dark Gray


# Check if internet connection is available by attempting to make a request to Google.
def is_internet_available():
    try:
        response = requests.get('http://www.google.com', timeout=1)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        # Initialize notebook attribute
        self.notebook = ttk.Notebook(self.root)

        if is_internet_available():
            self.initialize_with_internet()
        else:
            self.initialize_without_internet()

    def initialize_with_internet(self):
        # Internet is available, proceed with the initialization
        internet_label = tk.Label(self.root, text="Internet Available", font=("Arial", 10, "bold"), fg=SECONDARY_COLOR,
                                  background=BACKGROUND_COLOR)
        internet_label.pack(padx=10, pady=10)
        # Add home button
        home_button = tk.Button(self.root, text="Home", command=self.go_to_dashboard, bg=PRIMARY_COLOR, fg="white")
        home_button.pack(pady=3)

        self.notebook = ttk.Notebook(self.root)
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.exchange_rates = self.fetch_exchange_rates()

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.convert_currency_tab = ttk.Frame(self.notebook)
        self.view_conversion_history_tab = ttk.Frame(self.notebook)
        self.display_exchange_rates_tab = ttk.Frame(self.notebook)
        self.view_currency_name_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.convert_currency_tab, text="Convert Currency")
        self.notebook.add(self.view_conversion_history_tab, text="View Conversion History")
        self.notebook.add(self.display_exchange_rates_tab, text="1 USD to Target Currency")
        self.notebook.add(self.view_currency_name_tab, text="View Currency Name for Currency Code")

        self.create_dashboard_tab()
        self.create_convert_currency_tab()
        self.create_view_conversion_history_tab()
        self.create_display_exchange_rates_tab()
        self.create_view_currency_name_tab()

        self.notebook.pack(padx=10, pady=10)

        # Initialize conversion history list
        self.conversion_history = []
        self.create_view_conversion_history_tab()

    def initialize_without_internet(self):
        # Internet is not available, show a message
        internet_label = tk.Label(self.root, text="No Internet", font=("Arial", 10, "bold"), fg=ACCENT_COLOR,
                                  background=BACKGROUND_COLOR)
        internet_label.pack(padx=10, pady=10)
        # Add home button
        home_button = tk.Button(self.root, text="Home", command=self.go_to_dashboard, bg=PRIMARY_COLOR, fg="white")
        home_button.pack(pady=3)
        # Create Convert Currency, View Conversion History, and View Currency Name for Currency Code tabs
        self.convert_currency_tab = ttk.Frame(self.notebook)
        self.view_conversion_history_tab = ttk.Frame(self.notebook)
        self.view_currency_name_tab = ttk.Frame(self.notebook)

        # Create history_text attribute even when there is no internet
        self.history_text = tk.Text(self.view_conversion_history_tab, height=20, width=80)
        self.history_text.grid(row=1, column=0, padx=5, pady=5)

        # Add tabs to the notebook
        self.notebook.add(self.convert_currency_tab, text="Convert Currency")
        self.notebook.add(self.view_conversion_history_tab, text="View Conversion History")
        self.notebook.add(self.view_currency_name_tab, text="View Currency Name for Currency Code")

        # Pack the notebook to the main window
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        # Create Convert Currency and View Currency Name for Currency Code widgets
        self.create_convert_currency_tab()
        self.create_view_currency_name_tab()

    def go_to_dashboard(self):
        # Navigate to the Dashboard tab
        self.notebook.select(0)

    def create_dashboard_tab(self):
        # Add widgets for the dashboard
        label = tk.Label(self.dashboard_tab, text="Welcome to the Currency Converter Dashboard!", font=("Arial", 16),
                         fg=TEXT_COLOR, background=BACKGROUND_COLOR)
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # Set a common size for buttons
        button_width = 20
        button_height = 5

        # Add buttons for navigation
        convert_currency_button = tk.Button(self.dashboard_tab, text="Currency Converter", font=("Sagona", 10, "bold"),
                                            command=lambda: self.notebook.select(1), width=button_width,
                                            height=button_height, bg=PRIMARY_COLOR, fg="white")
        convert_currency_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        view_conversion_history_button = tk.Button(self.dashboard_tab, text="History", font=("Sagona", 10, "bold"),
                                                   command=lambda: self.notebook.select(2), width=button_width,
                                                   height=button_height, bg=PRIMARY_COLOR, fg="white")
        view_conversion_history_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        usd_to_target_currency_button = tk.Button(self.dashboard_tab,
                                                  text="Exchange Rates Table \n(1 USD to Target Currency)",
                                                  font=("Sagona", 10, "bold"),
                                                  command=lambda: self.notebook.select(3), width=button_width,
                                                  height=button_height, bg=PRIMARY_COLOR, fg="white")
        usd_to_target_currency_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        view_currency_name_button = tk.Button(self.dashboard_tab, text="Currency Code TO Currency Name",
                                              font=("Sagona", 10, "bold"),
                                              command=lambda: self.notebook.select(4), width=button_width,
                                              height=button_height, bg=PRIMARY_COLOR, fg="white")
        view_currency_name_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        # Set row and column weights to make widgets resizable
        for i in range(3):
            self.dashboard_tab.grid_rowconfigure(i, weight=1)
            self.dashboard_tab.grid_columnconfigure(i, weight=1)

    def create_convert_currency_tab(self):
        amount_label = tk.Label(self.convert_currency_tab, text="Amount:")
        amount_label.grid(row=0, column=0, padx=5, pady=5)

        self.amount_entry = tk.Entry(self.convert_currency_tab)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        source_currency_label = tk.Label(self.convert_currency_tab, text="Source Currency:")
        source_currency_label.grid(row=1, column=0, padx=5, pady=5)

        self.source_currency_entry = tk.Entry(self.convert_currency_tab)
        self.source_currency_entry.grid(row=1, column=1, padx=5, pady=5)

        target_currency_label = tk.Label(self.convert_currency_tab, text="Target Currency:")
        target_currency_label.grid(row=2, column=0, padx=5, pady=5)

        self.target_currency_entry = tk.Entry(self.convert_currency_tab)
        self.target_currency_entry.grid(row=2, column=1, padx=5, pady=5)

        convert_button = tk.Button(self.convert_currency_tab, text="Convert", command=self.convert_currency,
                                   bg="#4caf50", fg="white")
        convert_button.grid(row=3, column=0, pady=10)

        clear_button = tk.Button(self.convert_currency_tab, text="Clear", command=self.clear_entries, bg="#e74c3c",
                                 fg="white")  # Vibrant accent color for the button
        clear_button.grid(row=3, column=1, pady=10)

        self.converted_result_label = tk.Label(self.convert_currency_tab, text="")
        self.converted_result_label.grid(row=4, column=0, columnspan=2, pady=5)

    def clear_entries(self):
        # Clear the entry fields
        self.amount_entry.delete(0, tk.END)
        self.source_currency_entry.delete(0, tk.END)
        self.target_currency_entry.delete(0, tk.END)
        self.converted_result_label.config(text="")

    def create_view_conversion_history_tab(self):
        history_label = tk.Label(self.view_conversion_history_tab, text="Conversion History:")
        history_label.grid(row=0, column=0, padx=5, pady=5)

        # Increase the width and height of the Text widget
        self.history_text = tk.Text(self.view_conversion_history_tab, height=20, width=80, bg="white")
        self.history_text.grid(row=1, column=0, padx=5, pady=5)
        self.update_conversion_history_tab()  # Call this function after creating the history_text widget

    def create_display_exchange_rates_tab(self):
        update_button = tk.Button(self.display_exchange_rates_tab, text="Update Exchange Rates",
                                  command=self.update_exchange_rates, bg="#4caf50", fg="white")
        update_button.grid(row=0, column=0, padx=5, pady=5)

        export_button = tk.Button(self.display_exchange_rates_tab, text="Export to Excel", command=self.export_to_excel,
                                  bg="#4caf50", fg="white")
        export_button.grid(row=0, column=1, padx=5, pady=5)

        self.exchange_rates_treeview = ttk.Treeview(self.display_exchange_rates_tab,
                                                    columns=("Currency", "Exchange Rate"), show="headings")
        self.exchange_rates_treeview.heading("Currency", text="Target Currency")
        self.exchange_rates_treeview.heading("Exchange Rate", text="1USD to Target Currency")
        self.exchange_rates_treeview.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.display_exchange_rates_table()  # Call the method to display exchange rates

    def create_view_currency_name_tab(self):
        currency_code_label = tk.Label(self.view_currency_name_tab, text="Currency Code:")
        currency_code_label.grid(row=0, column=0, padx=5, pady=5)

        self.currency_code_entry = tk.Entry(self.view_currency_name_tab)
        self.currency_code_entry.grid(row=0, column=1, padx=5, pady=5)

        get_name_button = tk.Button(self.view_currency_name_tab, text="Get Currency Name",
                                    command=self.get_currency_name, bg="#4caf50", fg="white")
        get_name_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.currency_name_label = tk.Label(self.view_currency_name_tab, text="")
        self.currency_name_label.grid(row=2, column=0, columnspan=2, pady=5)

    def fetch_exchange_rates(self):
        # Check if internet connection is available
        if is_internet_available():
            try:
                response = requests.get(self.api_url)
                if response.status_code == 200:
                    data = response.json()
                    # Save the fetched exchange rates to a JSON file
                    with open('exchange_rates.json', 'w') as json_file:
                        json.dump(data['rates'], json_file)
                    return data['rates']
                else:
                    messagebox.showerror("Error", "Failed to fetch exchange rates. Please try again later.")
                    return {}
            except requests.RequestException as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                return {}
        else:
            # Use cached exchange rates from the JSON file
            return self.load_exchange_rates_from_file()

    def load_exchange_rates_from_file(self):
        try:
            with open('exchange_rates.json', 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            messagebox.showerror("Error", "No internet connection and no cached exchange rates found.")
            return {}

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            if amount < 0:
                raise ValueError("Invalid input for amount. Please enter a valid number.")

            source_currency = self.source_currency_entry.get().upper()
            target_currency = self.target_currency_entry.get().upper()

            # Check if entered currency codes are valid
            if not self.is_valid_currency(source_currency) or not self.is_valid_currency(target_currency):
                messagebox.showerror("Error",
                                     "Invalid currency code. Please recheck Source and Target currency and enter a valid currency code.")
                return

            # Check if internet connection is available
            if is_internet_available():
                # Fetch exchange rates from the API
                self.exchange_rates = self.fetch_exchange_rates()
            else:
                # Use cached exchange rates from the JSON file
                self.exchange_rates = self.load_exchange_rates_from_file()

            rate = self.exchange_rates.get(target_currency)

            if rate is not None:
                converted_amount = amount * rate
                result_text = f"{amount:.2f} {source_currency} is equal to {converted_amount:.2f} {target_currency}"
                self.converted_result_label.config(text=result_text)

                # Update conversion history
                self.log_conversion_history(source_currency, target_currency, amount, converted_amount)
                self.update_conversion_history_tab()

            else:
                messagebox.showerror("Error",
                                     "Invalid target currency code. Please choose from the supported currencies.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def is_valid_currency(self, currency_code):
        # Check if the currency code is valid (you can customize this validation based on your requirements)
        # For example, you can maintain a list of valid currency codes or fetch them from an API
        valid_currency_codes = ['USD', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM',
                                'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP',
                                'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK',
                                'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'FOK', 'GBP',
                                'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
                                'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY',
                                'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR',
                                'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR',
                                'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR',
                                'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF',
                                'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP',
                                'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD', 'TWD',
                                'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR',
                                'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL'
                                ]  # Update with your valid codes
        return currency_code in valid_currency_codes

    def log_conversion_history(self, from_currency, to_currency, amount, converted_amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "from_currency": from_currency, "to_currency": to_currency,
                     "amount": amount, "converted_amount": converted_amount}

        filename = 'conversion_history.json'

        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                json.dump([], file)

        with open(filename, 'r+') as file:
            try:
                history = json.load(file)
            except json.decoder.JSONDecodeError:
                history = []

            if len(history) >= 100:
                history.pop(0)

            history.append(log_entry)

            cutoff_date = datetime.now() - timedelta(days=15)
            history = [entry for entry in history if
                       datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S") > cutoff_date]

            file.seek(0)
            json.dump(history, file, indent=2)
            file.truncate()

    def update_conversion_history_tab(self):
        filename = 'conversion_history.json'

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    history = json.load(file)
                except json.decoder.JSONDecodeError:
                    history = []

                # Clear existing content in the Text widget
                self.history_text.delete(1.0, tk.END)

                for entry in reversed(history):  # Reverse the order to display the latest entry first
                    timestamp = entry["timestamp"]
                    from_currency = entry["from_currency"]
                    to_currency = entry["to_currency"]
                    amount = entry["amount"]
                    converted_amount = entry["converted_amount"]
                    history_entry = f"{timestamp}: {amount:.2f} {from_currency} => {converted_amount:.2f} {to_currency}\n"
                    # Insert the new history entry at the end of the Text widget
                    self.history_text.insert(tk.END, history_entry)

                # Scroll to the bottom of the Text widget
                self.history_text.see(tk.END)

    def update_exchange_rates(self):
        # Check if internet connection is available
        if is_internet_available():
            try:
                response = requests.get(self.api_url)
                if response.status_code == 200:
                    data = response.json()
                    # Save the fetched exchange rates to a JSON file
                    with open('exchange_rates.json', 'w') as json_file:
                        json.dump(data['rates'], json_file)
                    # Update the exchange rates attribute
                    self.exchange_rates = data['rates']
                    # Display the updated exchange rates in the Treeview
                    self.display_exchange_rates_table()
                    messagebox.showinfo("Success", "Exchange rates updated successfully.")
                else:
                    messagebox.showerror("Error", "Failed to fetch exchange rates. Please try again later.")
            except requests.RequestException as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "No internet connection. Unable to update exchange rates.")

    def export_to_excel(self):
        # Retrieve the exchange rates
        exchange_rates = self.exchange_rates

        # Check if there are exchange rates to export
        if not exchange_rates:
            messagebox.showwarning("No Data", "No exchange rates to export.")
            return

        # Create a DataFrame from the exchange rates
        df = pd.DataFrame(list(exchange_rates.items()), columns=['Currency Code', 'Exchange Rate'])

        # Specify the file name for the Excel file
        excel_filename = 'exchange_rates_export.xlsx'

        try:
            # Export the DataFrame to Excel
            df.to_excel(excel_filename, index=False)

            # Display a success message
            messagebox.showinfo("Export Successful", f"Exchange rates exported to {excel_filename}")
        except Exception as e:
            # Display an error message if the export fails
            messagebox.showerror("Error", f"An error occurred during export: {str(e)}")

    def get_currency_name(self):
        currency_code = self.currency_code_entry.get().upper()
        currency_name = self.get_currency_name_by_code(currency_code)
        result_text = f"The currency name for {currency_code} is: {currency_name}"
        self.currency_name_label.config(text=result_text)

    def get_currency_name_by_code(self, currency_code):
        currency_names = {
            "USD": "United States Dollar",
            "AED": "United Arab Emirates Dirham",
            "AFN": "Afghan Afghani",
            "ALL": "Albanian Lek",
            "AMD": "Armenian Dram",
            "ANG": "Netherlands Antillean Guilder",
            "AOA": "Angolan Kwanza",
            "ARS": "Argentine Peso",
            "AUD": "Australian Dollar",
            "AWG": "Aruban Florin",
            "AZN": "Azerbaijani Manat",
            "BAM": "Bosnia-Herzegovina Convertible Mark",
            "BBD": "Barbadian Dollar",
            "BDT": "Bangladeshi Taka",
            "BGN": "Bulgarian Lev",
            "BHD": "Bahraini Dinar",
            "BIF": "Burundian Franc",
            "BMD": "Bermudian Dollar",
            "BND": "Brunei Dollar",
            "BOB": "Bolivian Boliviano",
            "BRL": "Brazilian Real",
            "BSD": "Bahamian Dollar",
            "BTN": "Bhutanese Ngultrum",
            "BWP": "Botswanan Pula",
            "BYN": "Belarusian Ruble",
            "BZD": "Belize Dollar",
            "CAD": "Canadian Dollar",
            "CDF": "Congolese Franc",
            "CHF": "Swiss Franc",
            "CLP": "Chilean Peso",
            "CNY": "Chinese Yuan",
            "COP": "Colombian Peso",
            "CRC": "Costa Rican Colón",
            "CUP": "Cuban Peso",
            "CVE": "Cape Verdean Escudo",
            "CZK": "Czech Republic Koruna",
            "DJF": "Djiboutian Franc",
            "DKK": "Danish Krone",
            "DOP": "Dominican Peso",
            "DZD": "Algerian Dinar",
            "EGP": "Egyptian Pound",
            "ERN": "Eritrean Nakfa",
            "ETB": "Ethiopian Birr",
            "EUR": "Euro",
            "FJD": "Fijian Dollar",
            "FKP": "Falkland Islands Pound",
            "FOK": "Faroese Króna",
            "GBP": "British Pound Sterling",
            "GEL": "Georgian Lari",
            "GGP": "Guernsey Pound",
            "GHS": "Ghanaian Cedi",
            "GIP": "Gibraltar Pound",
            "GMD": "Gambian Dalasi",
            "GNF": "Guinean Franc",
            "GTQ": "Guatemalan Quetzal",
            "GYD": "Guyanaese Dollar",
            "HKD": "Hong Kong Dollar",
            "HNL": "Honduran Lempira",
            "HRK": "Croatian Kuna",
            "HTG": "Haitian Gourde",
            "HUF": "Hungarian Forint",
            "IDR": "Indonesian Rupiah",
            "ILS": "Israeli New Shekel",
            "IMP": "Isle of Man Pound",
            "INR": "Indian Rupee",
            "IQD": "Iraqi Dinar",
            "IRR": "Iranian Rial",
            "ISK": "Icelandic Króna",
            "JEP": "Jersey Pound",
            "JMD": "Jamaican Dollar",
            "JOD": "Jordanian Dinar",
            "JPY": "Japanese Yen",
            "KES": "Kenyan Shilling",
            "KGS": "Kyrgystani Som",
            "KHR": "Cambodian Riel",
            "KID": "Kiribati Dollar",
            "KMF": "Comorian Franc",
            "KRW": "South Korean Won",
            "KWD": "Kuwaiti Dinar",
            "KYD": "Cayman Islands Dollar",
            "KZT": "Kazakhstani Tenge",
            "LAK": "Laotian Kip",
            "LBP": "Lebanese Pound",
            "LKR": "Sri Lankan Rupee",
            "LRD": "Liberian Dollar",
            "LSL": "Lesotho Loti",
            "LYD": "Libyan Dinar",
            "MAD": "Moroccan Dirham",
            "MDL": "Moldovan Leu",
            "MGA": "Malagasy Ariary",
            "MKD": "Macedonian Denar",
            "MMK": "Myanma Kyat",
            "MNT": "Mongolian Tugrik",
            "MOP": "Macanese Pataca",
            "MRU": "Mauritanian Ouguiya",
            "MUR": "Mauritian Rupee",
            "MVR": "Maldivian Rufiyaa",
            "MWK": "Malawian Kwacha",
            "MXN": "Mexican Peso",
            "MYR": "Malaysian Ringgit",
            "MZN": "Mozambican Metical",
            "NAD": "Namibian Dollar",
            "NGN": "Nigerian Naira",
            "NIO": "Nicaraguan Córdoba",
            "NOK": "Norwegian Krone",
            "NPR": "Nepalese Rupee",
            "NZD": "New Zealand Dollar",
            "OMR": "Omani Rial",
            "PAB": "Panamanian Balboa",
            "PEN": "Peruvian Nuevo Sol",
            "PGK": "Papua New Guinean Kina",
            "PHP": "Philippine Peso",
            "PKR": "Pakistani Rupee",
            "PLN": "Polish Złoty",
            "PYG": "Paraguayan Guarani",
            "QAR": "Qatari Rial",
            "RON": "Romanian Leu",
            "RSD": "Serbian Dinar",
            "RUB": "Russian Ruble",
            "RWF": "Rwandan Franc",
            "SAR": "Saudi Riyal",
            "SBD": "Solomon Islands Dollar",
            "SCR": "Seychellois Rupee",
            "SDG": "Sudanese Pound",
            "SEK": "Swedish Krona",
            "SGD": "Singapore Dollar",
            "SHP": "Saint Helena Pound",
            "SLE": "Sierra Leonean Leone",
            "SLL": "Sierra Leonean Leone (old)",
            "SOS": "Somali Shilling",
            "SRD": "Surinamese Dollar",
            "SSP": "South Sudanese Pound",
            "STN": "São Tomé and Príncipe Dobra",
            "SYP": "Syrian Pound",
            "SZL": "Swazi Lilangeni",
            "THB": "Thai Baht",
            "TJS": "Tajikistani Somoni",
            "TMT": "Turkmenistani Manat",
            "TND": "Tunisian Dinar",
            "TOP": "Tongan Pa'anga",
            "TRY": "Turkish Lira",
            "TTD": "Trinidad and Tobago Dollar",
            "TVD": "Tuvaluan Dollar",
            "TWD": "New Taiwan Dollar",
            "TZS": "Tanzanian Shilling",
            "UAH": "Ukrainian Hryvnia",
            "UGX": "Ugandan Shilling",
            "UYU": "Uruguayan Peso",
            "UZS": "Uzbekistan Som",
            "VES": "Venezuelan Bolívar",
            "VND": "Vietnamese Đồng",
            "VUV": "Vanuatu Vatu",
            "WST": "Samoan Tala",
            "XAF": "Central African CFA Franc",
            "XCD": "East Caribbean Dollar",
            "XDR": "Special Drawing Rights",
            "XOF": "West African CFA Franc",
            "XPF": "CFP Franc",
            "YER": "Yemeni Rial",
            "ZAR": "South African Rand",
            "ZMW": "Zambian Kwacha",
            "ZWL": "Zimbabwean Dollar"
        }

        return currency_names.get(currency_code, "Unknown Currency")

    def display_exchange_rates_table(self):
        # Clear existing items in the Treeview
        for item in self.exchange_rates_treeview.get_children():
            self.exchange_rates_treeview.delete(item)

        # Display the exchange rates in the Treeview
        for currency_code, exchange_rate in self.exchange_rates.items():
            self.exchange_rates_treeview.insert("", tk.END, values=(currency_code, exchange_rate))

    def get_exchange_rate(self, currency_code):
        # Get the exchange rate for 1 USD to the specified currency
        rate = self.exchange_rates.get(currency_code)
        return rate if rate is not None else "N/A"


def main():
    root = tk.Tk()  # Create the main Tkinter root window
    app = CurrencyConverterApp(root)  # Create an instance of the CurrencyConverterApp, passing the root window
    app.update_conversion_history_tab()  # Call update_conversion_history_tab to load the conversion history
    root.mainloop()  # Start the Tkinter event loop


if __name__ == "__main__":
    main()

"""
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
"""