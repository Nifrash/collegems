from django.db import transaction


def generate_custom_id(model_class, field_name, prefix):
    """
    Generate IDs like:
    EUR.STU.0001
    EUR.LEC.0001
    EUR.STF.0001
    """

    with transaction.atomic():
        last_object = model_class.objects.select_for_update().order_by('id').last()

        if last_object:
            last_code = getattr(last_object, field_name)
            try:
                last_number = int(last_code.split('.')[-1])
            except (ValueError, AttributeError):
                last_number = 0
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}.{new_number:04d}"