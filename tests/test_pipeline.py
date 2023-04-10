from __future__ import absolute_import

from ..pipestream import Pipeline


class PipeTest:

    def do(stack, next):
        return next(stack)


class TestPipeline:

    def test_can_use_func_as_pipe(self):
        pipe = Pipeline.send(1).through(lambda v, n: n(v))

        assert len(pipe.pipes) == 1

    def test_can_use_class_as_pipe(self):
        pipe = Pipeline.send(1).through(PipeTest).via('do')

        assert pipe._method != 'handle'
        assert pipe._method == 'do'

    def test_can_run_pipes_then_return(self):
        def sum_plus_one(value, next): return next(value + 1)
        pipe = Pipeline.send(1).through(sum_plus_one).then_return()

        assert pipe == 2

    def test_can_run_pipes_then_call_destination(self):
        def sum_plus_one(value, next): return next(value + 1)
        def multiply_by_two(value): return value * 2

        pipe = Pipeline.send(1).through(sum_plus_one).then(multiply_by_two)

        assert pipe == 4
