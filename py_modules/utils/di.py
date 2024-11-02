
class UnresolvableDependencyException(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class Container:
    _beans = {}

    @classmethod
    def bean(cls, clazz):
        # Registra la clase en el contenedor, creando una instancia si no existe
        cls_name = clazz.__name__
        if cls_name != 'Logger':
            instance = clazz()
            cls._beans[cls_name] = instance
            """print(f"DI - Registered instance for {cls_name}")"""
        return clazz

    @classmethod
    def resolve(cls, bean_cls, declaring_class):
        # Resuelve la instancia de la clase por su tipo
        cls_name = bean_cls.__name__
        dec_cls_name = declaring_class.__name__
        if cls_name == "Logger":
            key = f"Logger<{dec_cls_name}>"
            if key in cls._beans:
                print(f"DI - Resolved instance {key} for {dec_cls_name}")
                return cls._beans.get(key)
            else:
                params = {"name": dec_cls_name}
                instance = bean_cls(**params)
                cls._beans[key] = instance
                return instance
        else:
            if cls_name in cls._beans:
                """print(f"DI - Resolved instance {cls_name} for {dec_cls_name}")"""
                return cls._beans.get(cls_name)
            else:
                raise UnresolvableDependencyException(f"Missing instance {cls_name} for {dec_cls_name}")

def bean(cls):
    return Container.bean(cls)

def inject(cls):
    original_init = cls.__init__ if '__init__' in cls.__dict__ else lambda self: None

    def new_init(self, *args, **kwargs):

        # Inyectar dependencias basadas en las anotaciones
        for attr_name, attr_type in cls.__annotations__.items():
            if attr_name.startswith('inj_'):
                setattr(self, attr_name, Container.resolve(attr_type, cls))
                
        # Llamar al __init__ original
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
