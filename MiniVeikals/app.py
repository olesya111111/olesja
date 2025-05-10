from flask import Flask, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
def get_db_connection():
    """
    Izveido un atgriež savienojumu ar SQLite datubāzi.
    """
    db = Path(__file__).parent / "miniVeikals.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produkti/<int:product_id>")
def products_show(product_id):
    conn = get_db_connection()
    product = conn.execute(
        """
        SELECT products.*,
                taisitajs.name AS taisitajs_nosaukums,
                daudzums.name AS daudzums_nosaukums,
                zimols.name AS zimols_nosaukums   -- Šeit ir "zimoli"
        FROM products
        LEFT JOIN taisitajs ON products.taisitajs = taisitajs.id
        LEFT JOIN daudzums ON products.daudzums = daudzums.id
        LEFT JOIN zimols ON products.zimols = zimols.id   -- Un šeit
        WHERE products.id = ?
        """,
        (product_id,)
    ).fetchone()
    conn.close()
    return render_template("products_show.html", product=product)

@app.route("/razotajs/<int:taisitajs_id>")
def razotajs_show(taisitajs_id):
    conn = get_db_connection()
    razotajs = conn.execute("SELECT * FROM taisitajs WHERE id = ?", (taisitajs_id,)).fetchone()
    conn.close()
    return render_template("taisitajs.html", razotajs=razotajs)

@app.route("/daudzums/<int:daudzums_id>")
def daudzums_show(daudzums_id):
    conn = get_db_connection()
    daudzums = conn.execute("SELECT * FROM daudzums WHERE id = ?", (daudzums_id,)).fetchone()
    conn.close()
    return render_template("daudzums.html", daudzums=daudzums)

@app.route("/zimols/<int:zimols_id>")
def zimols_show(zimols_id):
    conn = get_db_connection()
    zimols = conn.execute("SELECT * FROM zimols WHERE id = ?", (zimols_id,)).fetchone()
    conn.close()
    return render_template("zimols.html", zimols=zimols)
@app.route("/produkti")
def products():
    conn = get_db_connection() 
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close() 

    return render_template("products.html", products=products)    

@app.route("/par-mums")

def about():
    return render_template("about.html")


from flask import request, redirect, url_for
@app.route("/produkti/new", methods=["GET", "POST"])
def product_create():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        conn = get_db_connection()
        conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
        return redirect(url_for("products"))
    return render_template("product_form.html")


@app.route("/produkti/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        conn.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", (name, price, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for("products_show", product_id=product_id))
    conn.close()
    return render_template("product_form.html", product=product)


@app.route("/produkti/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("products"))




if __name__ == "__main__":
    app.run(debug=True)