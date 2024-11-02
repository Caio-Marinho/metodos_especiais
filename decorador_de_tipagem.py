class TipagemEstaticaFunction:
    """
    Formato para checar a tipagem de entrada e saída de uma função.
    """

    def __init__(self, func):
        self.func = func
        self.annotations = func.__annotations__

    def __call__(self, *args, **kwargs):
        if not self.annotations:
            raise TypeError("A função não possui anotações de tipo.")

        # Verifica o número de argumentos esperados
        expected_args = len(self.annotations) - 1  # Desconsidera 'return' se presente
        if len(args) != expected_args:
            raise TypeError(f"Esperados {expected_args} tipos de dados, mas foram fornecidos {len(args)}.")

        # Verificar tipos dos argumentos
        for arg, (name, tipo) in zip(args, self.annotations.items()):
            if name != 'return' and not isinstance(arg, tipo):
                raise TypeError(f"Argumento '{name}' deve ser do tipo {tipo.__name__}")

        # Chama a função original
        result = self.func(*args, **kwargs)

        # Verifica o tipo de retorno
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
        Intercepta todos os métodos da classe que possuem anotações de tipo e adiciona verificação de tipo.
        """
        for nome, metodo in self.cls.__dict__.items():
            if callable(metodo) and hasattr(metodo, '__annotations__'):
                # Substitui o método pela versão com verificação de tipo
                setattr(self.cls, nome, self.verificar_tipagem(metodo))

        # Verificar se a classe implementa um iterador e adicionar verificação de tipo para o método __next__
        if '__next__' in dir(self.cls):
            setattr(self.cls, '__next__', self.verificar_tipagem(self.cls.__next__))

    @staticmethod
    def verificar_tipagem(metodo):
        """
        Decora um método para verificar a tipagem dos parâmetros de entrada e do retorno.
        """

        def metodo_verificado(instance, *args, **kwargs):
            # Verificar tipos dos argumentos
            annotations = metodo.__annotations__
            for nome_param, tipo_param in annotations.items():
                if nome_param != "return":  # Ignorar anotação de retorno para argumentos
                    valor = kwargs.get(nome_param) if nome_param in kwargs else None
                    if not valor:
                        valor = args[list(annotations.keys()).index(nome_param)]  # Desconta 'self'
                    if not isinstance(valor, tipo_param):
                        raise TypeError(f"Parâmetro '{nome_param}' deve ser do tipo {tipo_param.__name__}")

            # Chamar o método original e capturar o resultado
            resultado = metodo(instance, *args, **kwargs)

            # Verificar o tipo de retorno
            tipo_retorno = annotations.get("return")
            if tipo_retorno and not isinstance(resultado, tipo_retorno):
                raise TypeError(f"Retorno do método '{metodo.__name__}' deve ser do tipo {tipo_retorno.__name__}")

            return resultado

        return metodo_verificado

    def __call__(self, *args, **kwargs):
        # Inicializa a instância da classe decorada
        self.validar_metodos()
        instance = self.cls(*args, **kwargs)
        return instance
