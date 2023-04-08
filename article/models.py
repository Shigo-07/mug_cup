from django.db import models
from mdeditor.fields import MDTextField
import markdown


# Create your models here.

class Article(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=100)
    content = MDTextField()

    def __str__(self):
        return self.title

    def markdown_to_html(self):
        md = markdown.Markdown(
            extensions=['extra', 'admonition', 'sane_lists', 'toc']
        )
        html = md.convert(self.content)
        return html
