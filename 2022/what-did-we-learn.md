# What did we learn from this?

## Day 1

We can't pass a stream by value to a function (which makes sense, I guess).
My first attempt around this was to pass a pointer to the stream, but that's C,
not C++. Instead I should have the function take a reference to the stream,
then I can pass everything around pretending I have the value.

In part 1 I learned that I really don't know how to do the equivalent of a list
transformation or map call in C++. There's something called std::transform but
reading its documentation makes my eyes glaze over.

auto is nice.
