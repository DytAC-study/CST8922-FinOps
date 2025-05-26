# RI Alerts Demo (CST8922 FinOps Project)

This project demonstrates an automated cost governance alert system for Reserved Instance (RI) underutilization in Microsoft Azure.

## Features

- Reads RI usage data via Azure Consumption API (or mock fallback)
- Identifies underutilized RIs (default threshold: 80%)
- Generates HTML report
- Saves CSV alert logs for audit
- Fully runnable in WSL or Ubuntu with Python venv

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Edit `monitor_ri.py` and replace your subscription ID:

```python
subscription_id = "your-subscription-id"
```

Then run:

```bash
python monitor_ri.py
```

## Output

- HTML report in `/alerts/`
- CSV report in `/alerts/`

## Optional Features

- Replace mock data with real Azure RI API
- Add Gmail or SendGrid integration
- Schedule via crontab

## Authors

Team CST8922 - Azure FinOps Automation