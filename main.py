from abc import ABCMeta, abstractmethod

# Interpolation
class Interpolation:
    __metaclass__ = ABCMeta

    # PROPERTIES

    @abstractproperty
    def N(self):
        pass

    @abstractproperty
    def a(self):
        pass

    @abstractproperty
    def b(self):
        pass

    # METHODS

    @abstractmethod
    def Function(self):
        pass

    @abstractmethod
    def InterpolationPolynomiale(self):
        pass

    @abstractmethod
    def InterpolationContinue(self):
        pass

    @abstractmethod
    def InterpolationSpline(self):
        pass

    @abstractmethod
    def CalculErreur(self):
        pass

# InterpolationUnidimensionnele
class InterpolationUnidimensionnele(Interpolation):
    def InterpolationPolynomiale(self):
        pass

    def InterpolationContinue(self):
        pass

    def InterpolationSpline(self):
        pass

# InterpolationBidimensionnele
class InterpolationBidimensionnele(Interpolation):
	def InterpolationPolynomiale(self):
        pass

    def InterpolationContinue(self):
        pass

    def InterpolationSpline(self):
        pass


def main():
	pass


if __name__ == "__main__":
    main()