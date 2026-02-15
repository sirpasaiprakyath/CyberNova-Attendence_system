
try:
    import pandas
    print("pandas imported successfully")
except ImportError as e:
    print(f"pandas import failed: {e}")

try:
    import openpyxl
    print("openpyxl imported successfully")
except ImportError as e:
    print(f"openpyxl import failed: {e}")
