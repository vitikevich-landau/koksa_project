import os
import re

from django.db import models
from ckeditor.fields import RichTextField
from transliterate import translit


class StaticCategories(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'static_categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


def _create_upload_link(f_name):
    from appl.middlewares import get_current_host
    from koksa_project.settings import MEDIA_URL

    return f'{get_current_host()}{MEDIA_URL}{f_name}'


class Static(models.Model):
    #   Default visibility
    VISIBLE = 1

    #  Empty fields
    EMPTY = ''

    ATTACHMENTS_SEPARATORS_COUNT = 25
    REGEX = r'<p>\*{}.*$'.format(f'{{{ATTACHMENTS_SEPARATORS_COUNT},}}')

    ATTACHMENT_LINK_TPL = '<a href="{url}" class="content-files">{name}</a><br />'

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

        not_empty_attachments = list(filter(lambda v: v.file.name, self.staticcontentattachments_set.all()))

        links = map(
            lambda v: self.ATTACHMENT_LINK_TPL.format(
                url=_create_upload_link(v.file.name), name=os.path.basename(v.file.name)
            ),
            reversed(not_empty_attachments)
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

        self.content = re.sub(self.REGEX, self.EMPTY, self.content, flags=re.S)

    def save(self, *args, **kwargs):
        self.clear_content()
        links = self.create_attachments_links()
        if links:
            self.content += f'{self.add_attachments_marker()}{self.create_attachments_links()}'

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
        #  Перевод в транслит для корректного сохранения
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
