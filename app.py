import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory, make_response
from flask_session import Session
import pdfkit
import random
import requests
from datetime import datetime
import string

#configure - always needs to be in flask app
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///bread.db")

#reference generator
def generate_reference(date_for_order, pattern):

    #change the format of the date to YYMMDD

    formatted_date = datetime.strptime(date_for_order, "%d-%m-%Y").strftime("%y%m%d")


    gen_reference = pattern.format(VARIABLE=formatted_date)
    gen_reference = ''.join(random.choice(string.ascii_uppercase + string.digits) if c.isalpha() else c for c in gen_reference)

    return gen_reference

def add_cors_headers(response):
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Add CORS headers to responses for CSS file
@app.route('/static/styles.css')
def css_with_cors():
    css_content = send_from_directory('static', 'styles.css')  # Replace with the actual path to your CSS file
    response = make_response(css_content)
    return add_cors_headers(response)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "public, max-age=3600"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    # SHOW MAIN PAGE

    return render_template("index.html")

@app.route("/gallery")
def gallery():
    # SHOW MAIN PAGE

    return render_template("gallery.html")

@app.route("/offer")
def offer(choice='default_choice'):
    # SHOW MAIN PAGE

    return render_template("offer.html", selected_option=choice)


@app.route("/preorder", methods=["GET", "POST"])
def preorder():
    # PREORDER PAGE
    if request.method == "POST":
        #get form data

        chleba = request.form.get("chleba")
        quantity = request.form.get("quantity")
        firstname = request.form.get("firstname")
        surname = request.form.get("surname")
        email = request.form.get("email")
        date_for_order = request.form.get("date_for_order")


        pattern = "{VARIABLE}-REFE"
        reference = generate_reference(date_for_order, pattern)


        #store the above data in a variable until button on the confirmation page is clicked

        session['preorder_data'] = {
             'chleba' : chleba,
             'quantity' : quantity,
             'firstname' : firstname,
             'surname' : surname,
             'email' : email,
             'reference' : reference,
             'date_for_order' : date_for_order
        }

        #redirect to the next page

        return redirect(url_for('payment_simulation'))

    else:
        selected_option = request.args.get('choice', 'default_choice')
        return render_template("preorder.html", selected_option=selected_option)

@app.route("/payment_simulation", methods=["GET", "POST"])
def payment_simulation():
    #retrieve the data from the session (form that was filled in previous step)

    preorder_data = session.get("preorder_data", None)

    if preorder_data is None:
        return redirect(url_for('preorder'))

    elif preorder_data:
        chleba = preorder_data['chleba']
        quantity = preorder_data['quantity']
        firstname = preorder_data['firstname']
        surname = preorder_data['surname']
        email = preorder_data['email']
        reference = preorder_data['reference']
        date_for_order = preorder_data['date_for_order']

    if request.method == 'POST':

        #perform action to submit the data into the database


        db.execute("INSERT INTO bread_orders (id, firstname, surname, reference, bread, quantity, email, date_for_order) VALUES (NULL, :firstname, :surname, :reference, :bread, :quantity, :email, :date_for_order)",
                   firstname=firstname, surname=surname, reference=reference, bread=chleba, quantity=quantity, email=email, date_for_order=date_for_order)

        #clear the session variable

        return redirect(url_for('confirm_order'))

    return render_template('payment_simulation.html', preorder_data=preorder_data)



@app.route("/confirm_order")
def confirm_order():

        preorder_data = session.get("preorder_data", None)

        if preorder_data is None:

            return redirect(url_for('preorder'))

        elif preorder_data:
            chleba = preorder_data['chleba']
            quantity = preorder_data['quantity']
            firstname = preorder_data['firstname']
            surname = preorder_data['surname']
            email = preorder_data['email']
            reference = preorder_data['reference']
            date_for_order = preorder_data['date_for_order']

            session.clear()

        return render_template('confirm_order.html', chleba=chleba, quantity=quantity, firstname=firstname, surname=surname, email=email, reference=reference, date_for_order=date_for_order)


@app.route("/contact",  methods=["GET", "POST"])
def contact():


    url = "/templates/mail.php"  # Replace with the actual URL where your mail.php script is hosted

        # Replace these values with the actual data you want to send
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'Hello, this is a test message!',
        'subject': 'Test Subject'
    }

    if request.method == 'POST':

        try:

            response = requests.post(url, data=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print("Email sent successfully!")
            else:
                    print(f"Error: {response.status_code} - {response.text}")

        except requests.RequestException as e:
                print(f"Request error: {e}")


    return render_template('contact.html')


@app.route("/change_order",  methods=["GET", "POST"])
def change_order():
    # CHANGE ORDER USING UNIQUE REFERENCE
    if request.method == "POST":

         #PULL UP THE TABLE BASED ON THE REFERENCE
        if 'lookup' in request.form:
            reference = request.form.get("reference")
            result = db.execute("SELECT * from bread_orders WHERE reference =?", reference)

            if result:
                order = result[0]

                date_for_order_str = order["date_for_order"]
                today = datetime.today().date()

                if date_for_order_str:
                    date_for_order = datetime.strptime(date_for_order_str, "%d-%m-%Y").date()

                    if date_for_order > today:
                        return render_template("change_order.html", result=result, reference=reference)
                    else:
                        flash('This order cannot be adjusted anymore.', 'error')
                        return render_template("change_order.html")
            else:
                flash('Order does not exist.', 'error')
                return render_template("change_order.html")


        elif 'make_change' in request.form:

             reference = request.form.get("reference")
             existing_order = db.execute("SELECT * FROM bread_orders WHERE reference =?", reference)

             if existing_order:

                # Get the new values from the form
                bread = request.form.get("chleba")
                quantity = request.form.get("quantity")
                firstname = request.form.get("firstname")
                surname = request.form.get("surname")
                email = request.form.get("email")
                date_for_order = request.form.get("date_for_order")

                # Build the update query dynamically based on provided fields
                update_query = "UPDATE bread_orders SET "
                update_params = []

                if bread:
                    update_query += "bread=?, "
                    update_params.append(bread)

                if quantity:
                    update_query += "quantity=?, "
                    update_params.append(quantity)

                if firstname:
                    update_query += "firstname=?, "
                    update_params.append(firstname)

                if surname:
                    update_query += "surname=?, "
                    update_params.append(surname)

                if email:
                    update_query += "email=?, "
                    update_params.append(email)

                if date_for_order:
                    update_query += "date_for_order=?, "
                    update_params.append(date_for_order)

                # Remove the trailing comma and add the WHERE clause
                update_query = update_query.rstrip(', ') + " WHERE reference=?"

                # Append the reference to the parameters
                update_params.append(reference)

                # Execute the update query
                db.execute(update_query, *update_params)

                return redirect(url_for('show_updated_order', reference=reference))
             else:
                 # Handle case where order with given reference doesn't exist
                flash('Order not found!', 'error')
                return redirect(url_for('change_order'))

        return redirect(url_for('show_updated_order', reference=reference))


    return render_template("change_order.html")

@app.route("/show_updated_order/<reference>/")
def show_updated_order(reference):

    updated_order = db.execute("SELECT * FROM bread_orders WHERE reference=?", reference)

    return render_template("change_order.html", result=updated_order, reference=reference)
