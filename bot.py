import requests
import os
import json
from datetime import datetime

# ─── Config from environment variables (GitHub Secrets) ───────────────────────
RAPIDAPI_KEY     = os.environ["RAPIDAPI_KEY"]
TELEGRAM_TOKEN   = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ─── Job search queries — هر چقدر خواستی اضافه کن ────────────────────────────
SEARCH_QUERIES = [
    "SEO specialist remote",
    "digital marketing remote",
]

# ─── JSearch API ──────────────────────────────────────────────────────────────
def search_jobs(query: str) -> list[dict]:
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key":  RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
    }
    params = {
        "query":        query,
        "num_pages":    "1",
        "date_posted":  "today",          # فقط آگهی‌های امروز
        "work_from_home": "true",         # ریموت
    }
    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "OK":
        print(f"[WARN] API error for '{query}': {data.get('error')}")
        return []

    return data.get("data", [])


# ─── Telegram sender ──────────────────────────────────────────────────────────
def send_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    resp = requests.post(url, json=payload, timeout=10)
    if not resp.ok:
        print(f"[ERROR] Telegram send failed: {resp.text}")


def format_job(job: dict) -> str:
    title    = job.get("job_title", "بدون عنوان")
    company  = job.get("employer_name", "نامشخص")
    city     = job.get("job_city") or ""
    country  = job.get("job_country") or ""
    location = f"{city}, {country}".strip(", ") or "ریموت"
    link     = job.get("job_apply_link") or job.get("job_google_link") or ""
    source   = job.get("job_publisher") or ""
    posted   = job.get("job_posted_at_datetime_utc", "")[:10] if job.get("job_posted_at_datetime_utc") else ""

    lines = [
        f"💼 <b>{title}</b>",
        f"🏢 {company}",
        f"📍 {location}",
    ]
    if source:
        lines.append(f"🌐 {source}")
    if posted:
        lines.append(f"📅 {posted}")
    if link:
        lines.append(f'🔗 <a href="{link}">Apply Now</a>')

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"[INFO] Bot started at {now}")

    all_jobs = []
    seen_ids = set()  # جلوگیری از تکرار

    for query in SEARCH_QUERIES:
        print(f"[INFO] Searching: {query}")
        jobs = search_jobs(query)
        print(f"[INFO] Found {len(jobs)} jobs")

        for job in jobs:
            job_id = job.get("job_id") or job.get("job_apply_link")
            if job_id and job_id not in seen_ids:
                seen_ids.add(job_id)
                all_jobs.append(job)

    if not all_jobs:
        send_telegram(f"🔍 <b>گزارش روزانه</b> — {now}\n\nامروز آگهی جدیدی پیدا نشد.")
        return

    # هدر پیام
    header = f"🔍 <b>آگهی‌های شغلی امروز</b>\n📅 {now}\n➖➖➖➖➖➖➖➖➖➖"
    send_telegram(header)

    # ارسال هر آگهی به صورت جداگانه (ماکزیمم ۱۰ تا)
    for job in all_jobs[:10]:
        send_telegram(format_job(job))

    print(f"[INFO] Sent {min(len(all_jobs), 10)} jobs to Telegram.")


if __name__ == "__main__":
    main()
