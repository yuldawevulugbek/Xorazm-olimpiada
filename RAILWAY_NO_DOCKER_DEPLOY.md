# Railway deploy — Dockersiz / Nixpacks

Bu zip Docker ishlatmaydi. Dockerfile olib tashlangan.

## Railway sozlama

Tavsiya qilingan eng oson sozlama:

```text
Root Directory: bo‘sh qolsin
Builder: Nixpacks
Start Command: bo‘sh qolsin
```

Repo rootida `nixpacks.toml` va `railway.json` bor. Railway o‘zi shuni oladi.

Agar Root Directory = `backend` qilsangiz ham ishlaydi, chunki `backend/nixpacks.toml` ham bor.

## Variables

```env
SECRET_KEY=ulugbek-super-secret-key-2003
DEBUG=False
ALLOWED_HOSTS=internationalolympiad-production.up.railway.app,.railway.app,.up.railway.app
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
```

PostgreSQL ishlatmoqchi bo‘lsangiz:
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Agar Postgres nomi PostgreSQL bo‘lsa:
```env
DATABASE_URL=${{PostgreSQL.DATABASE_URL}}
```

Backend tekshirish:
```text
https://YOUR-RAILWAY-URL.up.railway.app/api/health/
```

## Netlify frontend

```text
Base directory: frontend
Build command: npm run build
Publish directory: dist
```

Netlify environment variable:
```env
VITE_API_BASE_URL=https://YOUR-RAILWAY-URL.up.railway.app/api
```

Netlify URL chiqqandan keyin Railway CORS ga Netlify URL ni yozing:
```env
CORS_ALLOWED_ORIGINS=https://YOUR-NETLIFY-SITE.netlify.app
CSRF_TRUSTED_ORIGINS=https://YOUR-NETLIFY-SITE.netlify.app
```
