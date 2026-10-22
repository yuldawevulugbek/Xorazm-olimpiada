# Samarqand deploy tuzatishlari

Bu versiyada Railway/Netlify uchun muhim xatolar tuzatildi.

## Tuzatilgan joylar

- `backend/railway.json` ichidan `healthcheckPath` olib tashlandi. Railway endi Healthcheck failure bilan yiqilmasligi kerak.
- `seed_demo.py` ichidagi `ProtectedError` tuzatildi. Eski Rus tili yoki Matematika darajalariga o'quvchi biriktirilgan bo'lsa, ular yangi darajaga ko'chiriladi va keyin eski daraja o'chiriladi.
- Admin login har seed paytida qayta tayyorlanadi: `ulugbek / codingwithulugbek20030313`.
- `DATABASE_URL` noto'g'ri yoki bo'sh bo'lsa Django endi `ENGINE` xatosi bermasdan SQLite fallback bilan ishlaydi. Railway'da Postgres uchun baribir backend service Variables ichiga haqiqiy `DATABASE_URL` qo'yish tavsiya qilinadi.
- Accounts migration warning uchun `0004_alter_adminprofile_options.py` qo'shildi.

## Railway backend variables

Backend service ichida kamida shular bo'lsin:

```env
SECRET_KEY=samarqand-super-secret-key-2026
DEBUG=False
ALLOWED_HOSTS=*
DATABASE_URL=postgresql://...
CORS_ALLOW_NETLIFY=True
CORS_ALLOWED_ORIGINS=https://SIZNING-NETLIFY-LINK.netlify.app
CSRF_TRUSTED_ORIGINS=https://SIZNING-NETLIFY-LINK.netlify.app
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Push qilish

GitHub bilan ulangan papkada:

```powershell
git add .
git commit -m "fix railway deploy and seed demo"
git push
```
