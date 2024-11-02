class range:
    def __init__(self, start: int, stop: int | None = None, step: int = 1, incluir: bool | int = False) -> None:
        """
        Inicializa um objeto `range`, que gera uma sequência de números, semelhante ao
        `range` embutido do Python, mas com uma opção para incluir o valor final.

        Args: start (int): Valor inicial do intervalo.
        Args: stop (int | None): Valor final do intervalo. Se None,
        `start` é considerado o valor final e `start` é ajustado para 0.
        Args: step (int): Incremento entre os valores do intervalo. Padrão é 1.
        Args: incluir (bool): Se True, o valor final (`stop`) é incluído no
        intervalo. Se apenas `start` for passado, `start` é ajustado para 1.
        """
        # Define `start` como 0 e `stop` como o valor de `start`
        self.start = 0 if stop is None else start
        self.stop = start if stop is None else stop
        # Se `incluir` for True, começa a partir de 1
        if incluir:
            self.start = start if self.start else 1
        self.step = step if self.start < self.stop else -1 if self.stop < self.start else 1
        # Define o incremento entre os valores do intervalo
        self.atual = self.start  # Define o valor atual no início do intervalo
        self.incluir = incluir  # Define se `stop` deve ser incluído no intervalo

    def __iter__(self) -> 'range':
        """
        Retorna o próprio objeto `Range` como um iterador, reiniciando o valor atual.

        Returns:
            range: O próprio objeto `range` para iteração.
        """
        self.atual = self.start  # Reinicia o iterador a partir do valor inicial
        return self

    def __next__(self) -> int:
        """
        Retorna o próximo valor no intervalo definido pelo objeto `Range`.

        Returns:
            int: O próximo valor no intervalo.

        Raises:
            StopIteration: Quando o final do intervalo é atingido.
        """
        atual = self.atual
        # Verifica a condição de parada com base na direção do `step`

        if self.step > 0:
            # Condições de parada: define se inclui `stop` com base no valor de `incluir`
            # Para contagem crescente
            incluir = self.incluir and self.atual <= self.stop
            comum = not self.incluir and self.atual < self.stop
        else:
            # Para contagem decrescente
            incluir = self.incluir and self.atual >= self.stop
            comum = not self.incluir and self.atual > self.stop
        if incluir or comum:
            # Avança o valor atual para o próximo elemento no intervalo
            self.atual += self.step
            return atual
        else:
            # Levanta a exceção para sinalizar o fim da iteração
            raise StopIteration
