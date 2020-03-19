# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import os
import re

from django.db import models
from ckeditor.fields import RichTextField
from transliterate import translit


class StaticCategories(models.Model):
    id = models.SmallAutoField(primary_key=True)
    usestart = models.PositiveIntegerField()
    usefinal = models.PositiveIntegerField()
    parent = models.PositiveSmallIntegerField()
    type = models.PositiveIntegerField()
    usepic = models.IntegerField()
    picwidth = models.SmallIntegerField()
    picheight = models.SmallIntegerField()
    matlimit = models.PositiveIntegerField()
    ordering = models.PositiveIntegerField()
    main_material = models.PositiveIntegerField()
    alias = models.CharField(max_length=256)
    name = models.TextField()
    keywords = models.TextField()
    description = models.TextField()
    my_template = models.TextField()
    template = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'static_categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Static(models.Model):
    #   Default visibility
    VISIBLE = 1

    #  Empty fields
    EMPTY = ''

    REGEX = r'<p>\*{25,}.*$'

    ATTACHMENT_LINK_TPL = '<a href="{url}" class="content-files">{name}</a><br />'
    ATTACHMENTS_SEPARATORS_COUNT = 125

    #   Fields descriptions
    CATEGORY_DESCRIPTION = 'Пункт меню'
    START_DESCRIPTION = 'Дата публикации'
    TITLE_DESCRIPTION = 'Название'
    ICON_DESCRIPTION = 'Картинка'
    SHORT_DESCRIPTION = 'Анонс'
    CONTENT_DESCRIPTION = 'Подробнее'

    visibility = models.PositiveIntegerField(default=VISIBLE)
    category = models.ForeignKey(StaticCategories, on_delete=models.CASCADE, db_column='category',
                                 verbose_name=CATEGORY_DESCRIPTION)
    start = models.DateTimeField(auto_now=True, verbose_name=START_DESCRIPTION)
    final = models.DateTimeField(auto_now=True)
    alias = models.CharField(max_length=256)

    #  SEO fields
    title_tag = models.TextField(default=EMPTY)
    keywords = models.TextField(default=EMPTY)
    description = models.TextField(default=EMPTY)

    template = models.TextField(default=EMPTY)
    title = models.TextField(verbose_name=TITLE_DESCRIPTION)
    #   Image
    icon = models.ImageField(default=EMPTY, blank=True, upload_to='%Y/%m/%d', max_length=500,
                             verbose_name=ICON_DESCRIPTION)

    #   Short description
    short = models.TextField(default=EMPTY, blank=True, verbose_name=SHORT_DESCRIPTION)
    # content = models.TextField(verbose_name=CONTENT_DESCRIPTION)
    content = RichTextField(verbose_name=CONTENT_DESCRIPTION)

    def create_attachments_links(self):
        """
        Пройтись по вложениям и сгенерить ссылки на скачивание по шаблону
        """
        from appl.current_host_middleware import get_current_host
        from koksa_project.settings import MEDIA_URL

        current_host = get_current_host()

        not_empty_attachments = filter(lambda v: v.file.name, self.staticcontentattachments_set.all())

        links = map(
            lambda v: self.ATTACHMENT_LINK_TPL.format(
                url=current_host + MEDIA_URL + v.file.name, name=os.path.basename(v.file.name)
            ),
            not_empty_attachments
        )

        return ''.join(links)

    def add_attachments_marker(self):
        """
        Маркер в конце поля "content" ниже которого будут вставление ссылки
        на скачивание вложений
        """
        return '<p>{}<p>'.format(''.join(['*'] * self.ATTACHMENTS_SEPARATORS_COUNT))

    def clear_content(self):
        """
        Очистить маркер и всё что ниже маркера, до конца
        """
        self.content = re.sub(self.REGEX, self.EMPTY, self.content, flags=re.S) \
                       + self.add_attachments_marker()

    def save(self, *args, **kwargs):
        self.clear_content()
        self.content += self.create_attachments_links()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        #   If exist icon, delete icon
        if self.icon:
            storage, path = self.icon.storage, self.icon.path
            storage.delete(path)

        #   If exist attachments, delete all attachments
        attachments = self.staticcontentattachments_set.all()

        for attachment in attachments:
            storage, path = attachment.file.storage, attachment.file.path
            storage.delete(path)

        #   Then delete bounded model
        result = super().delete(*args, **kwargs)
        return result

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'static'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


#   Attachments
class StaticContentAttachments(models.Model):
    ATTACHMENT_LINK_TPL = '<a href="{url}" class="content-files">{name}</a>'

    content = models.ForeignKey(Static, on_delete=models.CASCADE)
    file = models.FileField(upload_to='%Y/%m/%d', null=True, blank=True, verbose_name='Вложения')

    def save(self, *args, **kwargs):
        f_name, f_extension = os.path.splitext(os.path.basename(self.file.name))
        self.file.name = translit(f_name, language_code='ru', reversed=True) + f_extension

        super().save(*args, **kwargs)

        #   Save model after save attachments
        self.content.save(update_fields=['content'])

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        storage.delete(path)

        result = super().delete(*args, **kwargs)

        #   Update content
        self.content.save(update_fields=['content'])

        return result

    def __str__(self):
        return os.path.basename(self.file.name)

    class Meta:
        db_table = 'static_content_attachments'
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
