class Fraction:
    def __init__(self, numerator, denominator=1):
        def float_to_fraction(value):
            """Converte un numero float in una frazione (numeratore, denominatore)."""
            string_repr = str(value)
            if '.' in string_repr:
                decimals = len(string_repr.split('.')[1])
            else:
                decimals = 0
            scale = 10 ** decimals
            return int(value * scale), scale

        if isinstance(numerator, str):
            if '/' in numerator:
                parts = numerator.split('/')
                numerator = int(parts[0])
                denominator = int(parts[1])
            else:
                numerator = int(numerator)
                denominator = 1

        if isinstance(numerator, float):
            numerator, denom_scale = float_to_fraction(numerator)
            denominator *= denom_scale

        if isinstance(denominator, float):
            denom_num, denom_denom = float_to_fraction(denominator)
            numerator *= denom_denom
            denominator = denom_num

        if denominator == 0:
            raise ValueError("Il denominatore non può essere zero.")

        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def simplify(self):
        """Semplifica la frazione."""
        gcd = self.greatest_common_divisor(abs(self.numerator), abs(self.denominator))
        self.numerator //= gcd
        self.denominator //= gcd
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    @staticmethod
    def greatest_common_divisor(a, b):
        """Calcola il massimo comune divisore (MCD)."""
        while b:
            a, b = b, a % b
        return a

    def add(self, other):
        """Somma fra due frazioni."""
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def subtract(self, other):
        """Sottrazione fra due frazioni."""
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def multiply(self, other):
        """Moltiplicazione fra due frazioni."""
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def divide(self, other):
        """Divisione fra due frazioni."""
        if other.numerator == 0:
            raise ZeroDivisionError("Non si può dividere per zero.")
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)

    def to_decimal(self):
        """Converte la frazione in un numero decimale (float)."""
        return self.numerator / self.denominator

    def __str__(self):
        """Converte la frazione in una stringa (numeratore/denominatore)."""
        if self.denominator == 1:
            return str(self.numerator)
        return str(self.numerator) + "/" + str(self.denominator)

# Funzione per l'iterazione del metodo del simplesso
def iterazione_tableau_simplesso(T):
    N = len(T[0])
    M = len(T)
    K = 0
    S = 0
    T2 = [[0 for _ in range(N)] for _ in range(M)]

    # Verifica ottimalità
    stop = True
    for j in range(0, N-1):
        if T[M-1][j].to_decimal() < 0:
            if stop:
                K = j
            stop = False
    if stop:
        return T, True, False

    # Verifica illimitatezza
    min_fraction = Fraction(-1)
    stop = True
    itemp = 0
    for i in range(0, M-1):
        if T[i][K].to_decimal() > 0:
            stop = False
            S = i
            min_fraction = T[S][N-1].divide(T[S][K])
            itemp = i
            break

    if stop:
        return T, False, True

    for i in range(itemp, M-1):
        if T[i][K].to_decimal() > 0:
            min_temp = T[i][N-1].divide(T[i][K])
            if min_temp.to_decimal() < min_fraction.to_decimal():
                min_fraction = min_temp
                S = i

    # Calcolo della nuova tabella
    vPivot = T[S][K]
    for j in range(0, N):
        T2[S][j] = T[S][j].divide(vPivot)

    for i in range(0, M):
        if i != S:
            for j in range(0, N):
                T2[i][j] = T[i][j].subtract(T[i][K].multiply(T2[S][j]))

    return T2, False, False

#MAIN 
# Lettura input
N = int(input("N: "))
M = int(input("M: "))
A = [[0 for _ in range(N)] for _ in range(M)]

for i in range(M):
    for j in range(N):
        A[i][j] = Fraction(input("T"+ str(i+1)+str(j+1)+": "))

ottimo = False
illimitato = False
i = 1
while not ottimo and not illimitato:
    A, ottimo, illimitato = iterazione_tableau_simplesso(A)
    if not ottimo and not illimitato:
        print("Iterazione n: " + str(i))
        i += 1
        for row in A:
            print([str(fraction) for fraction in row])
