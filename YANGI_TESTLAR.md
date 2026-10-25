# Yangi testlar (2026-10-22)

Eski testlar (English, Matematika 0–3-sinf, Arab tili, Rus tili) to‘liq o‘chirildi va o‘rniga yangilari qo‘yildi.

| Fan | Darajalar | Savollar | Vaqt |
| --- | --- | --- | --- |
| Matematika | 1-sinf … 11-sinf | har birida 20 ta | 30 daqiqa |
| English | Starter, Beginner (30 ta, rasmli), Elementary, Intermediate, Advanced | 20 ta | 30 daqiqa |
| Rus tili | A1, A2, B1 (B1 da 3 ta variant) | 20 ta | 30 daqiqa |
| IT Frontend | HTML CSS, JavaScript, Vue | 20 ta | 30 daqiqa |
| IT Backend | Python | 20 ta | 30 daqiqa |

- Testlar: `backend/olympiad/tests_data.py`. `seed_demo` faqat savoli yo‘q darajalarni to‘ldiradi, mavjud savollarga tegmaydi.
- Rasmlar: `frontend/public/test-images/`. Savolda `image_url` maydoni bor.
- 3 variantli savollar uchun `option_d` bo‘sh qoladi, sahifada faqat A/B/C chiqadi.
- 20 tagacha savolli testda bitta bosqich bo‘ladi, 20 tadan ko‘p bo‘lsa 20 + qolgani.
- Migratsiyalar: `0019` eski savollarni o‘chiradi, `0020` rasm maydonini qo‘shadi, `0021` eski bo‘sh darajalarni tozalaydi.
- Excel import "INGLIZ TILI", "MATEM", "RUS TILI", "3-SINF" kabi nomlarni avtomatik "English", "Matematika", "3-sinf" ga moslaydi.
  `seed_demo` testni hali boshlamagan shunday o‘quvchilarni ham mos testli darajaga o‘tkazadi.

Ishga tushirish:

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
```

## Dizayn: Xorazm Olimpiadasi

- `frontend/src/assets/xorazm.css` — Xiva majolikasi ranglari (lojuvard, firuza, oltin, qum), animatsiyalar.
- `frontend/src/components/XorazmScene.vue` — three.js 3D sahna: Kalta Minor, Islom Xo‘ja minorasi, moviy gumbaz, aylanuvchi oltin yulduzlar. Faqat o‘quvchi va admin kirish sahifalarida yuklanadi.
- `frontend/src/components/XorazmBackdrop.vue` — barcha sahifalar uchun yengil fon: naqsh, Xiva silueti, 3D kublar, yulduzchalar. Imtihon va admin sahifalarida tinchroq.
- `v-tilt` direktivasi — kartalarni sichqoncha tomonga 3D egadi (faqat kompyuterda).
- Admin panelda "Xiva kechasi" va "Kunduz" rejimlari.
- Telefonda va "kamroq harakat" sozlamasi yoqilgan qurilmalarda animatsiyalar yengillashadi.

## Ko'p o'quvchi bir vaqtda ishlaganda qotmaslik

Nima o'zgardi:
- **Server** (`backend/gunicorn.conf.py`): avval bitta jarayon so'rovlarni navbat bilan bajarardi. Endi 3 jarayon × 8 oqim bor, ya'ni 24 ta so'rov parallel bajariladi. Railway Variables orqali sozlanadi: `WEB_CONCURRENCY` (jarayonlar soni) va `GUNICORN_THREADS` (har bir jarayondagi oqimlar soni). Osilib qolgan so'rov 60 soniyada uziladi.
- **Savollar keshi**: imtihon savollari 60 soniya xotirada saqlanadi. Admin savolni o'zgartirsa, kesh darhol tozalanadi.
- **Kamroq so'rov**: test sahifasi avval har 3 soniyada serverga progress yuborardi. Endi bu har 15 soniyada bo'ladi, javob tanlanganda esa darhol yuboriladi. Natijada server yuklamasi taxminan 5 baravar kamaydi.
- **Yengil yakunlash**: `exam/submit` endi qisqa javob qaytaradi, to'g'ri javoblarni ham qaytarmaydi. Mental javoblar bitta so'rov bilan saqlanadi.
- **Qayta yuborish**: yakunlash so'rovi xato bersa, 5 martagacha qayta yuboriladi, shuning uchun javoblar yo'qolmaydi. Har bir so'rov uchun 25 soniya kutish chegarasi bor (Excel import va eksportda chegara yo'q).
- **Admin ro'yxati**: o'quvchilar ro'yxati natijalar bilan bitta so'rovda olinadi.
- **Baza**: PostgreSQL ulanishi har safar tekshiriladi. SQLite uchun WAL rejimi va kutish vaqti yoqilgan.

Yuklama testi (4 yadroli kompyuter, PostgreSQL). Har bir o'quvchi testni boshlaydi, javob beradi va oxirida hammasi birga yakunlaydi:

| | Oldin, 600 o'quvchi | Keyin, 600 o'quvchi | Keyin, 1200 o'quvchi |
|---|---|---|---|
| Testni boshlash (p95) | 1.8 s | 0.03 s | 0.09 s |
| Progress saqlash (p50) | 1.5 s | 0.01 s | 0.01 s |
| Yakunlash (p95) | 19.8 s | 0.05 s | 0.6 s |
| Xatolar | 0 | 0 | 0 |

Olimpiada kuni uchun tavsiyalar:
1. Railway'da **PostgreSQL** ulang. Postgres qo'shilganda `DATABASE_URL` o'zgaruvchisi avtomatik paydo bo'ladi. SQLite Railway'da qayta deploy qilinganda o'chib ketadi.
2. Railway xizmatiga kamida 1 GB RAM bering. 3 jarayon taxminan 300 MB ishlatadi.
3. Olimpiada paytida qayta deploy qilmang.

## Takroriy fanlar birlashtirildi

Excel'dan import qilinganda bir xil fan ikki xil nom bilan yozilib qolgan edi. Endi har bir fan bittadan:
- INGLIZ TILI → English
- MATEM → Matematika
- Mental, MENTAL → Mental arifmetika
- RUS TILI → Rus tili
- ARAB TILI → Arab tili

O'quvchilar, natijalar va savollar o'chmaydi, faqat to'g'ri fanga ko'chiriladi. "3-SINF" va "3-sinf" kabi bir xil darajalar ham bittaga birlashtiriladi. Bu ish server har ishga tushganda avtomatik bajariladi (`seed_demo` → `merge_duplicate_subjects`). Admin panelda mavjud fanning boshqacha yozilgan nusxasini endi qo'shib bo'lmaydi.

## Oq fonlar almashtirildi ("Tungi shisha" uslubi)

Kechki rejim (standart) va o'quvchi sahifalarida endi oq fonli element qolmadi:
- Inputlar, selectlar va textarealar to'q shaffof rangda. Select o'qi oltin rangda, ochiladigan ro'yxat ham to'q.
- O'quvchi va admin kirish oynalari, savol kartalari, variantlar va Excel yuklash qutisi to'q shisha uslubida, turkuaz va oltin nur bilan bezatilgan.
- Checkboxlar va fayl tanlash tugmasi mavzuga moslandi.
- Tugmalardagi yaltirash yumshatildi, shuning uchun matn aniq o'qiladi.
- Kunduz rejimida sof oq o'rniga iliq qum ranglari ishlatildi (inputlar va jadval qatorlari). "Xiva kechasi" tugmasi endi aniq ko'rinadi.

Barcha o'zgarishlar `frontend/src/assets/xorazm.css` oxiridagi "Tungi shisha" bo'limida joylashgan.

## O'quvchining o'zi ro'yxatdan o'tishi

O'quvchi kirish sahifasida "Testni boshlash" tugmasining tagida **Ro'yxatdan o'tish** tugmasi bor. O'quvchi uni bosganda quyidagilarni kiritadi:
- ism va familiya;
- o'quv markaz (mavjud markazlar taklif qilinadi, yangi nom ham yozish mumkin);
- yosh;
- fan va daraja (ro'yxatda faqat testi bor fan va darajalar chiqadi).

Enter yoki "Testga kirish" bosilganda o'quvchi yaratiladi va test darhol boshlanadi. Test sahifasining tepasida o'quvchining shaxsiy code'i ko'rinadi: sahifa yopilib qolsa, shu code bilan qayta kiradi. Admin paneldagi o'quvchilar ro'yxatida bunday o'quvchilar "o'zi ro'yxatdan o'tgan" belgisi bilan chiqadi. Ro'yxatda "Yosh" ustuni ham bor (Excel eksportida ham).

Texnik tafsilotlar: API manzillari `GET /api/exam/catalog/` va `POST /api/exam/register/` (bitta IP'dan daqiqasiga 60 tagacha ro'yxatdan o'tish mumkin). Bazaga migratsiya `0023` bilan `age` va `is_self_registered` maydonlari qo'shildi.

## Umumiy tekshiruv va telefon uchun tuzatishlar

Sayt to'rtta ekran o'lchamida tekshirildi: kompyuter (1366), planshet (768), telefon (390) va kichik telefon (360). Tuzatilganlar:
- Ro'yxatdan o'tgach yoki code bilan kirgach test har doim tepadan, 1-savoldan ochiladi. Har bir yangi sahifa ham tepadan ochiladi.
- Telefonda test sarlavhasi ixcham: ism, fan va code chapda, taymer o'ngda. Savollar uchun ko'proq joy qoladi.
- "Testni yakunlash" tugmasi endi darhol yubormaydi: oldin tasdiqlash oynasi chiqadi va unda javob berilmagan savollar soni ko'rsatiladi.
- 2-bosqich, test yakunlandi va natija oynalari, mental arifmetika sahifasi oq fonda edi. Endi ular tungi shisha uslubida.
- Admin paneldagi yuqori panel telefonda ekranning yarmini egallardi. Endi menyu tugmasi va nom bitta qatorda turadi, tugmalar esa ixcham qatorga joylashgan.
- Telefonda yopiq menyuning cheti ekranda chiziq bo'lib ko'rinib turardi, bu tuzatildi. Menyu ochilganda orqa fon qorayadi, bo'sh joyga bossangiz menyu yopiladi.
