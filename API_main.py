import requests, json, ast, inspect

def throw_error():
    with open("datas/usable_data.json", "w") as file:
        json.dump({"status": "404Error"}, file, indent=4)



def get_currency_data():
    key = ""
    with open(".env/api_key.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        key = data["api_key"]
    api_key = key
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        with open("datas/collected_data.json", "w") as file:
            json.dump(data, file, indent=4)

        with open("datas/collected_data.json", "r") as f:
            data_re = ast.literal_eval(f.read())            # Collected data from requests are not in a valid JSON format, this will read them again and make them a valid JSON format
            temp = dict()
            coin = ('USD', 'KRW', 'EGP', 'ILS', 'JMD', 'EUR', 'JPY', 'PHP', 'CAD', 'AUD', 'BRL')

            for i in coin:
                temp[i] = data_re["rates"][i]           # Collect all specific data that is usable in this application

            with open("datas/usable_data.json", "w") as file:
                json.dump(temp, file, indent=4)         # Saved the usable data in another file in correct JSON format for easy access throughout the other pages

        return temp

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print(f"API/Line {inspect.currentframe().f_lineno}: APIKeyInvalid")

        if response.status_code == 403:
            print(f"API/Line {inspect.currentframe().f_lineno}: APIKeyForbidden")

        throw_error()

        return {"status": "404Error"}

    except requests.exceptions.InvalidURL as e:
        print(f"API/Line {inspect.currentframe().f_lineno}: Invalid URL")

        throw_error()

        return {"status": "404Error"}

    except requests.exceptions.MissingSchema as e:
        print(f"API/Line {inspect.currentframe().f_lineno}: Missing Schema")

        throw_error()

        return {"status": "404Error"}

    except requests.exceptions.ConnectionError as e:
        print(f"API/Line {inspect.currentframe().f_lineno}: Connection Error")

        throw_error()

        return {"status": "404Error"}

    except requests.exceptions.Timeout as e:
        print(f"API/Line {inspect.currentframe().f_lineno}: Timeout Error")

        throw_error()

        return {"status": "404Error"}

    except requests.exceptions.RequestException as e:
        print(f"API/Line {inspect.currentframe().f_lineno}: Failed to establish connection")

        throw_error()

        return {"status": "404Error"}

    except:
        print(f"API/Line {inspect.currentframe().f_lineno}: Aray K0Oooo error")

        throw_error()

        return {"status": "404Error"}



def update_saved_data():
    with open("datas/collected_data.json", "r") as f:
        data_re = ast.literal_eval(
            f.read())
        temp = dict()
        coin = ('USD', 'KRW', 'EGP', 'ILS', 'JMD', 'EUR', 'JPY', 'PHP', 'CAD', 'AUD', 'BRL')

        for i in coin:
            temp[i] = data_re["rates"][i]

        with open("datas/usable_data.json", "w") as file:
            json.dump(temp, file, indent=4)



# For testing purposes, specifically for successful data retrieval
def get_dummy_data():
    return {
    "USD": "1.0",
    "KRW": "1455.91",
    "EGP": "47.35",
    "ILS": "3.2445",
    "JMD": "159.88",
    "EUR": "0.864603",
    "JPY": "153.42",
    "PHP": "58.8825",
    "CAD": "1.40475",
    "AUD": "1.53953",
    "BRL": "5.33235"
}



def get_dummy_datas():                      # For testing purposes, specifically for error
    return {"status": "404Error"}