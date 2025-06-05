import csv

def getImageData():
    dict1 = {}
    try:
        with open("Images/imageData.csv", 'r', encoding='utf-8-sig') as names:
            reader = csv.reader(names)
            for row in reader:
                # Skip empty rows and rows with fewer than 2 columns
                if len(row) >= 2 and row[0] and row[1]:
                    try:
                        dict1[row[0].strip()] = int(row[1].strip())
                    except ValueError:
                        print(f"Skipping invalid calorie value in row: {row}")
    except FileNotFoundError:
        print("Error: imageData.csv file not found")
        return {}
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}
    return dict1