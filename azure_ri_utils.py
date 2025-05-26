import json
from datetime import datetime, timedelta
from azure.identity import AzureCliCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.core.exceptions import HttpResponseError
import os

def get_mock_ri_usage(file_path="data/mock_ri_usage.json"):
    print("[⚠️] Using mock RI usage data...")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_real_ri_usage(subscription_id, fallback_file="data/mock_ri_usage.json"):
    try:
        print("[🔁] Querying real RI usage from Azure API...")
        credential = AzureCliCredential()
        client = ConsumptionManagementClient(credential, subscription_id)

        start_date = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = datetime.utcnow().strftime('%Y-%m-%d')

        usage = client.reservation_usage_details.list(
            scope=f"/subscriptions/{subscription_id}",
            start_date=start_date,
            end_date=end_date
        )

        records = []
        for item in usage:
            records.append({
                "instance_id": getattr(item, "instance_id", "unknown"),
                "sku_name": getattr(item, "sku_name", "unknown"),
                "quantity": getattr(item, "quantity", 0),
                "reserved_quantity": 100  # 模拟为 100；未来可调用 Reservation Order API 获取真实值
            })
        
        if not records:
            print("[⚠️] No real RI usage records found. Falling back to mock data.")
            return get_mock_ri_usage(fallback_file)

        return records

    except HttpResponseError as e:
        print(f"[❌] Azure API access error: {e.message}")
        return get_mock_ri_usage(fallback_file)

    except Exception as e:
        print(f"[❌] Unknown error: {str(e)}")
        return get_mock_ri_usage(fallback_file)
