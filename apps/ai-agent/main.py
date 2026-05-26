import os
import json
import requests
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
LOKI_URL = os.environ.get("LOKI_URL", "http://loki-gateway.monitoring.svc.cluster.local")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")

def get_logs_from_loki(namespace, pod, minutes=10):
    end = int(datetime.now().timestamp() * 1e9)
    start = int((datetime.now() - timedelta(minutes=minutes)).timestamp() * 1e9)
    
    query = f'{{namespace="{namespace}", pod="{pod}"}}'
    
    try:
        response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range",
            params={
                "query": query,
                "start": start,
                "end": end,
                "limit": 50
            },
            timeout=10
        )
        
        logs = []
        if response.status_code == 200:
            data = response.json()
            for stream in data.get("data", {}).get("result", []):
                for entry in stream.get("values", []):
                    logs.append(entry[1])
        return "\n".join(logs[-20:])
    except Exception as e:
        return f"Could not fetch logs: {str(e)}"

def analyze_with_groq(alert_name, namespace, pod, logs):
    prompt = f"""You are a Kubernetes DevOps expert. Analyze this alert and provide a concise diagnosis and fix.

Alert: {alert_name}
Namespace: {namespace}
Pod: {pod}

Recent logs:
{logs}

Provide:
1. Root cause (1-2 sentences)
2. Immediate fix (specific kubectl command if applicable)
3. Long-term recommendation (1 sentence)

Be concise and technical."""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        },
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "AI analysis unavailable"

def send_to_slack(alert_name, namespace, pod, analysis):
    if not SLACK_WEBHOOK:
        return
    
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🤖 AI Incident Analysis: {alert_name}"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Namespace:*\n{namespace}"},
                    {"type": "mrkdwn", "text": f"*Pod:*\n{pod}"}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*AI Analysis:*\n{analysis}"}
            }
        ]
    }
    
    requests.post(SLACK_WEBHOOK, json=message, timeout=10)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    
    for alert in data.get("alerts", []):
        alert_name = alert.get("labels", {}).get("alertname", "Unknown")
        namespace = alert.get("labels", {}).get("namespace", "default")
        pod = alert.get("labels", {}).get("pod", "")
        status = alert.get("status", "")
        
        if status != "firing":
            continue
            
        logs = get_logs_from_loki(namespace, pod, minutes=10)
        analysis = analyze_with_groq(alert_name, namespace, pod, logs)
        send_to_slack(alert_name, namespace, pod, analysis)
    
    return jsonify({"status": "ok"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)