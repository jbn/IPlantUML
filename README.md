[![Build Status](https://travis-ci.org/jbn/IPlantUML.svg?branch=master)](https://travis-ci.org/jbn/IPlantUML)

# What is it?

This Python package defines a [PlantUML](http://plantuml.com/) cell magic for
IPython. It lets you generate UML diagrams as inline SVG in your notebook. I'll
add embellishments as needed. But, for now, I just needed something that worked
and existed as a package (in pypi).

I based my code on [Steven Burke](https://github.com/sberke)'s
[plantuml gist](http://chickenbit.com/blog/2014/10/inline-plantuml-diagrams-in-ipython-notebook/).

## Installation

First, install IPlantum with pip.

```sh
pip install iplantuml
```

Then, download `plantuml.jar` and copy it to `/usr/local/bin/plantuml.jar`.

Alternatively you can set a custom path for plantuml.jar during installation

```sh
pip install iplantuml --jarpath /my/custom/path/plantuml.jar
```


## Usage

In Ipython, first,

```python
import iplantuml
```

then, create a cell like,

```
%%plantuml

@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response
@enduml
```

The output will be the generated SVG UML diagram.

By default, the magic removes the intermediate (`tmp.uml`) and target
(`tmp.svg`) files. However, if you enter a name in the `%%plantuml` line,
it retains both files of `$name.uml` and `$name.svg`. For example,

```
%%plantuml auth

@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response
@enduml
```

generates and retains `auth.uml` and `auth.svg`.
