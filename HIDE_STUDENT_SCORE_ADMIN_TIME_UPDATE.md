# Student score hidden + admin completion time

Qilingan o‘zgarishlar:

- O‘quvchi testni yakunlagandan keyin natija soni ko‘rinmaydi.
- Yakuniy modalda faqat: `Test yakunlandi` va `Javoblaringiz adminga yuborildi.` chiqadi.
- Natija code orqali ko‘rilsa ham o‘quvchiga nechta to‘g‘ri va foiz ko‘rsatilmaydi.
- Admin paneldagi `Natijalar`, `Dashboard` va `Yaratilgan o‘quvchilar` sahifalarida sarflagan vaqt ko‘rinadi.
- Test yakunlanganda frontend qolgan vaqtni backendga yuboradi, admin vaqti real ishlangan vaqt bo‘yicha hisoblanadi.
- O‘quvchi testdan chiqib ketib qayta code bilan kirsa, tanlangan javoblari va qolgan vaqti serverdan tiklanadi.

Deploy:

```powershell
cd C:\Users\User\Desktop\olimpiadasamarkand_push
git add .
git commit -m "hide student score and show admin completion time"
git push origin main
```
