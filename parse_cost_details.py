import json
import os
from collections import defaultdict
from tabulate import tabulate
from email_utils import (
    send_monthly_cost_email,
    save_alert_report,
    export_to_csv
)

def load_mock_cost_data(file_path="data/mock_cost_management_output.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_unused_reservations(data):
    columns = [col["name"] for col in data["columns"]]
    col_index = {name: i for i, name in enumerate(columns)}
    unused_rows = [row for row in data["rows"] if row[col_index["ChargeType"]] == "UnusedReservation"]

    summary = defaultdict(lambda: {"cost": 0, "entries": 0, "resource_groups": set()})
    for row in unused_rows:
        rid = row[col_index["ReservationId"]] or "Unknown"
        summary[rid]["cost"] += row[col_index["PreTaxCost"]]
        summary[rid]["entries"] += 1
        summary[rid]["resource_groups"].add(row[col_index["ResourceGroupName"]])

    # Print terminal summary
    results = []
    for rid, val in summary.items():
        results.append([
            rid,
            val["entries"],
            round(val["cost"], 2),
            ", ".join(val["resource_groups"])
        ])

    headers = ["Reservation ID", "Days Underutilized", "Total Unused Cost", "Resource Groups"]
    print(tabulate(results, headers=headers, tablefmt="github"))

    # Email summary
    send_monthly_cost_email(summary)

    # Simulate alert structure for saving local report
    alerts = [
        {
            "instance": rid,
            "sku": "unknown",
            "utilization": max(0, 1 - (val["cost"] / 100))  # 估算，100 代表原值
        }
        for rid, val in summary.items()
    ]
    save_alert_report(alerts, output_dir="alerts/monthly")
    export_to_csv(alerts, output_dir="alerts/monthly")

    return summary

if __name__ == "__main__":
    cost_data = load_mock_cost_data()
    analyze_unused_reservations(cost_data)
