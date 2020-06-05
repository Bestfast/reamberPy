# Reamber (Py)

`pip install reamber`

This is a simple package to handle VSRG file, useful if you'd want to manipulate data
such as offset, column, bpm, etc.

This doesn't provide complex algorithms, only the base dataclasses and helpful basic
algorithms

# Wiki

[Visit the wiki for more info](https://github.com/Eve-ning/reamber_base_py/wiki)

# Info

## Motivation

A growing amount of osu!mania players are becoming interested in programming.
The best way to learn is to relate it to something that you're familiar with.
That's why I'm making a library for most common VSRG (Vertical Scrolling Rhythm Game)
types.

## WIIFY (What's in it for you)

### Picking it up

Everything is in `Python`, a very easy to pick up language. Installing it is as easy as:

1. Installing `pip`
2. Run `pip install reamber`

### Easy Typing

The library heavily focuses on `Typing` for explicit returns and arguments.
This is at an expense of slower processing speed.

I recommend using `PyCharm` or any other python editor that supports hinting.
Hinting is where the editor hints you available functions, variables, etc.

### Piping

Inspired by `R Lang` `%>%` operator.

Piping is the act of chaining multiple functions together.

```
# Grabbing the notes in between 1s and 2s in columns 1 and 3

# Without Piping
Notes(Notes(notes.after(1000)).before(2000)).inColumns([1, 3])

# With Piping
notes.after(1000).before(2000).inColumns([1, 3]).data()
```

This library supports it, to retrieve the list, just call `.data()`

### List, Pandas Support

This library also supports exporting multiple classes as a `list` or `pandas.DataFrame`
via `.data()` and `.df()` respectively.

So you don't need to feel limited to just the current interfaces.

## Examples

Load in a osu! map

Grab the sorted holds in columns 1 & 2 in between 1s and 2s as a list
```python
from reamber.osu.OsuMapObject import OsuMapObject

m = OsuMapObject()
m.readFile("map.osu")
print(m.notes.holds.sorted().inColumns([1, 2]).between(1000, 2000, includeEnds=False).data())
```
Load in a Quaver map

Grab the SV multiplier values as a list
```python
from reamber.quaver.QuaMapObject import QuaMapObject

m = QuaMapObject()
m.readFile("map.qua")
print(m.svs.multipliers())
```