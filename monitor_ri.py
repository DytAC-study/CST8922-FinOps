# Main script (to be filled in manually)from azure_ri_utils import get_mock_ri_usage  # 也可以换成 get_real_ri_usage
from email_utils import save_alert_report, export_to_csv, send_daily_alert_email

def check_underutilization(usage_records, threshold=0.8):
    alerts = []
    for r in usage_records:
        used = r["quantity"]
        reserved = r.get("reserved_quantity", 100)
        utilization = used / reserved if reserved else 0
        if utilization < threshold:
            alerts.append({
                "instance": r["instance_id"],
                "sku": r["sku_name"],
                "utilization": utilization
            })
    return alerts

def main():
    records = get_mock_ri_usage()
    alerts = check_underutilization(records)

    if alerts:
        print(f"[⚠️] Found {len(alerts)} underutilized RIs")
        save_alert_report(alerts)
        export_to_csv(alerts)
        send_daily_alert_email(alerts)
    else:
        print("[✓] No underutilized RIs detected.")

if __name__ == "__main__":
    main()
