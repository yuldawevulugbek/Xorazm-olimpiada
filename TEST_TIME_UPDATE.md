# Test vaqt sozlamasi

- Oddiy A/B/C/D testlar: 30 minut.
- Mental arifmetika: umumiy 5 minut.
- Mental arifmetikada har bir misol 3 sekund ko‘rsatiladi, javob kiritilayotgan paytda ham umumiy vaqt yuraveradi.
- O‘quvchi testdan chiqib ketib, code bilan qayta kirsa:
  - backend `started_at` bo‘yicha qolgan vaqtni davom ettiradi;
  - browser `localStorage` orqali belgilangan javoblar qayta tiklanadi;
  - test boshidan boshlanmaydi.
