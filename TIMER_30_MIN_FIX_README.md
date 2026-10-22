# 30 minut timer fix

Tuzatildi:

- Admin yangi o‘quvchi yaratganda status majburan `not_started` bo‘ladi.
- Yangi o‘quvchi code bilan birinchi marta kirganda oddiy testlar 30:00 dan boshlaydi.
- Mental arifmetika 5:00 dan boshlaydi va har bir mental misol 3 sekund ko‘rsatiladi.
- Agar o‘quvchi testni boshlab chiqib ketsa, qayta code bilan kirganda `resume=true` bo‘ladi va avvalgi vaqt davom etadi.
- Backend `resume=false` yuborgan yangi startlarda frontend eski sana/clock farqi sabab 00:00 qilib yubormaydi.

GitHub push qilish:

```powershell
cd C:\Users\User\Desktop\olimpiadasamarkand_push
robocopy C:\Users\User\Desktop\Samarqand C:\Users\User\Desktop\olimpiadasamarkand_push /E /XD .git node_modules venv .venv __pycache__ dist
git add .
git commit -m "fix student timer starts at 30 minutes"
git push origin main
```
