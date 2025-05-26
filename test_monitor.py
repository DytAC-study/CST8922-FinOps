from monitor_ri import check_underutilization

def test_utilization_check():
    sample = [{"instance_id": "ri-1", "sku_name": "test", "quantity": 10, "reserved_quantity": 100}]
    alerts = check_underutilization(sample, threshold=0.8)
    assert len(alerts) == 1