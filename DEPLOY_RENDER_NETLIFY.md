# Render (backend) + Netlify (frontend) ga joylash

Testlar `backend/olympiad/tests_data.py` ichida turadi va har deployda `seed_demo` faqat **bo‘sh** darajalarni to‘ldiradi:
mavjud savollar, o‘quvchilar va natijalar o‘chirilmaydi, savollar ikki marta qo‘shilmaydi.
O‘quvchi va natijalar saqlanib qolishi uchun backend albatta **PostgreSQL** bilan ishlashi kerak
(Render serverining diski vaqtinchalik, SQLite har deployda o‘chadi). Shuning uchun PostgreSQL ulanmagan bo‘lsa, backend ishga tushmaydi.

## 1. Kodni GitHub'ga yuklang
Zip ichidagi `Dubai` papkasini GitHub repozitoriyga push qiling (`db.sqlite3` va `.env` .gitignore sabab yuklanmaydi).

## 2. Render: backend + baza
1. render.com → **New → Blueprint** → repozitoriyni tanlang. `render.yaml` o‘zi yaratadi:
   - `antalya-olimpiada-backend` (Python web service, `backend` papkasi)
   - `antalya-olimpiada-db` (PostgreSQL) va uning `DATABASE_URL`i
   - tasodifiy `SECRET_KEY`
2. So‘ralganda yozing:
   - `ADMIN_PASSWORD` — admin (login: `ulugbek`) uchun o‘z parolingiz
   - `CORS_ALLOWED_ORIGINS` — Netlify manzilingiz, masalan `https://antalya-olimpiada.netlify.app` (keyin ham yozish mumkin)
3. Deploy tugagach `https://<nom>.onrender.com/api/health/` ochilsa `{"status": "ok"}` chiqadi.

## 3. Netlify: frontend
1. netlify.com → **Add new site → Import from Git** → shu repozitoriy. `netlify.toml` sozlamalari o‘zi olinadi (base `frontend`, build `npm run build`, publish `dist`).
2. **Site configuration → Environment variables**: `VITE_API_BASE_URL = https://<nom>.onrender.com/api`
3. **Deploys → Trigger deploy** (o‘zgaruvchi yozilgandan keyin qayta build kerak).
4. Netlify manzilini Render'dagi `CORS_ALLOWED_ORIGINS` ga yozing (`*.netlify.app` sukut bo‘yicha ruxsat etilgan).

## Render bepul tarifi haqida
- Bepul server 15 daqiqa so‘rov bo‘lmasa uxlaydi, uyg‘onishi ~1 daqiqa. Sayt ochilganda frontend backendni avtomatik uyg‘otadi,
  lekin olimpiada boshlanishidan 5 daqiqa oldin saytni bir marta ochib qo‘ying.
- **Bepul PostgreSQL 30 kundan keyin o‘chiriladi** (1 GB). Olimpiada uchun bazani pullik tarifga o‘tkazing yoki 30 kun ichida o‘tkazing
  va natijalarni oldindan Excel'ga yuklab oling.
- Ko‘p o‘quvchi bir vaqtda ishlasa, web service uchun ham pullik (Starter) tarif tavsiya etiladi.
