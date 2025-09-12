from rest_framework import serializers


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if not "youtube.com" in str(tmp_val):
            raise serializers.ValidationError('Должна быть указана ссылка на видео с youtube.com')
