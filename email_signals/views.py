from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from . import utils


@staff_member_required
def model_attrs(request: HttpRequest, content_type_id: int) -> JsonResponse:
    """Returns a JSON response with the model attributes for the given content
    type.
    """

    content_type = get_object_or_404(ContentType, pk=content_type_id)
    model = content_type.model_class()
    attrs = utils.get_model_attr_names(model)
    return JsonResponse(attrs, safe=False)
