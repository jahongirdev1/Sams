from __future__ import annotations

import re

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from ckeditor.fields import RichTextField


# --- Главная: карусель ---
class CarouselItem(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Заголовок"), max_length=150, blank=True),
        subtitle=models.CharField(_("Подзаголовок"), max_length=250, blank=True),
    )
    image = models.ImageField(_("Изображение"), upload_to="carousel/")
    link_url = models.URLField(_("Ссылка"), blank=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Слайд")
        verbose_name_plural = _("Слайды")
        ordering = ["ordering", "-id"]

    def __str__(self) -> str:
        return self.safe_translation_getter("title", any_language=True) or f"Carousel #{self.pk}"


class SectionHeader(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Заголовок"), max_length=200),
        description=models.TextField(_("Описание"), blank=True),
    )
    photo = models.ImageField(
        _("Фото"),
        upload_to="section_headers/",
        blank=True,
        null=True,
        help_text=_("Фон для блока, можно не добавлять"),
    )
    slug = models.SlugField(
        _("Слаг"),
        unique=True,
        help_text=_("Ключ страницы: catalog, about, contact и т.д."),
    )
    is_active = models.BooleanField(_("Активен"), default=True)

    class Meta:
        verbose_name = _("Заголовок секции")
        verbose_name_plural = _("Заголовки секций")

    def __str__(self) -> str:
        return self.safe_translation_getter("title", any_language=True) or self.slug


# --- Каталог ---
class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название"), max_length=120),
        description=models.TextField(_("Описание"), blank=True),
    )
    slug = models.SlugField(_("Слаг"), unique=True, db_index=True, max_length=140)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            name_value = self.safe_translation_getter("name", any_language=True) or ""
            base = slugify(name_value) or "category"
            slug = base
            n = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.safe_translation_getter("name", any_language=True) or f"Category {self.pk}"


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название"), max_length=180),
        description=RichTextField(_("Описание"), blank=True),
    )
    slug = models.SlugField(_("Слаг"), unique=True, db_index=True, max_length=200)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)
    is_main = models.BooleanField(_("Показывать на главной"), default=False, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Категория"),
    )
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["category"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            name_value = self.safe_translation_getter("name", any_language=True) or ""
            base = slugify(name_value) or "product"
            slug = base
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.safe_translation_getter("name", any_language=True) or f"Product {self.pk}"


class ProductImage(TranslatableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Товар"),
    )
    translations = TranslatedFields(
        alt_text=models.CharField(_("Альтернативный текст"), max_length=150, blank=True),
    )
    image = models.ImageField(_("Изображение"), upload_to="products/")
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_primary = models.BooleanField(_("Основное"), default=False)

    class Meta:
        verbose_name = _("Изображение товара")
        verbose_name_plural = _("Изображения товара")
        ordering = ["ordering", "id"]
        indexes = [models.Index(fields=["product", "ordering"])]

    def clean(self):
        if self.is_primary:
            qs = ProductImage.objects.filter(product=self.product, is_primary=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    _("У продукта может быть только одно основное изображение (is_primary=True).")
                )

    def __str__(self) -> str:
        name = self.product.safe_translation_getter("name", any_language=True)
        return f"{name or self.product_id} image #{self.pk}"


# --- О нас ---
class Advantage(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Заголовок"), max_length=150),
        description=models.TextField(_("Описание")),
    )
    icon = models.ImageField(_("Иконка"), upload_to="about/icons/", blank=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активно"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Преимущество")
        verbose_name_plural = _("Преимущества")
        ordering = ["ordering", "id"]

    def __str__(self) -> str:
        return self.safe_translation_getter("title", any_language=True) or f"Advantage {self.pk}"


class Metric(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название"), max_length=120),
        value=models.CharField(_("Значение"), max_length=60),
        suffix=models.CharField(_("Суффикс"), max_length=20, blank=True),
    )
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активно"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Показатель")
        verbose_name_plural = _("Показатели")
        ordering = ["ordering", "id"]

    def __str__(self) -> str:
        return self.safe_translation_getter("name", any_language=True) or f"Metric {self.pk}"


class TeamMember(TranslatableModel):
    translations = TranslatedFields(
        full_name=models.CharField(_("ФИО"), max_length=150),
        role=models.CharField(_("Роль"), max_length=120),
        short_bio=models.TextField(_("Краткая биография"), blank=True),
    )
    photo = models.ImageField(_("Фото"), upload_to="about/team/")
    social_links = models.JSONField(_("Соцсети"), blank=True, null=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Член команды")
        verbose_name_plural = _("Команда")
        ordering = ["ordering", "id"]

    def __str__(self) -> str:
        return self.safe_translation_getter("full_name", any_language=True) or f"Team member {self.pk}"


class Value(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Заголовок"), max_length=150),
        description=models.TextField(_("Описание")),
    )
    icon = models.ImageField(_("Иконка"), upload_to="about/values/", blank=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активно"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Ценность")
        verbose_name_plural = _("Ценности")
        ordering = ["ordering", "id"]

    def __str__(self) -> str:
        return self.safe_translation_getter("title", any_language=True) or f"Value {self.pk}"


class Video(TranslatableModel):
    class Page(models.TextChoices):
        HOME = "home", _("Главная")
        ABOUT = "about", _("О нас")

    translations = TranslatedFields(
        title=models.CharField(_("Заголовок"), max_length=200, blank=True),
    )
    page = models.CharField(_("Страница"), max_length=10, choices=Page.choices)
    file = models.FileField(_("Видео-файл"), upload_to="videos/", blank=True, null=True)
    youtube_url = models.URLField(_("YouTube ссылка"), blank=True)
    is_active = models.BooleanField(_("Активно"), default=True)
    order = models.PositiveIntegerField(_("Порядок"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Видео")
        verbose_name_plural = _("Видео")
        ordering = ("order", "-created_at")

    def __str__(self) -> str:
        base = self.safe_translation_getter("title", any_language=True) or dict(self.Page.choices).get(
            self.page, "Video"
        )
        return f"{base}"

    def clean(self):
        if not self.file and not self.youtube_url:
            raise ValidationError(_("Заполните видеофайл или ссылку YouTube."))
        if self.youtube_url and "youtu" not in self.youtube_url:
            raise ValidationError(_("Поддерживаются только ссылки YouTube."))
        # Можно разрешить указание и файла, и ссылки, но если нужно строго одно,
        # можно раскомментировать код ниже.
        # if self.file and self.youtube_url:
        #     raise ValidationError(_("Укажите либо файл, либо ссылку, но не оба."))

    @property
    def youtube_embed(self) -> str | None:
        if not self.youtube_url:
            return None
        url = self.youtube_url.strip()
        match = re.search(r"(?:youtu\.be/|v=)([\w\-]{11})", url)
        video_id = match.group(1) if match else None
        return f"https://www.youtube.com/embed/{video_id}" if video_id else None


class CompanyInfo(TranslatableModel):
    translations = TranslatedFields(
        mission_text=models.TextField(_("Миссия"), blank=True),
        about_text=models.TextField(_("О компании"), blank=True),
    )
    contacts = models.JSONField(_("Контакты"), blank=True, null=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    def clean(self):
        if CompanyInfo.objects.exclude(pk=self.pk).exists():
            raise ValidationError(_("Разрешена только одна запись CompanyInfo (singleton)."))

    class Meta:
        verbose_name = _("Информация о компании")
        verbose_name_plural = _("Информация о компании")

    def __str__(self) -> str:
        return self.safe_translation_getter("about_text", any_language=True) or str(
            _("Информация о компании")
        )


# --- Контакты ---


class SocialMap(models.Model):
    instagram_url = models.URLField(_("Instagram"), blank=True)
    facebook_url = models.URLField(_("Facebook"), blank=True)
    youtube_url = models.URLField(_("YouTube"), blank=True)
    tiktok_url = models.URLField(_("Whatsapp"), blank=True)
    telegram_url = models.URLField(_("Telegram"), blank=True)
    map_embed = models.TextField(_("Карта (встраиваемый код)"), blank=True)
    map_url = models.URLField(_("Ссылка на карту"), blank=True)
    is_active = models.BooleanField(_("Активна"), default=True, db_index=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Соцсети и карта")
        verbose_name_plural = _("Соцсети и карта")

    def save(self, *args, **kwargs):
        if self.is_active:
            SocialMap.objects.exclude(pk=self.pk).update(is_active=False)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"SocialMap #{self.pk}" if self.pk else "SocialMap"


class ContactAddress(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Название"), max_length=150, blank=True),
        city=models.CharField(_("Город"), max_length=120, blank=True),
        address=models.TextField(_("Адрес")),
    )
    order = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Адрес")
        verbose_name_plural = _("Адреса")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        title = self.safe_translation_getter("title", any_language=True)
        city = self.safe_translation_getter("city", any_language=True)
        address = self.safe_translation_getter("address", any_language=True)
        parts = [part for part in [title, city, address] if part]
        return ", ".join(parts) if parts else f"Адрес #{self.pk}"


class ContactPhone(TranslatableModel):
    translations = TranslatedFields(
        label=models.CharField(_("Подпись"), max_length=120, blank=True),
    )
    phone = models.CharField(_("Телефон"), max_length=50)
    order = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Телефон")
        verbose_name_plural = _("Телефоны")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        label = self.safe_translation_getter("label", any_language=True)
        return label or self.phone


class ContactEmail(TranslatableModel):
    translations = TranslatedFields(
        label=models.CharField(_("Подпись"), max_length=120, blank=True),
    )
    email = models.EmailField(_("Email"))
    order = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Email")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        label = self.safe_translation_getter("label", any_language=True)
        return label or self.email


class ContactWorkingHours(TranslatableModel):
    translations = TranslatedFields(
        weekdays=models.CharField(_("Будни"), max_length=200),
        saturday=models.CharField(_("Суббота"), max_length=200),
        sunday=models.CharField(_("Воскресенье"), max_length=200),
        note=models.CharField(_("Примечание"), max_length=200, blank=True),
    )
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Режим работы")
        verbose_name_plural = _("Режим работы")

    def clean(self):
        super().clean()
        if self.is_active:
            qs = ContactWorkingHours.objects.filter(is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(_("Может существовать только одна активная запись времени работы."))

    def __str__(self) -> str:
        return self.safe_translation_getter("weekdays", any_language=True) or f"Hours {self.pk}"


class ContactTopic(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название"), max_length=150),
    )
    slug = models.SlugField(_("Слаг"), unique=True, max_length=160)

    class Meta:
        verbose_name = _("Тема обращения")
        verbose_name_plural = _("Темы обращений")
        ordering = ["slug"]

    def save(self, *args, **kwargs):
        if not self.slug:
            name_value = self.safe_translation_getter("name", any_language=True) or ""
            base = slugify(name_value) or "topic"
            slug = base
            index = 1
            while ContactTopic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{index}"
                index += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.safe_translation_getter("name", any_language=True) or f"Topic {self.pk}"


class ContactRequest(models.Model):
    name = models.CharField(_("Имя"), max_length=150)
    phone = models.CharField(_("Телефон"), max_length=50)
    email = models.EmailField(_("Email"), blank=True)
    topic = models.ForeignKey(
        ContactTopic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests",
        verbose_name=_("Тема"),
    )
    message = models.TextField(_("Сообщение"))
    consent = models.BooleanField(_("Согласие на обработку персональных данных"), default=False)
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField(_("IP"), null=True, blank=True)
    user_agent = models.TextField(_("User-Agent"), blank=True)

    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return f"{self.name} — {self.phone}"
