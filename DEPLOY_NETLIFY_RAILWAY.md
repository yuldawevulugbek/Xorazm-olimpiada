# Xorazm Olimpiadasi: Railway + PostgreSQL + Netlify'ga joylash

Bu loyihada backend (`backend/`) Railway'da ishlaydi, baza PostgreSQL, frontend (`frontend/`) esa Netlify'da. Hamma sozlamalar tayyor. Faqat quyidagi qadamlarni bajarasiz.

---

## 0. Kodni GitHub'ga yuklash

Zipni oching va papka ichida (unda `.git` bor) quyidagilarni bajaring:

```powershell
git add .
git commit -m "Xorazm olimpiadasi: yangi testlar, dizayn, postgres"
git push origin main
```

`.env`, `db.sqlite3` va `node_modules` fayllari GitHub'ga yuklanmaydi (`.gitignore` ularni chiqarib tashlaydi).

---

## 1. Railway: backend

1. railway.app → **New Project** → **Deploy from GitHub repo** → reponi tanlang.
2. Xizmat sozlamalarida **Root Directory** bo'sh qolsin (repo ildizi). `railway.json`, `nixpacks.toml` va `start_railway.sh` hammasini o'zi qiladi: kutubxonalarni o'rnatadi, migratsiya qiladi, testlarni yuklaydi va gunicorn'ni ishga tushiradi.
3. **Settings → Networking → Generate Domain** tugmasini bosing. Masalan, `xorazm-olimpiada.up.railway.app` degan manzil chiqadi.

## 2. Railway: PostgreSQL

1. Shu loyihaning ichida **+ New → Database → Add PostgreSQL** ni tanlang.
2. Backend xizmati → **Variables** → **Add Variable Reference** → `DATABASE_URL` ni tanlang (`${{Postgres.DATABASE_URL}}`).
3. Shundan keyin har bir deploy ma'lumotlarni saqlab qoladi. SQLite'da esa har deployda hammasi o'chib ketardi.

## 3. Railway Variables (backend → Variables)

| O'zgaruvchi | Qiymat | Izoh |
|---|---|---|
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | 2-qadamda qo'shilgan |
| `SECRET_KEY` | 50+ belgili tasodifiy matn | Majburiy. Masalan: `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `ADMIN_PASSWORD` | o'zingizning parolingiz | `ulugbek` akkauntining paroli. Yozilmasa, eski parol ishlaydi |
| `CORS_ALLOWED_ORIGINS` | `https://SIZNING-SAYT.netlify.app` | Ixtiyoriy: `*.netlify.app` domenlariga ruxsat avtomatik beriladi. O'z domeningiz bo'lsa, shuni yozing |
| `CSRF_TRUSTED_ORIGINS` | yuqoridagi bilan bir xil | Ixtiyoriy |
| `WEB_CONCURRENCY` | `3` | Ixtiyoriy: jarayonlar soni |
| `GUNICORN_THREADS` | `8` | Ixtiyoriy: har bir jarayondagi oqimlar soni |

`DEBUG` ni yozish shart emas: Railway'da u avtomatik o'chiq bo'ladi. Railway har deploydan keyin `/api/health/` manzilini tekshiradi. Server javob bermasa, eski versiya ishlashda davom etadi.

Tekshirish: brauzerda `https://SIZNING-BACKEND.up.railway.app/api/health/` manzilini oching. `{"status": "ok"}` chiqishi kerak.

## 4. Netlify: frontend

1. app.netlify.com → **Add new site → Import an existing project** → GitHub → reponi tanlang.
2. Build sozlamalari ildizdagi `netlify.toml` dan avtomatik olinadi (base `frontend`, `npm run build`, `dist`, Node 22). Hech narsani o'zgartirmang.
3. **Site configuration → Environment variables** bo'limiga quyidagini qo'shing:
   - `VITE_API_BASE_URL` = `https://SIZNING-BACKEND.up.railway.app/api`

   Manzil oxiridagi `/api` esdan chiqsa ham, frontend uni o'zi qo'shadi.
4. **Deploys → Trigger deploy** tugmasini bosing. O'zgaruvchi qo'shilgandan keyin bitta qayta build kerak bo'ladi.

## 5. Kompyuterdagi ma'lumotlarni PostgreSQL'ga ko'chirish (ixtiyoriy, bir marta)

Kompyuterdagi `backend/db.sqlite3` dagi o'quvchilar va natijalarni Railway Postgres'ga o'tkazish uchun:

1. Railway → Postgres → **Connect** → **Public Network** bo'limidan `DATABASE_PUBLIC_URL` ni nusxalang.
2. `backend/sqlite_to_postgres.bat` faylini ikki marta bosing va so'ralganda shu manzilni joylang.
3. Skript Postgres'dagi eski ma'lumotlarni o'chiradi va SQLite'dagilarni yozadi. Shuning uchun uni faqat birinchi marta ishlating.

## 6. Tekshirish ro'yxati

- [ ] `https://...railway.app/api/health/` manzili ok qaytaradi
- [ ] Netlify sayti ochiladi, "Ro'yxatdan o'tish" bosilganda fanlar ro'yxati chiqadi
- [ ] Admin panelga `ulugbek` va `ADMIN_PASSWORD` dagi parol bilan kirsa bo'ladi
- [ ] Bitta sinov o'quvchi bilan test ishlab, natija admin panelda ko'rinadi

## Muammo bo'lsa

| Belgi | Sababi va yechimi |
|---|---|
| Saytda "Network Error" chiqadi, fanlar yuklanmaydi | Netlify'da `VITE_API_BASE_URL` yozilmagan yoki noto'g'ri. Uni tuzatib, qayta deploy qiling |
| Brauzer konsolida CORS xatosi | Netlify'dan boshqa domen ishlatilyapti: Railway'da `CORS_ALLOWED_ORIGINS` ga o'sha domenni yozing |
| Railway'da `Bad Request (400)` | O'z domeningiz bor: `ALLOWED_HOSTS` ga `.railway.app,sizning-domen.uz` ni yozing |
| Har deploydan keyin o'quvchilar yo'qoladi | Postgres ulanmagan: 2-qadamni bajaring. Railway loglarida "DATABASE_URL topilmadi" degan ogohlantirish chiqadi |
