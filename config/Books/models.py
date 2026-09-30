from django.core.exceptions import ValidationError
from django.db import models


class StrictCharField(models.CharField):
    description = "A string field that rejects blank and purely numeric values."

    def to_python(self, value):
        if value is None:
            return value
        
        if not isinstance(value, str):
            raise ValidationError("Enter text, not a number.", code="invalid")
        return value.strip()

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value is None or not value.strip():
            raise ValidationError("This field cannot be blank.", code="blank")
        if value.strip().isdigit():
            raise ValidationError("This field cannot be numeric only.", code="numeric")

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if isinstance(value, str):
            value = value.strip()
            setattr(model_instance, self.attname, value)
        return value


class Book(models.Model):
    title = StrictCharField(max_length=200)
    author = StrictCharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(title=""), name="book_title_not_blank"
            ),
            models.CheckConstraint(
                condition=~models.Q(author=""), name="book_author_not_blank"
            ),
           
            models.CheckConstraint(
                condition=~models.Q(title__regex=r"^[0-9]+$"),
                name="book_title_not_numeric",
            ),
            models.CheckConstraint(
                condition=~models.Q(author__regex=r"^[0-9]+$"),
                name="book_author_not_numeric",
            ),
        ]

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures validate() runs on every save, not just in forms
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title