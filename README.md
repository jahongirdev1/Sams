# Samruks

## Как обновлять переводы

1. Убедитесь, что у вас установлены инструменты gettext (команды `django-admin makemessages` и `django-admin compilemessages` должны быть доступны).
2. Обновите `.po`-файлы после изменения текстов в шаблонах или Python-коде:
   ```bash
   DJANGO_SETTINGS_MODULE=Samruks.settings django-admin makemessages -l ru -l en
   ```
3. Переведите новые строки в `locale/en/LC_MESSAGES/django.po` (и в других локалях при необходимости).
4. Скомпилируйте сообщения для генерации `.mo`-файлов:
   ```bash
   DJANGO_SETTINGS_MODULE=Samruks.settings django-admin compilemessages
   ```
5. Добавьте обновленные `.po` и `.mo` файлы в коммит.