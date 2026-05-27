# 🤖 Job Search Telegram Bot

آگهی‌های شغلی از Google for Jobs (LinkedIn, Indeed, و غیره) رو هر روز صبح به تلگرامت میفرسته.

---

## ⚙️ راه‌اندازی

### ۱. ریپو بساز
یه ریپوی جدید **Private** در GitHub بساز و این فایل‌ها رو آپلود کن.

### ۲. Secrets رو اضافه کن
برو به `Settings > Secrets and variables > Actions > New repository secret` و این ۳ تا رو اضافه کن:

| نام Secret         | مقدار                          |
|--------------------|-------------------------------|
| `RAPIDAPI_KEY`     | کلید RapidAPI ات               |
| `TELEGRAM_BOT_TOKEN` | توکن ربات تلگرام             |
| `TELEGRAM_CHAT_ID` | آیدی عددی تلگرام تو           |

### ۳. تست دستی
برو به تب `Actions` در گیت‌هاب ← workflow رو انتخاب کن ← دکمه `Run workflow` رو بزن.

---

## 🔧 شخصی‌سازی

در فایل `bot.py` این قسمت رو ویرایش کن:

```python
SEARCH_QUERIES = [
    "SEO specialist remote",
    "digital marketing remote",
    # هر چیزی که میخوای اینجا اضافه کن
]
```

همچنین میتونی `date_posted` رو از `today` به `3days` یا `week` تغییر بدی.

---

## ⏰ زمانبندی

بات هر روز **ساعت ۷ صبح به وقت ایران** اجرا میشه.
برای تغییر، فایل `.github/workflows/run.yml` رو ویرایش کن.

---

## 📊 محدودیت پلن رایگان

- **۲۰۰ ریکوئست در ماه**
- هر query = ۱ ریکوئست
- با ۲ query در روز → ~۶۰ ریکوئست در ماه ✅
