from __future__ import annotations

import inspect
from functools import reduce
from typing import Tuple, Type


class Pipeline:

    # The list of class/callable pipes
    pipes: list = []

    # The object being passed through the pipeline.
    _passable: any

    # The method to call on each pipe if a class instance if passed as pipe
    _method: str

    def __init__(self, passable: any, method: str = 'handle'):
        self._passable = passable
        self._method = method

    @staticmethod
    def send(passable: any, method: str = 'handle') -> Type[Pipeline]:
        """Set the object being sent through the pipeline."""
        return Pipeline(passable, method)

    def through(self, *pipes: Tuple[callable]) -> Type[Pipeline]:
        """Set the list of pipes."""
        self.pipes = list(pipes)
        return self

    def via(self, method: str) -> Type[Pipeline]:
        """Set the method to call on the pipe."""
        self._method = method
        return self

    def then(self, destination: callable) -> any:
        """Run the pipeline with a final destination callback."""
        pipeline = reduce(self._carry(), self.pipes,
                          self._prepare_destination(destination))
        return pipeline(self._passable)

    def then_return(self) -> any:
        """Run the pipeline and return the result."""
        return self.then(lambda passable: passable)

    def _prepare_destination(self, destination: callable) -> callable:
        """Get the final piece of the Closure onion."""
        def _destination(passable):
            try:
                return destination(passable)
            except Exception as e:
                return self.handle_exception(passable, e)
        return _destination

    def _carry(self) -> callable:
        """Get a Closure that represents a slice of the application onion."""
        def inner(stack, pipe):
            def _pipe(passable):
                nonlocal pipe
                try:
                    if inspect.isclass(pipe):
                        return getattr(pipe, self._method)(passable, stack)

                    return pipe(passable, stack)
                except Exception as e:
                    return self.handle_exception(passable, e)
            return _pipe
        return inner

    def handle_exception(self, passable, e):
        raise e
