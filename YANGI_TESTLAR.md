# Antalya Olimpiadasi: yangi testlar (2026-10-22)

Barcha eski testlar (English, Rus tili, Koreys tili, eski Matematika va IT) o‘chirildi. Endi platformada faqat "Umumiy testlar" arxividagi testlar bor.

| Fan | Darajalar | Savollar | Vaqt |
| --- | --- | --- | --- |
| Matematika | Kids, 1-sinf … 8-sinf, 10-sinf, 11-sinf (9-sinf arxivda yo‘q) | har birida 20 ta (Kids: 15 ta) | 30 daqiqa |
| IT | HTML CSS, JavaScript, React, Vue, Python | 20 ta | 30 daqiqa |
| Kompyuter | Excel, Word Excel PowerPoint | 20 ta | 30 daqiqa |

- Matematika savollari uch tilda: o‘zbek, rus va ingliz. 1-sinf savollarida rasm bor (`math1-*.jpg`).
- IT va Kompyuter fayllarida 30 tadan savol bor edi, har biridan birinchi 20 tasi olindi.
- Migratsiya `0025_antalya_tests` eski savollarni o‘chiradi, bo‘sh qolgan eski daraja va fanlarni tozalaydi. O‘quvchisi bor daraja va fanlarga tegilmaydi.
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

## Dizayn: Antalya Olimpiadasi

- Platforma nomi hamma joyda "Antalya Olimpiadasi" (sahifa sarlavhasi, o‘quvchi va admin kirish sahifalari, admin panel).
- `frontend/src/assets/xorazm.css` — O‘rta dengiz ranglari (dengiz ko‘ki, firuza, quyosh oltini, qum, terrakota), animatsiyalar.
- `frontend/src/components/AntalyaScene.vue` — three.js 3D sahna: Yivli Minare (qizil g‘isht, yivli tana, firuza belbog‘lar), Hıdırlık minorasi, Hadrian darvozasi (Üç Kapılar), to‘lqinlanuvchi dengiz, palmalar, aylanuvchi oltin yulduzlar. Faqat o‘quvchi va admin kirish sahifalarida yuklanadi.
- `frontend/src/components/AntalyaBackdrop.vue` — barcha sahifalar uchun yengil fon: naqsh, Toros tog‘lari va Antalya silueti (minoralar, darvoza, palmalar, dengiz), 3D kublar, yulduzchalar.
- `v-tilt` direktivasi — kartalarni sichqoncha tomonga 3D egadi (faqat kompyuterda).
- Admin panelda "Antalya kechasi" va "Kunduz" rejimlari.
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
- Kunduz rejimida sof oq o'rniga iliq qum ranglari ishlatildi (inputlar va jadval qatorlari). "Antalya kechasi" tugmasi endi aniq ko'rinadi.

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

## Code yaratish (o'z code'ingiz bilan o'quvchi qo'shish)

Admin paneldagi **Code yaratish** bo'limiga Excel yuklanadi. Har bir o'quvchi Excel'da yozilgan 6 xonali code bilan yaratiladi va shu code bilan kirganda Excel'dagi fan va darajadan test ishlaydi.

- Ustunlar: `Ism familiya`, `Fan`, `Daraja`, `O'quv markaz`, `Code` (`Filial` ixtiyoriy). "Excel namunasini yuklab olish" tugmasi tayyor shablon va testi bor fan/darajalar ro'yxatini beradi.
- Code 6 xonali son bo'lishi va takrorlanmasligi kerak. Excel boshidagi 0 ni tushirib yuborsa (012345 → 12345), u qayta tiklanadi.
- Xato qatorlar (band code, takroriy code, testi yo'q fan/daraja, noto'g'ri code) yaratilmaydi va sababi bilan ko'rsatiladi. "MATEM" / "7" kabi yozuvlar "Matematika" / "7-sinf" ga moslanadi.
- **O'quvchi yaratish** formasida ham code'ni qo'lda yozish yoki "Random" bilan berish mumkin. Bo'sh qolsa, avvalgidek avtomatik beriladi.
- API: `POST /api/students/import-codes/` (Excel), `GET /api/students/code-template/` (namuna).

## Antalya: umumiy tekshiruv (2026-10-22)

Brauzerda to'liq sinaldi: code bilan kirish → savollar → sahifani yangilash → yakunlash → code qayta kiritilganda "oldin ishlatilgan"; vaqt tugaganda avtomatik yakunlash; admin panelning barcha sahifalari (kompyuter va telefon).

Tuzatilganlar:
- **Sahifa yangilanganda vaqt qayta boshlanardi** (har F5 da o'quvchiga qo'shimcha vaqt). Endi qolgan vaqt brauzerda saqlangandan olinadi.
- **Test sahifasi yangi oynada ochilsa bo'sh ekran chiqardi.** Endi code kiritish sahifasiga qaytaradi.
- **O'quvchi kompyuterida admin eski tokeni qolgan bo'lsa**, test so'rovlari xato berib, o'quvchini admin login sahifasiga otib yuborishi mumkin edi. Imtihon so'rovlari endi admin tokenini ishlatmaydi.
- **Code'larni terib topishdan himoya**: bitta IP'dan 10 daqiqada 60 tadan ko'p noto'g'ri code kiritilsa, vaqtincha to'xtatiladi.
- **Progress saqlash** bitta UPDATE so'roviga o'tkazildi: 600 o'quvchi bir vaqtda ishlaganda o'rtacha 0.84 s → 0.05 s.
- **Yakunlash** javob kalitini keshdan oladi va bazaga kamroq so'rov yuboradi.
- Gunicorn jarayonlari kamroq qayta ishga tushadi (`max_requests` 10000): yuklama paytida ulanishlar kamroq uziladi.
- `start_railway.sh`: `seed_demo` xato bersa ham server ishga tushadi.
- Brauzer yorlig'i uchun belgi (favicon) qo'shildi.

Yuklama testi (4 yadroli kompyuter, PostgreSQL 16, gunicorn 3×8): 600 o'quvchi bir vaqtda boshlaydi, har 1–2 soniyada javob saqlaydi (haqiqiydan ancha og'ir) va hammasi bir soniyada yakunlaydi:

| | p50 | p95 | Server xatolari |
|---|---|---|---|
| Testni boshlash | 0.05 s | 0.45 s | 0 |
| Progress saqlash | 0.05 s | 0.19 s | 0 |
| Yakunlash (600 ta bir vaqtda) | 2.8 s | 5.3 s | 0 |

## Ingliz tili testlari (2026-10-24)

"English Language Assessment tests" faylidan English fani qo‘shildi: Kids, Beginner, Elementary, Intermediate, Advanced darajalariga 20 tadan savol (Grammar bo‘limi), har biriga 30 daqiqa. Faylda javob kaliti yo‘q edi, javoblar tekshirib belgilandi va to‘g‘ri javob A/B/C/D bo‘yicha teng taqsimlandi. Excel'da fan "English" yoki "Ingliz tili" deb yozilishi mumkin. Deploydan keyin `seed_demo` bo‘sh English darajalarini avtomatik to‘ldiradi.

## Matematika 9-sinf (2026-10-24)

Arxivda 9-sinf testlari yo‘q edi, shuning uchun 20 ta savol alohida tuzildi (uch tilda: Uzb/Rus/Eng), 30 daqiqa. Endi Matematika Kids va 1–11-sinf darajalarining hammasida test bor. Jami savollar: 475.

## Umumiy tekshiruv (2026-10-24)

- 80 ta WAMAS o‘quvchisi code bilan kirib, testni topshirib chiqdi; code ikkinchi marta ishlamaydi, natijalar admin panelda ko‘rinadi.
- Natija o‘quvchiga ko‘rsatilmaydi (faqat admin): `/api/exam/result/` javobidan ball va foiz ham olib tashlandi.
- Matematika Kids 13-savol takroriy edi ("4 * 5 = ?"), "3 * 6 = ?" bilan almashtirildi.
- Kids, 10-sinf, JavaScript, React, Word Excel PowerPoint darajalarida to‘g‘ri javoblar A/B/C/D bo‘yicha teng taqsimlandi.
- `0026_rebalance_answer_keys` migratsiyasi jonli bazadagi shu savollarni o‘chirmasdan joyida yangilaydi (natijalar saqlanadi).
