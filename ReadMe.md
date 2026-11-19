<br><img src="images/coinhub.png" alt="Coin Hub Logo" height="70px" width="210px" id="top">

---

###### Developed By BSIT-4J Group

![Version](https://img.shields.io/badge/Version-0.1-blue)
![Build](https://img.shields.io/badge/Build-0.7-green)
![Release](https://img.shields.io/badge/Release-Unofficial-red)

---

### Overview 
**Coin Hub** is an API-powered application that lets users view the latest currency prices and perform currency conversions all in one place.  
This project is intended for testing, practice, and educational development.

##### *Disclaimer* 
We do not claim ownership of any images or the API used in this project.  
All rights belong to their respective owners.


---

### How to run Coin Hub
- **🚀 Prebuilt Executable**: A prebuilt executable named `CoinHub.exe` is included and runs the full program.
  - The executable may be flagged as suspicious by some systems because it was packaged using a standard open-source compiler.  
  Code-signing certificates could prevent this, but they are expensive and not practical for a small non-commercial project.  
  Rest assured, the program is completely safe and free of any malicious content.
  - - If the file is not included in the repo, you can download the game here: [Download Coin Hub](https://drive.google.com/file/d/1vcptt78fvT6sOd_wIW66wJTO_JDLyE3G/view?usp=drive_link)
- **Compiler**: Use any IDE **(e.g. PyCharm or VS Code)** and open the folder that contains this file and run the file named `HomePage.py`.
- **Note**: Do ensure that you have internet access before running Coin Hub

---

## Coin Hub Features

---

#### Tutorial Mechanics
The application checks if the user is opening it for the first time.
It checks the file `/datas/first_time.json`, If the file does not exist, the tutorial starts automatically.

The file stores a dictionary with a key `complete` and a value of either **1** or **2**:  
**1** → Marks the **HomePage** tutorial as complete.  
**2** → Marks the **Currency Conversion** Page tutorial as complete.  

##### Additional Notes
- If the app is closed before completing a tutorial, it will restart based on the saved data.  
- To restart the tutorial manually, delete `datas/first_time.json`.

---

#### Currency Feature
- A listview panel that displays the current value/price of currencies.
- Price calculation, Convert from one currency to another.
- A dropdown list for selection of currency in **Conversion Page**.

---

#### Proper Error Handling
- **Input Validation** - The input field will only accept whole numbers or with decimals, other characters will display an error or invalid input.
- **Requests handling** - An error page is displayed for users, while detailed tracebacks appear in the console for developers to debug efficiently.
    - To test this feature, try turning off internet connection before launching Coin Hub.
    - There's also **Reload** button within this page allowing the application to try make new requests.
    - If successful, then it will close the error page and open the main page.

---

#### Other Feature(s)
- A **5 mins of interval** between new data requests helps maintain consistency.
    - Results may not be noticeable due to values being rounded to three decimal places.

---

[Go to Top](#top)


