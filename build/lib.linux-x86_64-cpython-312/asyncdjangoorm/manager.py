from asyncdjangoorm._internal.queryset import Queryset




class AsyncManager:
    def __init__(self, model):
        self.model = model
    
    
    def all(self):
        return Queryset(self.model)
    
    
    def filter(self, **kwargs):
        return Queryset(self.model).filter(**kwargs)
    
    
    def exclude(self, **kwargs):
        return Queryset(self.model).exclude(**kwargs)
    
    
    def order_by(self, *fields):
        return Queryset(self.model).order_by(*fields)
    
    
    def distinct(self):
        return Queryset(self.model).distinct()
    
    
    def values(self, *fields):
        return Queryset(self.model).values(*fields)
    
    
    def annotate(self, **annotations):
        return Queryset(self.model).annotate(**annotations)
    
    
    def select_related(self, *related_fields):
        return Queryset(self.model).select_related(*related_fields)
    
    
    def prefetch_related(self, **related_fields):
        return Queryset(self.model).prefetch_related(**related_fields)
    
    def only(self, *fields):
        return Queryset(self.model).only(*fields)
    
    def defer(self, *fields):
        return Queryset(self.model).defer(*fields)
    
        
    # Async methods delegate directly to Queryset
    async def get(self, **kwargs):
        return await Queryset(self.model).get(**kwargs)

    async def create(self, **kwargs):
        return await Queryset(self.model).create(**kwargs)

    async def get_or_create(self, defaults=None, **kwargs):
        return await Queryset(self.model).get_or_create(defaults=defaults, **kwargs)

    async def update_or_create(self, defaults=None, **kwargs):
        return await Queryset(self.model).update_or_create(defaults=defaults, **kwargs)

    async def bulk_update(self, objs: list[dict], key_field="id"):
        return await Queryset(self.model).bulk_update(objs, key_field=key_field)

    async def bulk_delete(self, ids: list[int], key_field="id"):
        return await Queryset(self.model).bulk_delete(ids, key_field=key_field)

    async def count(self):
        return await Queryset(self.model).count()

    async def exists(self):
        return await Queryset(self.model).exists()
    