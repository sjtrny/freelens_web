import inspect
import random

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from freelens import Tag as FreelensTag
from freelens import max_int_for_N, message_length_for_N

TAG_SIZE_CHOICES = {5: "5", 7: "7", 9: "9", 11: "11"}

TAG_SCALES = [1, 2, 4]


def get_defaults_as_dict(func):
    """
    Extract default parameter values as a dictionary.
    """
    sig = inspect.signature(func)
    return {
        k: v.default
        for k, v in sig.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_new_message_int(n):
    # Define the range
    start, end = 0, max_int_for_N(n)

    # Get the set of used numbers
    used_numbers = set(
        Tag.objects.filter(active=True).values_list("message_int", flat=True)
    )

    # Calculate available numbers
    available_numbers = set(range(start, end + 1)) - used_numbers

    if not available_numbers:
        raise ValidationError(f"No available tags left for N={n}.")

    # Randomly select an available number
    return random.choice(list(available_numbers))


class Tag(models.Model):
    # Creation date - datetime
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Active
    active = models.BooleanField(default=True)
    last_accessed = models.DateTimeField(default=now, editable=False)
    # Size
    N = models.PositiveIntegerField(default=5, choices=TAG_SIZE_CHOICES)
    # Message - integer
    message_int = models.BigIntegerField(
        blank=False,
        editable=False,
        default=-1,
    )
    # URL or Associated Data - max length of a URL
    _data = models.CharField(max_length=2048, blank=False, editable=True)

    @property
    def data(self):
        # Update last_accessed when data is retrieved
        self.last_accessed = now()
        self.save(update_fields=["last_accessed"])
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    class Meta:
        constraints = [
            # Enforce that message int is unique amongst active tags
            models.UniqueConstraint(
                fields=["message_int"],
                condition=Q(active=True),
                name="unique_active_message_int",
            )
        ]

    def clean(self):
        super().clean()

        # Use the _data field directly to avoid triggering the @property logic
        if self._data:
            # Check for existing active tags with the same data
            existing_tag = (
                Tag.objects.filter(_data=self._data, active=True)
                .exclude(pk=self.pk)
                .first()
            )
            if existing_tag:
                raise ValidationError(
                    f"A tag with the data '{self._data}' already exists."
                )

    def save(self, *args, **kwargs):
        # Check for an existing tag with the same data
        existing_tag = Tag.objects.filter(_data=self._data, active=True).first()

        if existing_tag:
            # Copy all fields dynamically
            for field in self._meta.fields:
                if field.name != "id" and not field.auto_created:
                    setattr(self, field.name, getattr(existing_tag, field.name))
        else:
            # If no existing tag is found, generate a new message_int if not set
            if self.message_int < 0:
                self.message_int = get_new_message_int(self.N)

        # Save the model (either updates or creates, depending on `pk`)
        super().save(*args, **kwargs)

    def get_image(self, scale=1):
        n_bits_message = message_length_for_N(self.N)
        message_binary_string = format(self.message_int, f"0{n_bits_message}b")
        tag = FreelensTag.from_message(message_binary_string, n=self.N)

        sig = inspect.signature(tag.to_image)

        return tag.to_image(
            cell_size=scale * sig.parameters["cell_size"].default,
            quiet_pad_size=scale * sig.parameters["quiet_pad_size"].default,
        )

    def __str__(self):
        return f"Tag {self.N}x{self.N} ({self.message_int}) - {self._data}"
