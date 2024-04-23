import fitz
import csv

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page in pdf_file:
            text += page.get_text()
    return text

def save_to_csv(data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the column headers
        writer.writerow(["Sr No.", "Date of Encashment", "Name of the Political Party",
                         "Account no. of Political Party", "Prefix", "Bond Number",
                         "Denominations", "Pay Branch Code", "Pay Teller"])
        # Write data to CSV
        for row in data:
            try:
                writer.writerow(row)
            except Exception as e:
                print(f"Error writing row to CSV: {e}")


def convert_pdf_to_csv(pdf_path, csv_path):
    text = extract_text_from_pdf(pdf_path)
    preprocessed = preprocess_data(text)
    save_to_csv(preprocessed, csv_path)

def preprocess_data(page_text):
    # Split the page text by lines
    lines = page_text.split('\n')

    # Initialize an empty list to store preprocessed data
    preprocessed_data = []
    a=1
    date = 0

    # Loop through each line in the text
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Skip lines containing headers and footer
        if any(header_word in line for header_word in ["Sr No.",'Date of', 'Encashment','Name of the Political Party','Account no. of','Political Party','Prefix','Bond','Number Denominations','Pay Branch','Code','Pay Teller', "Page"]):
            continue

        if a == 1:
          if ' ' in line:
            serial_no = line.split(' ')[0]
            date_and_party = ' '.join(line.split(' ')[1:])
            a = 3
          else:
            serial_no = line
            a+=1
        elif a==2:
          if date != 0:
            date_and_party = date + ' ' + line
            date = 0
            a +=1
          elif ' ' in line:
            date_and_party = line
            a += 1
          else:
            date = line
            continue
        elif a==3:
          account_no = line
          a+=1
        elif a==4:
          prefix = line
          a+=1
        elif a==5:
          bond_number = line
          a+=1
        elif a==6:
          denominations = line
          a+=1
        elif a==7:
          branch_code = line
          a+=1
        elif a==8:
          pay_teller = line

          # Rearrange the data to have 9 columns
          row = [
              serial_no,
              date_and_party.split(' ')[0],  # Extracting Date of Encashment from combined field
              ' '.join(date_and_party.split(' ')[1:]),  # Extracting Name of the Political Party from combined field
              account_no,
              prefix,
              bond_number,
              denominations,
              branch_code,
              pay_teller
          ]
          # print(row)

          # Append the processed row to the preprocessed data list
          preprocessed_data.append(row)
          a = 1

    return preprocessed_data


# preprocessed = preprocess_data(text)
# print(preprocessed)

# Example usage:
pdf_path = '/content/Table_1.pdf'
csv_path = '/content/Table_1.csv'
convert_pdf_to_csv(pdf_path, csv_path)

text = extract_text_from_pdf(pdf_path)
