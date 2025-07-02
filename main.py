from flask import Flask, render_template, request, redirect, flash
import csv
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "sdfhisjwofekmdkmmjfiesf"

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

@app.route('/')
def home():
    products = []
    with open('data/hardware_inventory.csv', newline="", encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row)
    return render_template("index.html", products=products)

@app.route('/search')
def search():
    query = request.args.get('query')
    return f"Results for: {query}"

# Add dummy routes for navigation
@app.route('/produk')
def produk():
    return "Produk Page"

@app.route('/tentang')
def tentang():
    return render_template("tentang_kami.html")

@app.route('/company-profile')
def company_profile():
    return render_template("company-profile.html")

@app.route('/contact_us', methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        company = request.form.get("company")
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        email_body = f"""
        Nama Perusahaan : {company}
        Nama User : {name}
        Email : {email}
        Nomor Telepon : {phone}
        Kebutuhan: {message}
        """

        try:
            msg = MIMEText(email_body)
            msg["Subject"] = f"Inquiry baru dari {name}"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = EMAIL_ADDRESS

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            flash("Pesan berhasil terkirim, tim kami akan segera menghubungi anda!","success")
        except Exception as e:
            print(e)
            flash("Terjad kesalahan dalam mengirim pesan. Silakan mencoba sekali lagi atau kirim email ke 'suksesmandiricemerlang@gmail.com")

        return redirect("/contact_us")

    return render_template("contact_us.html")

@app.route('/software')
def software():
    return render_template('software.html')

@app.route('/hardware')
def hardware():
    selected_brands = request.args.getlist('brand')  # <-- this gets a list of all checked brands
    products = []

    with open('data/hardware_inventory.csv', newline="", encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not selected_brands or row['Brand'] in selected_brands:
                products.append(row)

    return render_template('hardware.html', products=products, selected_brands=selected_brands)

@app.route('/service')
def service():
    return render_template('service.html')

if __name__ == "__main__":
    app.run(debug=True)
