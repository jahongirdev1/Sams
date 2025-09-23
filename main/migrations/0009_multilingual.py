from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import ckeditor.fields


def copy_translations(apps, schema_editor):
    language = "ru"

    CarouselItem = apps.get_model("main", "CarouselItem")
    CarouselItemTranslation = apps.get_model("main", "CarouselItemTranslation")
    for obj in CarouselItem.objects.all():
        CarouselItemTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            title=getattr(obj, "title", ""),
            subtitle=getattr(obj, "subtitle", ""),
        )

    SectionHeader = apps.get_model("main", "SectionHeader")
    SectionHeaderTranslation = apps.get_model("main", "SectionHeaderTranslation")
    for obj in SectionHeader.objects.all():
        SectionHeaderTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            title=getattr(obj, "title", ""),
            description=getattr(obj, "description", ""),
        )

    Category = apps.get_model("main", "Category")
    CategoryTranslation = apps.get_model("main", "CategoryTranslation")
    for obj in Category.objects.all():
        CategoryTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            name=getattr(obj, "name", ""),
            description=getattr(obj, "description", ""),
        )

    Product = apps.get_model("main", "Product")
    ProductTranslation = apps.get_model("main", "ProductTranslation")
    for obj in Product.objects.all():
        ProductTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            name=getattr(obj, "name", ""),
            description=getattr(obj, "description", ""),
        )

    ProductImage = apps.get_model("main", "ProductImage")
    ProductImageTranslation = apps.get_model("main", "ProductImageTranslation")
    for obj in ProductImage.objects.all():
        ProductImageTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            alt_text=getattr(obj, "alt_text", ""),
        )

    Advantage = apps.get_model("main", "Advantage")
    AdvantageTranslation = apps.get_model("main", "AdvantageTranslation")
    for obj in Advantage.objects.all():
        AdvantageTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            title=getattr(obj, "title", ""),
            description=getattr(obj, "description", ""),
        )

    Metric = apps.get_model("main", "Metric")
    MetricTranslation = apps.get_model("main", "MetricTranslation")
    for obj in Metric.objects.all():
        MetricTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            name=getattr(obj, "name", ""),
            value=getattr(obj, "value", ""),
            suffix=getattr(obj, "suffix", ""),
        )

    TeamMember = apps.get_model("main", "TeamMember")
    TeamMemberTranslation = apps.get_model("main", "TeamMemberTranslation")
    for obj in TeamMember.objects.all():
        TeamMemberTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            full_name=getattr(obj, "full_name", ""),
            role=getattr(obj, "role", ""),
            short_bio=getattr(obj, "short_bio", ""),
        )

    Value = apps.get_model("main", "Value")
    ValueTranslation = apps.get_model("main", "ValueTranslation")
    for obj in Value.objects.all():
        ValueTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            title=getattr(obj, "title", ""),
            description=getattr(obj, "description", ""),
        )

    Video = apps.get_model("main", "Video")
    VideoTranslation = apps.get_model("main", "VideoTranslation")
    for obj in Video.objects.all():
        VideoTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            title=getattr(obj, "title", ""),
        )

    CompanyInfo = apps.get_model("main", "CompanyInfo")
    CompanyInfoTranslation = apps.get_model("main", "CompanyInfoTranslation")
    for obj in CompanyInfo.objects.all():
        CompanyInfoTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            mission_text=getattr(obj, "mission_text", ""),
            about_text=getattr(obj, "about_text", ""),
        )

    ContactAddress = apps.get_model("main", "ContactAddress")
    ContactAddressTranslation = apps.get_model("main", "ContactAddressTranslation")
    for obj in ContactAddress.objects.all():
        ContactAddressTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            title=getattr(obj, "title", ""),
            city=getattr(obj, "city", ""),
            address=getattr(obj, "address", ""),
        )

    ContactPhone = apps.get_model("main", "ContactPhone")
    ContactPhoneTranslation = apps.get_model("main", "ContactPhoneTranslation")
    for obj in ContactPhone.objects.all():
        ContactPhoneTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            label=getattr(obj, "label", ""),
        )

    ContactEmail = apps.get_model("main", "ContactEmail")
    ContactEmailTranslation = apps.get_model("main", "ContactEmailTranslation")
    for obj in ContactEmail.objects.all():
        ContactEmailTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            label=getattr(obj, "label", ""),
        )

    ContactWorkingHours = apps.get_model("main", "ContactWorkingHours")
    ContactWorkingHoursTranslation = apps.get_model("main", "ContactWorkingHoursTranslation")
    for obj in ContactWorkingHours.objects.all():
        ContactWorkingHoursTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            weekdays=getattr(obj, "weekdays", ""),
            saturday=getattr(obj, "saturday", ""),
            sunday=getattr(obj, "sunday", ""),
            note=getattr(obj, "note", ""),
        )

    ContactTopic = apps.get_model("main", "ContactTopic")
    ContactTopicTranslation = apps.get_model("main", "ContactTopicTranslation")
    for obj in ContactTopic.objects.all():
        ContactTopicTranslation.objects.create(
            master_id=obj.pk,
            language_code=language,
            name=getattr(obj, "name", ""),
        )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_product_description_richtext"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdvantageTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.advantage",
                    ),
                ),
            ],
            options={
                "db_table": "main_advantage_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="CarouselItemTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("title", models.CharField(blank=True, max_length=150)),
                ("subtitle", models.CharField(blank=True, max_length=250)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.carouselitem",
                    ),
                ),
            ],
            options={
                "db_table": "main_carouselitem_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="CategoryTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.category",
                    ),
                ),
            ],
            options={
                "db_table": "main_category_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="CompanyInfoTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("mission_text", models.TextField(blank=True)),
                ("about_text", models.TextField(blank=True)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.companyinfo",
                    ),
                ),
            ],
            options={
                "db_table": "main_companyinfo_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ContactAddressTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("title", models.CharField(blank=True, max_length=150)),
                ("city", models.CharField(blank=True, max_length=120)),
                ("address", models.TextField()),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.contactaddress",
                    ),
                ),
            ],
            options={
                "db_table": "main_contactaddress_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ContactEmailTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("label", models.CharField(blank=True, max_length=120)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.contactemail",
                    ),
                ),
            ],
            options={
                "db_table": "main_contactemail_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ContactPhoneTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("label", models.CharField(blank=True, max_length=120)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.contactphone",
                    ),
                ),
            ],
            options={
                "db_table": "main_contactphone_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ContactTopicTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("name", models.CharField(max_length=150)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.contacttopic",
                    ),
                ),
            ],
            options={
                "db_table": "main_contacttopic_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ContactWorkingHoursTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("weekdays", models.CharField(max_length=200)),
                ("saturday", models.CharField(max_length=200)),
                ("sunday", models.CharField(max_length=200)),
                ("note", models.CharField(blank=True, max_length=200)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.contactworkinghours",
                    ),
                ),
            ],
            options={
                "db_table": "main_contactworkinghours_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="MetricTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("name", models.CharField(max_length=120)),
                ("value", models.CharField(max_length=60)),
                ("suffix", models.CharField(blank=True, max_length=20)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.metric",
                    ),
                ),
            ],
            options={
                "db_table": "main_metric_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ProductImageTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("alt_text", models.CharField(blank=True, max_length=150)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.productimage",
                    ),
                ),
            ],
            options={
                "db_table": "main_productimage_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ProductTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("name", models.CharField(max_length=180)),
                ("description", ckeditor.fields.RichTextField(blank=True)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.product",
                    ),
                ),
            ],
            options={
                "db_table": "main_product_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="SectionHeaderTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.sectionheader",
                    ),
                ),
            ],
            options={
                "db_table": "main_sectionheader_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="TeamMemberTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("full_name", models.CharField(max_length=150)),
                ("role", models.CharField(max_length=120)),
                ("short_bio", models.TextField(blank=True)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.teammember",
                    ),
                ),
            ],
            options={
                "db_table": "main_teammember_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="ValueTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.value",
                    ),
                ),
            ],
            options={
                "db_table": "main_value_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.CreateModel(
            name="VideoTranslation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language_code", models.CharField(db_index=True, max_length=15)),
                ("title", models.CharField(blank=True, max_length=200)),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="main.video",
                    ),
                ),
            ],
            options={
                "db_table": "main_video_translation",
                "unique_together": {("language_code", "master")},
            },
        ),
        migrations.RunPython(copy_translations, migrations.RunPython.noop),
        migrations.RemoveField(model_name="advantage", name="description"),
        migrations.RemoveField(model_name="advantage", name="title"),
        migrations.RemoveField(model_name="carouselitem", name="subtitle"),
        migrations.RemoveField(model_name="carouselitem", name="title"),
        migrations.RemoveField(model_name="category", name="description"),
        migrations.RemoveField(model_name="category", name="name"),
        migrations.RemoveField(model_name="companyinfo", name="about_text"),
        migrations.RemoveField(model_name="companyinfo", name="mission_text"),
        migrations.RemoveField(model_name="contactaddress", name="address"),
        migrations.RemoveField(model_name="contactaddress", name="city"),
        migrations.RemoveField(model_name="contactaddress", name="title"),
        migrations.RemoveField(model_name="contactemail", name="label"),
        migrations.RemoveField(model_name="contactphone", name="label"),
        migrations.RemoveField(model_name="contacttopic", name="name"),
        migrations.RemoveField(model_name="contactworkinghours", name="note"),
        migrations.RemoveField(model_name="contactworkinghours", name="saturday"),
        migrations.RemoveField(model_name="contactworkinghours", name="sunday"),
        migrations.RemoveField(model_name="contactworkinghours", name="weekdays"),
        migrations.RemoveField(model_name="metric", name="name"),
        migrations.RemoveField(model_name="metric", name="suffix"),
        migrations.RemoveField(model_name="metric", name="value"),
        migrations.RemoveField(model_name="product", name="description"),
        migrations.RemoveField(model_name="product", name="name"),
        migrations.RemoveField(model_name="productimage", name="alt_text"),
        migrations.RemoveField(model_name="sectionheader", name="description"),
        migrations.RemoveField(model_name="sectionheader", name="title"),
        migrations.RemoveField(model_name="teammember", name="full_name"),
        migrations.RemoveField(model_name="teammember", name="role"),
        migrations.RemoveField(model_name="teammember", name="short_bio"),
        migrations.RemoveField(model_name="value", name="description"),
        migrations.RemoveField(model_name="value", name="title"),
        migrations.RemoveField(model_name="video", name="title"),
    ]
