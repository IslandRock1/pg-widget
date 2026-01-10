
# py-widget

A simple library to create UI elements in python, based on PyGame. This library implements various UI elements like buttons and sliders.

It's meant to be very easy to use, requiring very little technical skills. So, should you use it? Probably not.. Even simple visualizations takes many milliseconds to render, it's a bit buggy, and i make no promises to avoid breaking changes.

## TODO

There are many improvements i want to make to this library. First on the list is probably adding support for changing UI elements at runtime. Aka, when right-clicking, open a settings-box.

* Circular slider/progressbar
* Easier for UI components to use keyboard presses.
* onHover function, to let elements react when the mouse is over them.
* Settings at runtime
* Better padding (.inBorder works.. but idk)

## Usage

To use the library, simply do ``` pip install git+https://github.com/IslandRock1/py-widget.git@v0.1.0-alpha```.
Then in your code the library can be imported like this: ````import pg_widgets as pw````. Examples can be found in the tests directory.

## Showcase

The simple examples in the tests directory gives these visualizations. (Sorry for the ugly colors, i know nothing about UI.. these can easily be changed!)

### tests/completeSuite.py

![completeSuite.py](images/completeSuite.png)

### tests/tabs.py

![tabs1](images/tabsTab1.png)
![tabs2](images/tabsTab2.png)