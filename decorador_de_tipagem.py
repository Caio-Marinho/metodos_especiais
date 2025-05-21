class TipagemEstaticaFunction:
    """
    Decorador para checar a tipagem de entrada e saída de uma função.
    """

    def __init__(self, func):
        self.func = func
        self.annotations = func.__annotations__

    def __call__(self, *args, **kwargs):
        if not self.annotations:
            raise TypeError("A função não possui anotações de tipo.")

        # Extrai os nomes dos parâmetros esperados (exceto 'return')
        param_names = [name for name in self.annotations if name != 'return']

        if len(args) != len(param_names):
            raise TypeError(f"Esperados {len(param_names)} argumentos, mas foram fornecidos {len(args)}.")

        for arg, name in zip(args, param_names):
            expected_type = self.annotations[name]
            if not isinstance(arg, expected_type):
                raise TypeError(f"Argumento '{name}' deve ser do tipo {expected_type.__name__}")

        result = self.func(*args, **kwargs)

        if 'return' in self.annotations and not isinstance(result, self.annotations['return']):
            raise TypeError(f"Retorno deve ser do tipo {self.annotations['return'].__name__}")

        return result


class TipagemEstaticaClasse:
    """
    Decorador para checar a tipagem de entrada e saída de funções e métodos de uma classe, incluindo iteradores.
    """

    def __init__(self, cls):
        self.cls = cls

    def validar_metodos(self):
        """
        Adiciona verificação de tipo a todos os métodos da classe com anotações.
        """
        for nome, metodo in self.cls.__dict__.items():
            if callable(metodo) and hasattr(metodo, '__annotations__'):
                setattr(self.cls, nome, self.verificar_tipagem(metodo))

        # Trata __next__ se for um iterador
        if '__next__' in dir(self.cls):
            setattr(self.cls, '__next__', self.verificar_tipagem(getattr(self.cls, '__next__')))

    @staticmethod
    def verificar_tipagem(metodo):
        """
        Envolve o método para verificar os tipos de entrada e saída.
        """

        def metodo_verificado(self_or_cls, *args, **kwargs):
            annotations = metodo.__annotations__
            param_names = [name for name in annotations if name != 'return']

            for idx, name in enumerate(param_names):
                # Tenta buscar em kwargs, senão usa args pela ordem
                if name in kwargs:
                    valor = kwargs[name]
                elif idx < len(args):
                    valor = args[idx]
                else:
                    continue  # Pode ser parâmetro opcional, deixar para o Python lançar erro

                expected_type = annotations[name]
                if not isinstance(valor, expected_type):
                    raise TypeError(f"Parâmetro '{name}' deve ser do tipo {expected_type.__name__}")

            resultado = metodo(self_or_cls, *args, **kwargs)

            tipo_retorno = annotations.get("return")
            if tipo_retorno and not isinstance(resultado, tipo_retorno):
                raise TypeError(f"Retorno do método '{metodo.__name__}' deve ser do tipo {tipo_retorno.__name__}")

            return resultado

        return metodo_verificado

    def __call__(self, *args, **kwargs):
        self.validar_metodos()
        return self.cls(*args, **kwargs)
