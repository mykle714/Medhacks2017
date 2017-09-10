from flask import Flask, render_template, request, make_response, redirect
from logic import Logic
import api
app = Flask(__name__)

home = "http://127.0.0.1:5000/"
logic = Logic()

@app.route("/")
def index():
    return redirect("%smainpage.html" % home, code=302)

@app.route("/mainpage.html", methods=["GET","POST"])
def main():
    if request.method == "POST" and request.form['button'] == 'submit':
        email = request.form["email"]
        password = request.form["password"]
        logic.setUser(logic.login(email, password))
        if logic.user is not None:
            return redirect("%smainmenu.html" % home, code=302)
    return render_template("mainpage.html")

@app.route("/registrationpage.html", methods=["GET", "POST"])
def reg1():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        birthday = request.form['birthday']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']

        if name == "" or email == "" or birthday == "" or address == "" or phone == "" or password == "":
            return render_template("registrationpage.html")
        else:
            logic.setUser(api.Patient(name, birthday, address, phone, email, password))
            return redirect("%sregistrationpage2.html" % home, code=302)
    return render_template("registrationpage.html")

@app.route("/registrationpage2.html", methods=["GET", "POST"])
def reg2():
    if logic.user is None:
        return redirect("%smainpage.html" % home, code=302)
    if request.method =="POST":
        insurance = request.form['insurance']
        group = request.form['group']
        policy = request.form['policy']
        type = request.form['type']
        customer = request.form['customer']

        if insurance == "" or group == "" or policy == "" or type == "" or customer == "":
            return render_template("registrationpage2.html")
        else:
            logic.user.updateInsurance(insurance, group, policy, type, customer)
            logic.addPatient2(logic.user)
            logic.saveUser(logic.user)
            return redirect("%smainmenu.html" % home, code=302)
    return render_template("registrationpage2.html")

@app.route("/mainmenu.html")
def menu():
    if logic.user is None:
        return redirect("%smainpage.html" % home, code=302)
    return render_template("mainmenu.html")

@app.route("/profile.html")
def profile():
    if logic.user is None:
        return redirect("%smainpage.html" % home, code=302)
    return render_template("profile.html")

@app.route("/settings.html")
def settings():
    if logic.user is None:
        return redirect("%smainpage.html" % home, code=302)
    return render_template("settings.html")

@app.route("/signout.html")
def signout():
    logic.clearUser()
    return redirect("%smainpage.html" % home, code=302)

if __name__ == "__main__":
    app.run()
