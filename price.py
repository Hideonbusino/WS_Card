from imports import *

#helper function:returns a string with only characters
def extract_characters(s):
    whitelist = r'[a-zA-Z0-9\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
    return ''.join(re.findall(whitelist, s))
#helper function: returns a list with mercari products [name, price, availability]
def extract_item_details(output, text):
    results = []
    for line in output:
        # Check if every character in 'text' exists in the current line
        if all(char.lower() in line.lower() for char in text):
            item = {}
            
            # Check if the item is sold out
            if "売り切れ" in line:
                item['availability'] = "sold out"
            else:
                item['availability'] = "available"
                item['name'] = re.split(r"の画像", line)[0]
            item['product_name'] = re.sub('\u3000', ' ', re.split(r"の画像", line)[0])
            item['price'] = re.search(r"(\d+,?\d+)(円)", line).group(1)
            results.append(item)
    return results

#helper function: append df to csv
def to_csv(df, file_name):
 # Check if DataFrame is valid and non-empty
    if df is None or df.empty:
        print("Error: Invalid or empty DataFrame provided.")
        return

    try:
        # Check if file exists, read existing data, and append the new data
        if os.path.exists(file_name):
            existing_data = pd.read_csv(file_name)
            df = pd.concat([existing_data, df], ignore_index=True)

        # Write the DataFrame to csv
        df.to_csv(file_name, index=False)
        #print(f"Data has been appended to '{file_name}'.")

    except PermissionError:
        print(f"Error: Permission denied. Can't write to '{file_name}'.")
    except FileNotFoundError:
        print(f"Error: Invalid path specified: '{file_name}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#helper function: estimates the  final price
def price(df, info, letter):
    try:
        # Ensure the DataFrame has the expected columns
        if not set(['price', 'availability']).issubset(df.columns):
            print(f"Error: DataFrame doesn't have the required columns for {info[1]}.")
            return -1

        # Safely convert price to integer
        df['price'] = df['price'].str.replace(',', '', regex=False).astype(int)

        # Calculate IQR for price, with checks for dataframe length
        if len(df) < 4:  # Arbitrary threshold; adjust as needed
            print(f"Warning: Results for {info[1]} has only {len(df)} row(s). Results might not be reliable.")

        Q1 = df['price'].quantile(0.25)
        Q3 = df['price'].quantile(0.75)
        IQR = Q3 - Q1
        median = df['price'].median()
        # Define bounds for outliers
        lower_bound = Q1 / 2.5
        upper_bound = Q3 * 3
        print(f"Lower bound: {lower_bound}, upper bound: {upper_bound}")
        # Filter out outliers
        df_filtered = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]

        # Calculate average price for available items
        df_available = df_filtered[df_filtered['availability'] == 'available'].reset_index(drop=True)
        sorted_available = df_available.sort_values(by=['price'], ascending=True)
        if len(sorted_available) >= 2:
            available_price = sorted_available.iloc[:2]['price'].mean()
        elif len(sorted_available) == 1:
            available_price = sorted_available['price'].mean()
        else:
            available_price = 0

        # Calculate weighted average price for sold items
        df_sold = df_filtered[df_filtered['availability'] == 'sold out'].reset_index(drop=True)
        df_sold['recency_weight'] = df_sold.index[::-1] + 2
        numerator = (df_sold['price'] * df_sold['recency_weight']).sum()
        denominator = df_sold['recency_weight'].sum()

        # Check for division by zero
        if denominator == 0:
            sold_price = 0
        else:  
            sold_price = numerator / denominator
        #print(f"available: {available_price}, sold: {sold_price}")
        if available_price == 0:
            final_price = sold_price
        elif sold_price == 0:
            final_price = available_price
        else:
            final_price = (available_price + sold_price) / 2
        final_price = round(final_price, -1)
        #print(f"Final price for {info[1]}: {final_price}")
        price_row = pd.DataFrame({'id': [info[0]], 'estimated_price': [final_price], 'name': [info[1]], 'no_of_items': [len(df)], 
                                            'sold_items': [len(df_sold)], 'available_items': [len(df_available)], 'grade': [letter], 
                                            'yuyu_price': [info[2]], 'yuyu_av': [info[3]]})
        to_csv(price_row, price_csv_path)
        return final_price

    except Exception as e:
        print(f"An error occurred for {info[1]}: {e}")
        return -1

#main function: returns a dataframe with the following columns: id, name, price, availability
def mercari(info, letter):
    try:
        #service = Service(r"C:/SeleniumDriver/chromedriver.exe")

        # Build the URL
        url = 'https://jp.mercari.com/search?keyword=' + re.sub(' ', '%20', info[1])
        print(url)
        # Initialize the WebDriver
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(3)  # Adjust this sleep time if needed

        # Get page source and parse with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ensure driver is closed after extraction
        driver.quit()

        # Extract required elements
        div_elems = soup.find_all('div', class_='merItemThumbnail fluid__a6f874a2', limit=15)
        if not div_elems:
            print(f"Warning: No elements found on the Mercari page for {info[1]}. (1)")
            return -1

        elems = [elem['aria-label'] for elem in div_elems if 'aria-label' in elem.attrs]

        # Check if any elements were found
        if not elems:
            print(f"Warning: No elements found on the Mercari page for {info[1]}. (2)")
            return -1

        data = extract_item_details(elems, extract_characters(info[1]))
        if not data:
            print(f"Warning: No elements found on the Mercari page for {info[1]}. (3)")
            return -1
        for item in data:
            item['id'] = info[0]
            item['name'] = info[1]
        # Create DataFrame and save to csv
        df = pd.DataFrame(data, columns=['id', 'name','product_name', 'price', 'availability'])
        to_csv(df, raw_csv_path)
        price(df, info, letter)
        
        return df

    except Exception as e:
        print(f"An error occurred in the 'mercari' function for {info[1]}: {e}")
        return -1

