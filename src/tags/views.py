from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TagForm
from .models import TAG_SCALES, Tag


def create_tag_view(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        # Check for existing active tags with the same data before validation
        data = request.POST.get("_data")
        existing_tag = Tag.objects.filter(_data=data, active=True).first()
        if existing_tag:
            # Add a message about the existing tag
            return redirect(
                reverse("tag_detail", kwargs={"tag_id": existing_tag.pk})
                + "?existing=true"
            )

        # Proceed with form validation and saving if no duplicates exist
        if form.is_valid():
            tag = form.save()
            return redirect(reverse("tag_detail", kwargs={"tag_id": tag.pk}))
    else:
        form = TagForm()

    return render(request, "create_tag.html", {"form": form})


def tag_detail_view(request, tag_id):
    # Retrieve the tag using the primary key (pk)
    tag = get_object_or_404(Tag, pk=tag_id, active=True)

    existing = request.GET.get("existing", "false").lower() == "true"

    return render(request, "tag_detail.html", {"tag": tag, "existing": existing})


def tag_image_view(request, tag_id):
    # Fetch the tag object, ensuring it exists and is active
    tag = get_object_or_404(Tag, pk=tag_id, active=True)

    # Get the size from query parameters (default to 300px)
    scale = int(request.GET.get("scale", TAG_SCALES[0]))

    if scale not in TAG_SCALES:
        return HttpResponseBadRequest(f"Invalid scale parameter.")

    # Generate the PIL image for the tag
    pil_image = tag.get_image(scale=scale)

    # Convert the PIL image to an HTTP response
    response = HttpResponse(content_type="image/png")
    pil_image.save(response, "PNG")
    return response
