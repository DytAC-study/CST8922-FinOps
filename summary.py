from azure_ri_utils import get_mock_ri_usage  # 可替换为 get_real_ri_usage
from monitor_ri import check_underutilization
from parse_cost_details import load_mock_cost_data, analyze_unused_reservations
from email_utils import (
    save_alert_report,
    export_to_csv,
    send_daily_alert_email,
    send_monthly_cost_email,
)

def summarize_ri_status():
    print("\n🔍 Step 1: Checking RI utilization status (daily)...")
    usage_records = get_mock_ri_usage()
    alerts = check_underutilization(usage_records)

    if alerts:
        print(f"⚠️  Found {len(alerts)} underutilized RIs. Saving daily report...")
        save_alert_report(alerts)
        export_to_csv(alerts)
        send_daily_alert_email(alerts)
    else:
        print("✓ No low-utilization RIs detected today.")

    print("\n📊 Step 2: Analyzing monthly RI cost waste...")
    cost_data = load_mock_cost_data()
    summary = analyze_unused_reservations(cost_data)
    send_monthly_cost_email(summary)

if __name__ == "__main__":
    summarize_ri_status()
