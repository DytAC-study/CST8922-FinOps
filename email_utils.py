import os
import smtplib
import csv
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def save_alert_report(alerts, output_dir="alerts"):
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ri_alert_{now}.html"
    filepath = os.path.join(output_dir, filename)

    html = "<h2>Reserved Instances Underutilization Alert</h2><ul>"
    for a in alerts:
        html += f"<li><strong>{a['instance']}</strong> ({a['sku']}): {a['utilization']*100:.2f}%</li>"
    html += "</ul>"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[✅] Alert report saved to: {filepath}")

def export_to_csv(alerts, output_dir="alerts"):
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ri_alert_{now}.csv"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["instance", "sku", "utilization"])
        writer.writeheader()
        for a in alerts:
            writer.writerow(a)

    print(f"[📄] CSV report saved to: {filepath}")

def send_email(subject, html_body, recipient="recipient@example.com"):
    try:
        msg = MIMEText(html_body, "html")
        msg["Subject"] = subject
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)

        print(f"[📧] Email sent to {recipient}")
    except Exception as e:
        print(f"[❌] Failed to send email: {e}")

def send_daily_alert_email(alerts):
    html_body = "<h2>Daily RI Underutilization Alert</h2><ul>"
    for a in alerts:
        html_body += f"<li><strong>{a['instance']}</strong> ({a['sku']}): {a['utilization']*100:.2f}%</li>"
    html_body += "</ul>"
    send_email("Daily RI Alert – Low Utilization", html_body)

def send_monthly_cost_email(summary):
    html_body = "<h2>Monthly RI Waste Report (UnusedReservation)</h2><table border='1'><tr><th>Reservation ID</th><th>Days</th><th>Cost</th><th>Groups</th></tr>"
    for rid, val in summary.items():
        html_body += f"<tr><td>{rid}</td><td>{val['entries']}</td><td>${val['cost']:.2f}</td><td>{', '.join(val['resource_groups'])}</td></tr>"
    html_body += "</table>"

    analysis = "<h3>🔎 FinOps Analysis & Suggested Actions</h3><ul>"
    for rid, val in summary.items():
        cost = val["cost"]
        days = val["entries"]
        if days >= 5:
            suggestion = "Repeated underuse. Investigate long-term allocation."
        elif days >= 3 and cost > 25:
            suggestion = "Consider exchanging or reallocating."
        elif cost < 10:
            suggestion = "Minor cost. Can be monitored or ignored."
        else:
            suggestion = "Monitor closely."
        analysis += f"<li><strong>{rid}</strong>: {suggestion} Cost wasted: ${cost:.2f} over {days} days.</li>"
    analysis += "</ul>"

    html_body += analysis
    send_email("Monthly RI Report – UnusedReservation Summary", html_body)
