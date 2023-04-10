# Pipestream

## Usage

Pipestream provides a convenient way to "pipe" a given input through a series of classes or callable, giving each class the opportunity to inspect or modify the input and invoke the next callable in the pipeline:

```python
from pipestream import Pipeline


def sum_one(value, next):
    return next(value + 1)


def multiply_by_two(value, next):
    return next(value * 2)


Pipeline
    .send(1)
    .through(
        sum_one,
        multiply_by_two
    )
    .then(print)

# output: 4
```

As you can see, each invokable class or closure in the pipeline is provided the input and a `next` closure. Invoking the `next` closure will invoke the next callable in the pipeline. As you may have noticed, this is very similar to middleware and [chain of responsability pattern](https://refactoring.guru/design-patterns/chain-of-responsibility).

When the last callable in the pipeline invokes the `next` closure, the callable provided to the then method will be invoked. Typically, this callable will simply return the given input.

Of course, as discussed previously, you are not limited to providing functions to your pipeline. You may also provide classes with common method's between them. If a class is provided, the class method will be accessed by python std method `getattr`.

```python
from pipestream import Pipeline


user = Pipeline
    .send(user)
    .through(
        GenerateProfilePhoto,
        ActivateSubscription,
        SendWelcomeEmail
    )
    .via('do')
    .then(lambda value: value)
```

## Install
```sh
$ pip install pipestream
 ```

## Running tests
```sh
$ pytest tests/
```

This package is inspired by [Laravel's Pipeline Helper](https://laravel.com/docs/10.x/helpers#pipeline)