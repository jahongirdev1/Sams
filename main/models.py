from __future__ import annotations

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# --- Главная: карусель ---
class CarouselItem(models.Model):
    title = models.CharField(_("Заголовок"), max_length=150, blank=True)
    subtitle = models.CharField(_("Подзаголовок"), max_length=250, blank=True)
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
        return self.title or f"Carousel #{self.pk}"


# --- Каталог ---
class Category(models.Model):
    name = models.CharField(_("Название"), max_length=120)
    slug = models.SlugField(_("Слаг"), unique=True, db_index=True, max_length=140)
    description = models.TextField(_("Описание"), blank=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(_("Название"), max_length=180)
    slug = models.SlugField(_("Слаг"), unique=True, db_index=True, max_length=200)
    description = models.TextField(_("Описание"), blank=True)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)
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
            base = slugify(self.name)
            slug = base
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Товар"),
    )
    image = models.ImageField(_("Изображение"), upload_to="products/")
    alt_text = models.CharField(_("Альтернативный текст"), max_length=150, blank=True)
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
                raise ValidationError("У продукта может быть только одно основное изображение (is_primary=True).")

    def __str__(self) -> str:
        return f"{self.product} image #{self.pk}"


# --- О нас ---
class Advantage(models.Model):
    title = models.CharField(_("Заголовок"), max_length=150)
    description = models.TextField(_("Описание"))
    icon = models.ImageField(_("Иконка"), upload_to="about/icons/", blank=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активно"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Преимущество")
        verbose_name_plural = _("Преимущества")
        ordering = ["ordering", "id"]


class Metric(models.Model):
    name = models.CharField(_("Название"), max_length=120)
    value = models.CharField(_("Значение"), max_length=60)
    suffix = models.CharField(_("Суффикс"), max_length=20, blank=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активно"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Показатель")
        verbose_name_plural = _("Показатели")
        ordering = ["ordering", "id"]


class TeamMember(models.Model):
    full_name = models.CharField(_("ФИО"), max_length=150)
    role = models.CharField(_("Роль"), max_length=120)
    photo = models.ImageField(_("Фото"), upload_to="about/team/")
    short_bio = models.TextField(_("Краткая биография"), blank=True)
    social_links = models.JSONField(_("Соцсети"), blank=True, null=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Член команды")
        verbose_name_plural = _("Команда")
        ordering = ["ordering", "id"]


class Value(models.Model):
    title = models.CharField(_("Заголовок"), max_length=150)
    description = models.TextField(_("Описание"))
    icon = models.ImageField(_("Иконка"), upload_to="about/values/", blank=True)
    ordering = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активно"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Ценность")
        verbose_name_plural = _("Ценности")
        ordering = ["ordering", "id"]


class CompanyInfo(models.Model):
    mission_text = models.TextField(_("Миссия"), blank=True)
    about_text = models.TextField(_("О компании"), blank=True)
    contacts = models.JSONField(_("Контакты"), blank=True, null=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    def clean(self):
        if CompanyInfo.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Разрешена только одна запись CompanyInfo (singleton).")

    class Meta:
        verbose_name = _("Информация о компании")
        verbose_name_plural = _("Информация о компании")

    def __str__(self) -> str:
        return _("Информация о компании")


# --- Контакты ---
class ContactAddress(models.Model):
    title = models.CharField(_("Название"), max_length=150, blank=True)
    city = models.CharField(_("Город"), max_length=120, blank=True)
    address = models.TextField(_("Адрес"))
    order = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Адрес")
        verbose_name_plural = _("Адреса")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        parts = [
            part
            for part in [self.title, self.city, self.address]
            if part
        ]
        return ", ".join(parts) if parts else f"Адрес #{self.pk}"


class ContactPhone(models.Model):
    label = models.CharField(_("Подпись"), max_length=120, blank=True)
    phone = models.CharField(_("Телефон"), max_length=50)
    order = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Телефон")
        verbose_name_plural = _("Телефоны")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.label or self.phone


class ContactEmail(models.Model):
    label = models.CharField(_("Подпись"), max_length=120, blank=True)
    email = models.EmailField(_("Email"))
    order = models.PositiveIntegerField(_("Порядок"), default=0, db_index=True)
    is_active = models.BooleanField(_("Активен"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Email")
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.label or self.email


class ContactWorkingHours(models.Model):
    weekdays = models.CharField(_("Будни"), max_length=200)
    saturday = models.CharField(_("Суббота"), max_length=200)
    sunday = models.CharField(_("Воскресенье"), max_length=200)
    note = models.CharField(_("Примечание"), max_length=200, blank=True)
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
        return self.weekdays


class ContactTopic(models.Model):
    name = models.CharField(_("Название"), max_length=150)
    slug = models.SlugField(_("Слаг"), unique=True, max_length=160)

    class Meta:
        verbose_name = _("Тема обращения")
        verbose_name_plural = _("Темы обращений")
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            index = 1
            while ContactTopic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{index}"
                index += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


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
