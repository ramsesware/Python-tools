# Python-tools
I'll be pushing on this repository all my python tools 

## 1. H4CK1NG_T00L.py

### Description:
`H4CK1NG_T00L.py` is a tool currently **under development**, with the goal of becoming a comprehensive suite of penetration testing tools integrated into a single graphical interface. The focus is on **ease of use** and **user-friendly GUI**, allowing penetration testers to perform common tasks more efficiently. At this stage of development, the script includes the following features:

### Features:
- **Web Directory Analysis:** Performs a dictionary-based analysis of possible web directories, checking their availability via HTTP/HTTPS requests.


### Future Development:
The goal of `H4CK1NG_T00L.py` is to incorporate various tools used in penetration testing, all accessible from a single graphical user interface, prioritizing ease of use and productivity for both beginners and advanced users in the cybersecurity field.

### Usage:
Run the script, and it will open a GUI where you can input a URL to search for images or analyze directories. The results will be displayed in the GUI along with real-time updates.

### Dependencies:
- `tkinter`
- `requests`
- `beautifulsoup4`

---

## 2. Contability.py

### Description:
`Contability.py` is a personal finance management tool that allows users to track income and expenses through a graphical interface. It includes features for recording transactions, viewing the transaction history, and displaying a visual graph of the user's financial balance.

### Features:
- **Income and Expense Tracking:** Users can input their income and expenses, which are saved locally.
- **Graphical Visualization:** The script uses `matplotlib` to display a dynamic graph of the user's total balance based on their financial records.
- **Transaction History:** Displays a history of both income and expense transactions within the GUI.
- **Balance Calculation:** Automatically calculates and updates the total financial balance based on user input.

### Usage:
Launch the script to open the GUI. From there, you can add new income or expense records, view transaction history, and visualize your financial balance over time.

### Dependencies:
- `tkinter`
- `matplotlib`

---

## Windows Users: Running the Script with a Single Click

If you are a Windows user, you can create a `.bat` file to execute the Python script with a single click. Follow these steps to set it up:

### Steps:
1. **Create a `.bat` file**:
    - Open **Notepad** or any text editor and paste the following code:
    ```bat
    start "" "C:/Users/YOUR_USER_NAME/AppData/Local/Microsoft/WindowsApps/python.exe" C:/path/to/your/script/H4CK1NG_T00L.py
    ```
    - Replace `YOUR_USER_NAME` with your actual Windows username.
    - Replace `C:/path/to/your/script/` with the actual path where your `H4CK1NG_T00L.py` file is located.

2. **Save the file**:
    - Save the file with a `.bat` extension, for example: `Run_H4CK1NG_T00L.bat`.

3. **Create a desktop shortcut**:
    - Right-click on the `.bat` file you just created and select **Create Shortcut**.
    - Drag this shortcut to your desktop for easy access.

4. **Change the icon (optional)**:
    - To make it more visually appealing, right-click on the shortcut, select **Properties**, and click on **Change Icon...**. 
    - You can choose any icon file you prefer or use a custom icon that represents your tool.

Now, when you double-click the shortcut on your desktop, the script will run automatically using Python.

---
