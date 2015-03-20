from models import Image, ImageSet, ImageImageSet


def create_image_set(image_id_list):
    image_set = ImageSet.objects.create()
    for image_id in image_id_list:
        if image_id is str:
            image_id = int(image_id)
        image = Image.objects.filter(id=image_id)
        if image.count() == 1:
            image = image[0]
            ImageImageSet.objects.create(image_set=image_set, image=image)
    return image_set


def add_to_image_set(image_set_id, image_id_list):
    added = []
    if image_set_id is str:
        image_set_id = int(image_set_id)
    image_set = ImageSet.objects.filter(id=image_set_id)
    if image_set.count() == 1:
        image_set = image_set[0]
        for image_id in image_id_list:
            if image_id is str:
                image_id = int(image_id)
            image = Image.objects.filter(id=image_id)
            if image.count() == 1:
                image = image[0]
                ImageImageSet.objects.get_or_create(image_set=image_set, image=image)
                added.append(image_id)
    return added


def remove_from_image_set(image_set_id, image_id_list):
    removed = []
    if image_set_id is str:
        image_set_id = int(image_set_id)
    image_set = ImageSet.objects.filter(id=image_set_id)
    if image_set.count() == 1:
        image_set = image_set[0]
        for image_id in image_id_list:
            if image_id is str:
                image_id = int(image_id)
            image = Image.objects.filter(id=image_id)
            if image.count() == 1:
                image = image[0]
                ImageImageSet.objects.filter(image_set=image_set, image=image).delete()
                removed.append(image_id)
    return removed


def update_image_set(image_set_id, image_id_list):
    if image_set_id is str:
        image_set_id = int(image_set_id)
    image_set = ImageSet.objects.filter(id=image_set_id)
    if image_set.count() == 1:
        image_set = image_set[0]
        ImageImageSet.objects.filter(image_set=image_set).delete()
        return add_to_image_set(image_set_id, image_id_list)
    return []