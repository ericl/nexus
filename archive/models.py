from django import forms
from django.contrib import admin
from django.db import models
from os.path import basename
from pdfutil import *

class Page(models.Model):
    pdf = models.FileField(upload_to=PDF_PATH)
    parent = models.ForeignKey('PDF')

    def save(self):
        super(Page, self).save()
        self.calculate_thumbnail_url() 

    def calculate_thumbnail_url(self):
        return pdf_to_thumbnail(self.pdf.path, 512)

    def __str__(self):
        return "%s" % basename(self.pdf.path)

class PDF(models.Model):
    order = models.IntegerField()
    pdf = models.FileField(upload_to=PDF_PATH)
    parent = models.ForeignKey('Issue')

    def save(self):
        super(PDF, self).save()
        for page in self.page_set.all():
            page.delete()
        for page in burst_pdf(self.pdf.path):
            s = Page(pdf=page, parent=self)
            s.save()
            self.page_set.add(s)

    def __str__(self):
        return "%s" % basename(self.pdf.path)

    class Meta:
        ordering = ['order']

class PDFAdminForm(forms.ModelForm):
    def clean_pdf(self):
        validate_pdf(self.cleaned_data['pdf'])
        return self.cleaned_data['pdf']

class PDFInline(admin.TabularInline):
    model = PDF
    form = PDFAdminForm

class IssueAdminForm(forms.ModelForm):
    # XXX manual validation since unique=True doesn't work with inlined forms
    def clean_date(self):
        if 'date' not in self.changed_data:
            return self.cleaned_data['date']
        try:
            date = Issue.objects.get(date=self.cleaned_data['date'])
        except:
            return self.cleaned_data['date']
        raise forms.ValidationError("That date is already taken")

class IssueAdmin(admin.ModelAdmin):
    inlines = [PDFInline]
    form = IssueAdminForm

class Issue(models.Model):
    date = models.DateField(unique=True)

    def calculate_thumbnail_url(self):
        try:
            return pdf_to_thumbnail(self.pdf_set.all()[0].page_set.all()[0].pdf.path, 256)
        except IndexError: # someone deleted all the pages
            return pdf_to_thumbnail(STOCK_EMPTY_ISSUE, 256)

    def calculate_join_url(self):
        return joined_pdfs([page.pdf.path for page in self.pdf_set.all()])

    def save(self):
        super(Issue, self).save()
        self.calculate_join_url()
        self.calculate_thumbnail_url()

    def __str__(self):
        return "%s" % self.date

    class Meta:
        ordering = ['-date']