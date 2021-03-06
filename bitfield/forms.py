from django.forms import CheckboxSelectMultiple, IntegerField
from django.utils.encoding import force_unicode

from .types import BitHandler


class BitFieldCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is not None:
            value = [k for k, v in value if v]
        return super(BitFieldCheckboxSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if initial != data:
            return True
        initial_set = set([force_unicode(value) for value in initial])
        data_set = set([force_unicode(value) for value in data])
        return data_set != initial_set


class BitFormField(IntegerField):
    """
    'choices' should be a flat list of flags (just as BitField
    accepts them).
    """
    def __init__(self, choices=(), widget=BitFieldCheckboxSelectMultiple, *args, **kwargs):
        kwargs['widget'] = widget
        super(BitFormField, self).__init__(*args, **kwargs)
        self.widget.choices = [(i, i) for i in choices]
        choices = [i.encode('utf8') for i in choices]
        self.choices = choices

    def clean(self, value):
        if not value:
            return 0

        result = BitHandler(0, self.choices)
        for k in value:
            setattr(result, k.encode('utf8'), True)
        return int(result)
