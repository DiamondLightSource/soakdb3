from importlib.metadata import version

__version__ = version("soakdb3")
del version

__all__ = ["__version__"]
