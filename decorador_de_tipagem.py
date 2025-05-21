from typing import get_origin, get_args


class TipagemEstaticaFunction:
    """
    Decorador para checar a tipagem de entrada e saída de uma função.
    """

    def __init__(self, func):
        self.func = func
        self.annotations = func.__annotations__

    def _verificar_tipo(self, valor, tipo_esperado, nome):
        origem = get_origin(tipo_esperado)
        args_tipo = get_args(tipo_esperado)

        if origem:
            if not isinstance(valor, origem):
                raise TypeError(f"Parâmetro '{nome}' deve ser do tipo {origem.__name__}")
            if origem in (list, tuple) and args_tipo:
                for item in valor:
                    if not isinstance(item, args_tipo[0]):
                        raise TypeError(f"Itens da coleção '{nome}' devem ser do tipo {args_tipo[0].__name__}")
        else:
            if not isinstance(valor, tipo_esperado):
                raise TypeError(f"Parâmetro '{nome}' deve ser do tipo {tipo_esperado.__name__}")

    def __call__(self, *args, **kwargs):
        if not self.annotations:
            raise TypeError("A função não possui anotações de tipo.")

        param_names = [name for name in self.annotations if name != 'return']

        if len(args) != len(param_names):
            raise TypeError(f"Esperados {len(param_names)} argumentos, mas foram fornecidos {len(args)}.")

        for arg, name in zip(args, param_names):
            tipo_esperado = self.annotations[name]
            self._verificar_tipo(arg, tipo_esperado, name)

        result = self.func(*args, **kwargs)

        if 'return' in self.annotations:
            self._verificar_tipo(result, self.annotations['return'], 'return')

        return result


class TipagemEstaticaClasse:
    """
    Decorador para checar a tipagem de entrada e saída de funções e métodos de uma classe, incluindo iteradores.
    """

    def __init__(self, cls):
        self.cls = cls

    def _verificar_tipo(self, valor, tipo_esperado, nome):
        origem = get_origin(tipo_esperado)
        args_tipo = get_args(tipo_esperado)

        if origem:
            if not isinstance(valor, origem):
                raise TypeError(f"Parâmetro '{nome}' deve ser do tipo {origem.__name__}")
            if origem in (list, tuple) and args_tipo:
                for item in valor:
                    if not isinstance(item, args_tipo[0]):
                        raise TypeError(f"Itens da coleção '{nome}' devem ser do tipo {args_tipo[0].__name__}")
        else:
            if not isinstance(valor, tipo_esperado):
                raise TypeError(f"Parâmetro '{nome}' deve ser do tipo {tipo_esperado.__name__}")

    def validar_metodos(self):
        for nome, metodo in self.cls.__dict__.items():
            if callable(metodo) and hasattr(metodo, '__annotations__'):
                setattr(self.cls, nome, self.verificar_tipagem(metodo))

        if '__next__' in dir(self.cls):
            setattr(self.cls, '__next__', self.verificar_tipagem(getattr(self.cls, '__next__')))

    def verificar_tipagem(self, metodo):
        def metodo_verificado(self_or_cls, *args, **kwargs):
            annotations = metodo.__annotations__
            param_names = [name for name in annotations if name != 'return']

            for idx, name in enumerate(param_names):
                if name in kwargs:
                    valor = kwargs[name]
                elif idx < len(args):
                    valor = args[idx]
                else:
                    continue

                tipo_esperado = annotations[name]
                self._verificar_tipo(valor, tipo_esperado, name)

            resultado = metodo(self_or_cls, *args, **kwargs)

            tipo_retorno = annotations.get("return")
            if tipo_retorno:
                self._verificar_tipo(resultado, tipo_retorno, metodo.__name__)

            return resultado

        return metodo_verificado

    def __call__(self, *args, **kwargs):
        self.validar_metodos()
        return self.cls(*args, **kwargs)
