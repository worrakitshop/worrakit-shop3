
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "please-change-this-in-production"

ADMIN_USER = "sudket204"
ADMIN_PASS = "1329900935042"

computers = [
    {"id": 1, "name": "เครื่องที่ 1", "spec": "Intel Core Ultra 9 + RTX 5070"},
    {"id": 2, "name": "เครื่องที่ 2", "spec": "Ryzen 7 7800X3D + RX 9060 XT"},
]
bookings = []

@app.route("/")
def index():
    decorated = []
    for b in bookings:
        comp = next((c for c in computers if c["id"] == b["computer_id"]), None)
        decorated.append({**b, "computer_name": comp["name"] if comp else f"#{b['computer_id']}"})
    return render_template("index.html",
                           title="Worrakit Shop — บริการเช่าคอมพิวเตอร์เกมมิ่ง",
                           today=datetime.now().strftime("%d/%m/%Y"),
                           computers=computers,
                           bookings=decorated,
                           is_admin=session.get("admin", False))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("username")==ADMIN_USER and request.form.get("password")==ADMIN_PASS:
            session["admin"] = True
            flash("ล็อกอินสำเร็จ","success")
            return redirect(url_for("index"))
        flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง","danger")
    return render_template("admin.html", mode="login", title="เข้าสู่ระบบแอดมิน")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("ออกจากระบบแล้ว", "info")
    return redirect(url_for("index"))

@app.route("/book", methods=["POST"])
def book():
    if not session.get("admin"):
        flash("ต้องล็อกอินแอดมินก่อนถึงจะเพิ่มคิวได้","warning")
        return redirect(url_for("index"))
    name = request.form.get("name","").strip()
    computer_id = int(request.form.get("computer_id"))
    date = request.form.get("date")
    start = request.form.get("start")
    end = request.form.get("end")
    if not name or not date or not start or not end:
        flash("กรอกข้อมูลให้ครบ","danger"); return redirect(url_for("index"))
    for b in bookings:
        if b["computer_id"]==computer_id and b["date"]==date:
            if not (end <= b["start"] or start >= b["end"]):
                flash("ช่วงเวลานี้มีการจองแล้ว","warning")
                return redirect(url_for("index"))
    bookings.append({"name":name,"computer_id":computer_id,"date":date,"start":start,"end":end})
    flash("เพิ่มคิวแล้ว","success")
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete():
    if not session.get("admin"):
        flash("ต้องล็อกอินแอดมินก่อนถึงจะลบคิวได้","warning")
        return redirect(url_for("index"))
    idx = int(request.form.get("idx",-1))
    if 0 <= idx < len(bookings):
        bookings.pop(idx)
        flash("ลบคิวแล้ว","info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
