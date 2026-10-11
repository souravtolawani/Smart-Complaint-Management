
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, add_complaint, get_complaints, update_complaint_status

app = Flask(__name__)
app.secret_key = "resolvehub-demo-key"

init_db()


@app.route("/")
def home():
    complaints = get_complaints()

    total = len(complaints)
    pending = sum(c["status"] == "Pending" for c in complaints)
    in_progress = sum(c["status"] == "In Progress" for c in complaints)
    resolved = sum(c["status"] == "Resolved" for c in complaints)

    return render_template(
        "index.html",
        complaints=complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved
    )


@app.route("/submit", methods=["GET", "POST"])
def submit_complaint():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        priority = request.form.get("priority", "").strip()
        description = request.form.get("description", "").strip()

        allowed_categories = {
            "IT Support", "Infrastructure", "Maintenance",
            "Academics", "Other"
        }
        allowed_priorities = {"Low", "Medium", "High"}

        if (
            not title or len(title) > 100
            or not description or len(description) > 2000
            or category not in allowed_categories
            or priority not in allowed_priorities
        ):
            flash("Please enter valid complaint details.", "error")
            return redirect(url_for("submit_complaint"))

        add_complaint(title, category, priority, description)
        flash("Complaint submitted successfully!", "success")
        return redirect(url_for("home"))

    return render_template("submit_complaint.html")


@app.route("/update-status/<int:complaint_id>", methods=["POST"])
def update_status(complaint_id):
    new_status = request.form.get("status", "").strip()

    if update_complaint_status(complaint_id, new_status):
        flash("Complaint status updated successfully!", "success")
    else:
        flash("Unable to update complaint status.", "error")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
