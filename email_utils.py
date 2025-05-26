import os
import csv
from datetime import datetime

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
