import os

from django.conf import settings
from django.shortcuts import render


def album_list(request):
    base_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'laotong')
    names = []
    if os.path.isdir(base_dir):
        for f in os.listdir(base_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                names.append(f)
    images = [{'src': f"/static/img/laotong/{name}", 'title': os.path.splitext(name)[0]} for name in sorted(names)]
    context = {'images': images}
    return render(request, 'album/list.html', context)
