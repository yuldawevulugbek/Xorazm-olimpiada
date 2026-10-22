> **Joylash (Railway + PostgreSQL + Netlify):** [DEPLOY_NETLIFY_RAILWAY.md](DEPLOY_NETLIFY_RAILWAY.md). Yangi testlar va o'zgarishlar: [YANGI_TESTLAR.md](YANGI_TESTLAR.md).

# Al-Aziz Academy

Django + Vue.js asosidagi xalqaro olimpiada platformasi.

## Asosiy imkoniyatlar

- Admin login/parol orqali panelga kiradi.
- Super admin boshqa adminlarni yaratadi.
- Admin o‘quvchi yaratadi: ism, familya, fan, daraja, o‘quv markaz.
- Har bir o‘quvchiga avtomatik 6 xonali random status code beriladi.
- O‘quvchilar Excel orqali import qilinadi.
- O‘quvchi faqat status code bilan testga kiradi.
- Code faqat bir marta ishlaydi.
- Admin panelda statuslar rang bilan ko‘rinadi:
  - qizil: ishlamagan
  - sariq: ishlayapti
  - yashil: ishlab bo‘ldi
- Test vaqti fan/daraja bo‘yicha belgilanadi.
- O‘quvchi testni yakunlaganda natija avtomatik hisoblanadi.
- Natijalar Excel formatda yuklab olinadi.

## Project strukturasi

```text
al_aziz_academy/
├── backend/
└── frontend/
```

---

# Backend ishga tushirish

```bash
cd backend
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Kutubxonalarni o‘rnatish:

```bash
pip install -r requirements.txt
```

Migratsiya:

```bash
python manage.py migrate
```

Demo admin, fanlar, darajalar, o‘quv markaz va testlarni yaratish:

```bash
python manage.py seed_demo
```

Serverni ishga tushirish:

```bash
python manage.py runserver
```

Demo admin:

```text
Username: admin
Password: admin12345
```

Backend URL:

```text
http://127.0.0.1:8000/api/
```

---

# Frontend ishga tushirish

```bash
cd frontend
npm install
npm run dev
```

Frontend URL odatda:

```text
http://localhost:5173
```

Admin login:

```text
/admin/login
```

O‘quvchi code bilan kirish sahifasi:

```text
/student
```

---

# Excel import formati

Excel faylda birinchi qatorda header bo‘lishi kerak:

| Ism | Familya | Fan | Daraja | O'quv markaz |
|---|---|---|---|---|
| Ali | Valiyev | English | Beginner | Al-Aziz Academy |
| Madina | Karimova | Mathematics | Junior | Smart School |

Header nomlarini aynan shunday yozish tavsiya qilinadi:

```text
Ism
Familya
Fan
Daraja
O'quv markaz
```

---

# API qisqa ro‘yxat

```text
POST /api/auth/login/
POST /api/auth/refresh/
GET  /api/accounts/admins/
POST /api/accounts/admins/

GET/POST /api/centers/
GET/POST /api/subjects/
GET/POST /api/levels/
GET/POST /api/questions/
GET/POST /api/students/
POST     /api/students/import-excel/

POST /api/exam/start/
POST /api/exam/submit/

GET /api/results/
GET /api/results/export-excel/
```

---

# Muhim eslatma

Bu loyiha MVP holatda tayyorlangan. Production uchun quyidagilarni qo‘shish kerak:

- kuchli SECRET_KEY
- DEBUG=False
- PostgreSQL
- Railway/Render backend deploy
- Netlify frontend deploy
- HTTPS domain
- admin permissionlarni yanada kuchaytirish

---

# Mental arifmetika rejimi

`seed_demo` komandasi avtomatik `Mental arifmetika` fanini va `Junior` darajasini yaratadi.

Agar o‘quvchi fani nomida `Mental` so‘zi bo‘lsa, platforma oddiy test savollarini chiqarmaydi. Buning o‘rniga:

1. Ekranda `3`, `2`, `1` countdown chiqadi.
2. 5 ta mental misol ketma-ket chiqadi.
3. Har bir misolda sonlar alohida-alohida ko‘rinadi, masalan: `12`, `+2`, `-4`, `+1`.
4. Keyin modal oyna ochilib, o‘quvchi javob kiritadi.
5. 5 ta misol tugagach natija adminga tushadi.

Admin `Natijalar` sahifasida mental misollarni ham ko‘radi:

```text
12 +2 -4 +1 = 11 / to‘g‘ri: 11
```

Excel export ichida ham `Mental javoblar` ustuni bor.

---


# Testlarni kiritish

Testlarni Word orqali yuklash joyi olib tashlandi. Testlarni foydalanuvchi yuboradi, keyin savollar loyiha ichiga fan va daraja bo‘yicha tayyor qilib kiritiladi. Admin paneldagi Testlar sahifasida zarurat bo‘lsa bitta-bitta savol qo‘shish formasi qoldirildi.


## Deploy

Netlify + Railway uchun toʻliq yoʻriqnoma: `DEPLOY_NETLIFY_RAILWAY.md`.
