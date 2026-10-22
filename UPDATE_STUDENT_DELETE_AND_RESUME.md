# Update: o‘quvchilarni ommaviy o‘chirish va test davom ettirish

Qilingan o‘zgarishlar:

- Admin paneldagi **Yaratilgan o‘quvchilar** sahifasiga checkbox qo‘shildi.
- Admin o‘quvchilarni bittalab yoki ko‘rinib turganlarini umumiy belgilab o‘chira oladi.
- Backendga `POST /api/students/bulk-delete/` endpoint qo‘shildi.
- Test jarayonidagi progress serverda saqlanadi:
  - tanlangan javoblar;
  - qolgan vaqt;
  - mental arifmetika current index/javoblari.
- O‘quvchi testdan chiqib ketib, keyin code bilan qayta kirsa, tanlagan javoblari va qolgan vaqti tiklanadi.
- Oddiy testlar 30 minut, mental arifmetika 5 minut va har misol 3 sekundligicha qoldi.

Deploy qilish:

```powershell
cd C:\Users\User\Desktop\olimpiadasamarkand_push
git add .
git commit -m "add bulk student delete and server resume progress"
git push origin main
```

Railway migration avtomatik ishlaydi: `python manage.py migrate --noinput`.
