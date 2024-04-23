from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nebular1!'
app.config['MYSQL_DB'] = 'assignment_4'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # Perform database query based on the search query
    # Replace 'your_query_here' with your actual database query
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM your_table WHERE column_name LIKE %s", ('%' + query + '%',))
    data = cursor.fetchall()
    cursor.close()
    return render_template("search_results.html", data=data)

@app.route('/company_individual', methods=['POST'])
def company_individual():
    company = request.form.get('company')
    # Perform database query to get data related to the selected company/individual
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM your_table WHERE company_individual = %s", (company,))
    data = cursor.fetchall()
    cursor.close()
    # Calculate total value of bonds purchased per year
    total_value = sum([row['amount'] for row in data])

    # Prepare data for bar plot
    companies = [row['company_individual'] for row in data]
    amounts = [row['amount'] for row in data]

    return render_template("company_individual.html", data=data, total_value=total_value, companies=companies, amounts=amounts)


@app.route('/political_party', methods=['POST'])
def political_party():
    party = request.form.get('party')
    # Perform database query to get data related to the selected political party
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM your_table WHERE political_party = %s", (party,))
    data = cursor.fetchall()
    cursor.close()
    # Calculate total value per year
    total_value = sum([row['amount'] for row in data])

    # Prepare data for bar plot
    parties = [row['political_party'] for row in data]
    amounts = [row['amount'] for row in data]

    return render_template("political_party.html", data=data, total_value=total_value, parties=parties, amounts=amounts)


@app.route('/donations_to_party', methods=['POST'])
def donations_to_party():
    party = request.form.get('party')
    # Perform database query to get data related to donations to the selected political party
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT company, SUM(amount) AS total_amount FROM your_table WHERE political_party = %s GROUP BY company", (party,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("donations_to_party.html", data=data)


@app.route('/donations_from_company', methods=['GET', 'POST'])
def donations_from_company():
    if request.method == 'POST':
        company = request.form.get('company')
        # Perform database query to get data related to donations from the selected company
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT political_party, SUM(amount) AS total_amount FROM your_table WHERE company = %s GROUP BY political_party", (company,))
        data = cursor.fetchall()
        cursor.close()
        return render_template("donations_from_company.html", data=data, companies=get_company_options(), selected_company=company)
    else:
        # Render the template with dropdown menu options
        return render_template("donations_from_company.html", companies=get_company_options())

def get_company_options():
    # Perform database query to get distinct company names
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT company FROM your_table")
    companies = cursor.fetchall()
    cursor.close()
    return [company['company'] for company in companies]

@app.route('/total_donations', methods=['POST'])
def total_donations():
    # Perform database query to get total donations to all parties
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT political_party, SUM(amount) AS total_amount FROM your_table GROUP BY political_party")
    data = cursor.fetchall()
    cursor.close()

    return render_template("total_donations.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
