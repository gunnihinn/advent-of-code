# What did we learn from this?

## Day 3

I'm maybe doing too much work in the `parse` function. Whatever I do there ends
up being tailored to part 1, and if part 2 holds the data in a different way I
have to contort to make do.

I also don't know how set intersections work. I was convinced that

```
    A \cap B \cap C = (A \cup B) \cap C
```

but that gave the wrong answer for part 2.

## Day 2

I had a bug where I wrote

```
if (a = b)
```

and the compiler didn't bat an eye, even with warnings and errors set to
complain about everything.

## Day 1

We can't pass a stream by value to a function (which makes sense, I guess).
My first attempt around this was to pass a pointer to the stream, but that's C,
not C++. Instead I should have the function take a reference to the stream,
then I can pass everything around pretending I have the value.

In part 1 I learned that I really don't know how to do the equivalent of a list
transformation or map call in C++. There's something called std::transform but
reading its documentation makes my eyes glaze over.

auto is nice.
