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
        writer.writerow(['Sr No.','Reference No (URN)', 'Journal Date' ,'Date of Purchase',
                         'Date of Expiry', 'Name of the Purchaser' ,'Prefix' ,'Bond Number',
                         'Denominations' ,'Issue Branch Code' ,'Issue Teller' ,'Status'])

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
    # print(lines[0:1000])

    # Initialize an empty list to store preprocessed data
    preprocessed_data = []
    a = 0
    b = 1

    # Loop through each line in the text
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Skip lines containing headers and footer
        if any(header_word in line for header_word in ["Sr No.",'Journal','Reference','Date of', 'Purchase','Date of Expiry','Name of the Purchaser','Prefix','Status','Bond','Number Denominations','Issue Branch','Code','Issue Teller', "Page"]):
            continue

        if a == 0:
          if ' ' in line:
            serial_no = line.split(' ')[0]
            reference_no = line.split(' ')[1]
            a = 2
            continue
          else:
            serial_no = line
            a+=1
        elif a==1:
          reference_no = line
          a+=1
        elif a==2:
          if ' ' in line:
            journal_date = line.split(' ')[0]
            Date_of_purchase = line.split(' ')[1]
            a = 4
            continue
          else:
            journal_date = line
            a+=1
        elif a==3:
          Date_of_purchase = line
          a+=1
        elif a==4:
          if ' ' in line:
            Date_of_Expiry = line.split(' ')[0]
            name_of_purchaser = ' '.join(line.split(' ')[1:])
            a = 6
            continue
          else:
            Date_of_Expiry = line
            a+=1
        elif a==5:
          name_of_purchaser = line
          a+=1
        elif a==6:
          prefix = line
          a+=1
        elif a==7:
          bond_no = line
          a+=1
        elif a==8:
          denominations = line
          a+=1
        elif a==9:
          branch_code = line
          a+=1
        elif a==10:
          issue_teller = line
          a+=1
        elif a==11:
          status = line

          # Rearrange the data to have 12 columns
          row = [
              serial_no,
              reference_no,
              journal_date,
              Date_of_purchase,
              Date_of_Expiry,
              name_of_purchaser,
              prefix,
              bond_no,
              denominations,
              branch_code,
              issue_teller,
              status
          ]
          # if b<5000:
          #   print(row)
          #   b+=1
          # print(row)

          # Append the processed row to the preprocessed data list
          preprocessed_data.append(row)
          a = 0

    return preprocessed_data



# Example usage:
pdf_path = '/content/Table_2.pdf'
csv_path = '/content/Table_2.csv'
convert_pdf_to_csv(pdf_path, csv_path)

# text = extract_text_from_pdf(pdf_path)
# print(text)

# preprocessed = preprocess_data(text)
# print(preprocessed)
