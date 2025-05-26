from azure_ri_utils import get_real_ri_usage
from email_utils import save_alert_report, export_to_csv

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
    subscription_id = "your-subscription-id-here"  # 用 az account show 查询并替换
    records = get_real_ri_usage(subscription_id)

    alerts = check_underutilization(records)
    if alerts:
        print(f"[⚠️] Found {len(alerts)} underutilized RIs")
        save_alert_report(alerts)
        export_to_csv(alerts)
    else:
        print("[✓] No underutilized RIs detected.")

if __name__ == "__main__":
    main()
