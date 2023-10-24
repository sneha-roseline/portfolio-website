from flask import Flask, render_template ,request, redirect
import time
import smtplib
import os
import csv

#Initiate flask app
app = Flask(__name__)

# Define a route to render the HTML template.
@app.route('/')
def home_page():
    return render_template("index.html")


# Define a route to handle form submission.
@app.route('/submit_form',methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_data_csv(data)
            return render_template("index.html",code="test()")
        except PermissionError:
            message = "Permission denied when trying to save data."
            return render_template('index.html', message=message)
        except FileNotFoundError:
            message = "CSV file not found."
            return render_template('index.html', message=message)
        except Exception as e:
            message = f"An error occurred: {str(e)}"
            return render_template('index.html', message=message)
    else:
        message = "FORM NOT SUBMITTED"
        return render_template('index.html', message=message)

@app.route('/<string:page_name>')
def page(page_name='/'):
    try:
        return render_template(page_name)
    except:
        return redirect('/')    

def write_data_csv(data):
    name = data['name']
    email = data['email']
    message = data["message"]
    with open('db.csv', 'a', newline='') as csvfile:
        db_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        db_writer.writerow([name, email, message])

if __name__ == '__main__':
    app.run(debug=True)