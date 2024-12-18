# Python-tools
I'll be pushing on this repository all my python tools 

## 1. Contability.py

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
    start "" "C:/Users/YOUR_USER_NAME/AppData/Local/Microsoft/WindowsApps/python.exe" C:/path/to/your/script/Contability.py
    ```
    - Replace `YOUR_USER_NAME` with your actual Windows username.
    - Replace `C:/path/to/your/script/` with the actual path where your `Contability.py` file is located.

2. **Save the file**:
    - Save the file with a `.bat` extension, for example: `Run_Contability.bat`.

3. **Create a desktop shortcut**:
    - Right-click on the `.bat` file you just created and select **Create Shortcut**.
    - Drag this shortcut to your desktop for easy access.

4. **Change the icon (optional)**:
    - To make it more visually appealing, right-click on the shortcut, select **Properties**, and click on **Change Icon...**. 
    - You can choose any icon file you prefer or use a custom icon that represents your tool.

Now, when you double-click the shortcut on your desktop, the script will run automatically using Python.

---
