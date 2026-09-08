import csv
import json
import logging

logging.basicConfig(filename="app.log", level=logging.ERROR)


# Read CSV
def read_csv(filename):
    file = open(filename, "r")
    data = list(csv.DictReader(file))
    file.close()
    return data


# Read JSON
def read_json(filename):
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    return data


# Check record
def check_record(record):

    if record["name"] == "":
        return "Name is missing"

    if "@" not in record["email"]:
        return "Email is invalid"

    if int(record["age"]) < 18:
        return "Age must be 18 or above"

    return ""

filename = input("Enter file name: ")

if filename.endswith(".csv"):
    records = read_csv(filename)

elif filename.endswith(".json"):
    records = read_json(filename)

else:
    print("Only CSV or JSON files are allowed")
    exit()


clean_records = []


for record in records:

    error = check_record(record)

    if error:

        print("Invalid:", record)
        print("Error:", error)

        logging.error(str(record) + " -> " + error)

    else:

        clean_records.append(record)


# Save clean records
file = open("cleaned_output.json", "w")
json.dump(clean_records, file, indent=4)
file.close()


print()
print("Done!")
print("Total records:", len(records))
print("Clean records:", len(clean_records))
print("Invalid records:", len(records) - len(clean_records))