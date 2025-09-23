import sqlalchemy
from asyncdjangoorm._internal.init_tables import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import operators
from sqlalchemy import func, and_


class Q:
    def __init__(self, *conditions, join_type="and"):
        self.conditions = conditions
        self.join_type = join_type.lower()
        
    
    def __and__(self, other):
        return Q(self, other, join_type="and")
    
    def __or__(self, other):
        return Q(self, other, join_type="or")
    
    def build(self):
        conds = [c.build() if isinstance(c, Q) else c for c in self.conditions]
        return sqlalchemy.and_(*conds) if self.join_type == "and" else sqlalchemy.or_(*conds)



class F:
    def __init__(self, field):
        self.field = field
        
    def resolve(self, model):
        return getattr(model, self.field)




LOOKUP_MAP = {
    # Equality
    "exact": operators.eq,
    "iexact": lambda c, v: func.lower(c) == func.lower(v),

    # String containment
    "contains": operators.contains_op,
    "icontains": lambda c, v: func.lower(c).contains(func.lower(v)),

    # Comparisons
    "gt": operators.gt,
    "gte": operators.ge,
    "lt": operators.lt,
    "lte": operators.le,

    # In / not in
    "in": operators.in_op,
    "not_in": lambda c, v: ~c.in_(v),

    # Starts/ends with
    "startswith": operators.startswith_op,
    "istartswith": lambda c, v: func.lower(c).startswith(func.lower(v)),
    "endswith": operators.endswith_op,
    "iendswith": lambda c, v: func.lower(c).endswith(func.lower(v)),

    # Null checks
    "in": lambda col, val: col.in_(val),
    "not_in": lambda col, val: ~col.in_(val),
    "isnull": lambda c, v: (c.is_(None) if v else c.isnot(None)),

    # Range
    "range": lambda c, v: and_(c >= v[0], c <= v[1]),

    # Regex
    "regex": lambda c, v: c.op("~")(v),
    "iregex": lambda c, v: c.op("~*")(v),

    # Exact inequality
    "ne": operators.ne,

    # Boolean field check
    "is": operators.is_,
    "isnot": operators.isnot,
    "between": lambda c, v: and_(c >= v[0], c <= v[1]),
}






class Queryset:
    def __init__(self, model, query=None):
        self.model = model
        self.query = query or sqlalchemy.select(model)
    
    
    def _clone(self, query):
        return Queryset(self.model, query=query)
    
    
    def _build_filters(self, **kwargs):
        conditions = []
        for key, value in kwargs.items():
            if isinstance(value, Q):
                conditions.append(value.build())
            
            else: 
                if '__' in key:
                    field, lookup = key.split("__", 1)
                    column = getattr(self.model, field)
                    op = LOOKUP_MAP.get(lookup)
                    if not op:
                        raise ValueError(f"Unsupported lookup: {lookup}")
                    
                    if isinstance(value, F):
                        value = value.resolve(self.model)
                    conditions.append(op(column, value))
                else: 
                    column = getattr(self.model, key)
                    if isinstance(value, F):
                        value = value.resolve(self.model)
                    conditions.append(column == value)
        return sqlalchemy.and_(*conditions)
    
        
    def filter(self, **kwargs):
        query = self.query.where(self._build_filters(**kwargs))
        return self._clone(query)
    
    
    def exclude(self, **kwargs):
        query = self.query.filter(~self._build_filters(**kwargs))
        return self._clone(query)
    
    
    def order_by(self, *fields):
        ordering = []
        for f in fields:
            if f.startswith("-"):
                ordering.append(getattr(self.model, f[1:]).desc())
            else: 
                ordering.append(getattr(self.model, f).asc())
        query = self.query.order_by(*ordering)
        return self._clone(query)
    
    
    def distinct(self):
        return self._clone(self.query.distinct())
    
    def values(self, *fields):
        cols = [getattr(self.model, f) for f in fields]
        return self._clone(sqlalchemy.select(*cols))
    
    
    async def values_list(self, *fields, flat=False):
        cols = [getattr(self.model, f) for f in fields]
        stmt = sqlalchemy.select(*cols)
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(stmt)
            rows = result.all()
            if flat and len(cols) == 1:
                return [row[0] for row in rows]
            return rows
    
    async def all(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(self.query)
            return result.scalars().first()
    
    
    async def first(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                self.query.order_by(sqlalchemy.desc("id")).limit(1)
            )
            return result.scalars().first()
    
    
    async def last(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(self.query.order_by(sqlalchemy.desc("id")).limit(1))
            return result.scalars().first()
    
    
    async def get(self, **kwargs):
        qs = self.filter(**kwargs)
        async with AsyncSessionLocal() as session:
            result = await session.execute(qs.query)
            obj = result.scalars().all()
            if len(obj) == 0:
                raise ValueError("DoesNotExist")
            if len(obj) > 1:
                raise ValueError("MultipleObjectsReturned")
            return obj[0]
    
    
    async def count(self):
        async with AsyncSessionLocal() as seession:
            stmt = sqlalchemy.select(sqlalchemy.func.count()).select_from(self.query.subquery())
            result = await seession.execute(stmt)
            return result.scalar_one()
    
    
    async def exists(self):
        return (await self.count()) > 0
    
    
    async def aggregate(self, **kwargs):
        stmt = sqlalchemy.select(*[v.label(k) for k, v in kwargs.items()])
        async with AsyncSessionLocal() as session:
            result = await session.execute(stmt)
            return result.mappings().first()
    
    
    def annotate(self, **annotations):
        cols = [self.model]
        for name, expr in annotations.items():
            cols.append(expr.label(name))
        query = sqlalchemy.select(*cols).select_from(self.model)
        return self._clone(query)

    
    async def create(self, **kwargs):
        async with AsyncSessionLocal() as session:
            obj = self.model(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
    
    
    async def update(self, **kwargs):
        async with AsyncSessionLocal() as session:
            stmt = sqlalchemy.update(self.model).where(
                self.query._where_criteria
            ).values(**kwargs)
            await session.execute(stmt)
            await session.commit()
            
        
    async def delete(self):
        async with AsyncSessionLocal() as session:
            stmt = sqlalchemy.delete(self.model).where(self.query._where_criteria)
            await session.execute(stmt)
            await session.commit()


    async def get_or_create(self, defaults=None, **kwargs):
        try:
            obj = await self.get(**kwargs)
            return obj, False
        except ValueError:
            params = {**kwargs, **(defaults or {})}
            obj = await self.create(**params)
            return obj, True
        
    
    async def update_or_create(self, defaults=None, **kwargs):
        try:
            obj = await self.get(**kwargs)
            for k, v in (defaults or {}).items():
                setattr(obj, k, v)
            async with AsyncSessionLocal() as session:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
            return obj, False
        except ValueError:
            params = {**kwargs, **(defaults or {})}
            obj = await self.create(**params)
            return obj, True
            
    
    async def bulk_update(self, objs: list[dict], key_field="id"):
        async with AsyncSessionLocal() as session:
            for obj in objs:
                pk = obj.pop(key_field)
                stmt = (
                    sqlalchemy.update(self.model)
                    .where(getattr(self.model, key_field) == pk)
                    .values(**obj)
                )
                await session.execute(stmt)
            await session.commit()
    
    
    async def bulk_delete(self, ids: list[int], key_field="id"):
        async with AsyncSessionLocal() as session:
            stmt = sqlalchemy.delete(self.model).where(
                getattr(self.model, key_field).in_(ids)
            )
            await session.execute(stmt)
            await session.commit()
    
    
    def __getitem__(self, k):
        if isinstance(k, slice):
            query = self.query.offset(k.start or 0)
            if k.stop is not None:
                query = query.limit(k.stop - (k.start or 0))
            return self._clone(query)
        elif isinstance(k, int):
            query = self.query.offset(k).limit(1)
            return self._clone(query)
        else: 
            raise TypeError("Invalid argument type")
    
    
    def union(self, other):
        return self._clone(self.query.union(other.query))
    
    
    def intersection(self, other):
        return self._clone(self.query.intersect(other.query))
    
    
    def difference(self, other):
        return self._clone(self.query.except_(other.query))


    def select_related(self, *related_fields):
        query = self.query
        for rel in related_fields:
            query = query.options(sqlalchemy.orm.joinload(getattr(self.model, rel)))
        return self._clone(query)
    
    
    def prefetch_related(self, **related_fields):
        
        query = self.query
        for rel in related_fields:
            query = query.options(sqlalchemy.orm.selectinload(getattr(self.model, rel)))
        return self._clone(query)
    
    
    def defer(self, *fields):
        opts = [sqlalchemy.orm.defer(f) for f in fields]
        return self._clone(self.query.options(*opts))
    
    
    def only(self, *fields):
        opts = [sqlalchemy.orm.load_only(*fields)]
        return self._clone(self.query.options(*opts))
    
    
