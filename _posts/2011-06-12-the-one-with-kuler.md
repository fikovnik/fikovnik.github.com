---
  title: The One With Kuler
  layout: post
---

## Introduction

Last week I was working on poster for the [ICAC'11][] conference.  I'm far from
being a graphical designer, but I really like designing posters. The scientific
ones are not that much of a "fun", but still more enjoyable then just plain
writing. I decided to use [OmniGraffle][] which together with [LaTeXiT][] I
consider to be the turning point to switch to Mac (if only other software was
that useful). After getting some inspiration from the [Scientific Poster
Design][inspiration1] presentation by the Cornell University and plenty of other
from my [favorite source][inspiration2] as well as plenty of comments from my
advisor I came up with this:

![Kuler](SASSRelatedWorkOverviewimages/journal/the-one-with-kuler/original.png "Original")

Yeah, the biggest problem is the color scheme, isn't it :) That one definitely
had to be improved. A [color scheme][] is simply an aesthetic combination of
colors that goes together nicely. There are quite a few ways how you create one,
however, most of the time, some logical combination of colors from a [color
wheel][] is used. I remembered that some time ago a friend of mine showed me a
nice utility for creating such color schemes - a [color scheme designer][]. I
started playing with it, but after a while I found three things:

1. it is hard to come up with a good looking colors, 

1. the harder it is to come up with good looking colors, the more painful my
   hand is from the constant clicking of changing colors, and

1. there is no way how one can easily type in the standard OSX color picker a
   hex color like `#ff1300`.

I remember encountering the last problem already so I decided this time instead
of converting hex to decimal, find some way how to do it easily (_on Mac there
must be one, right?_).

## Approach

I have never realized that the OSX color picker is a actually a wrapper for set
of plugins so as google pointed me to [Robin Wood post][] I was pretty amazed.
Not only I found what I was looking for - a [hex color picker][], but more
importantly,I found something that looked that is designed for color schemes:
[Mondrianum 2][].

Mondrianum is a color picker that downloads color schemes from [Adobe Kuler][]
and makes them accessible right from the color picker. Kuler is web application,
well rather a platfom, for creating and more importantly sharing color schemes.
You can list them sorted by popularity or rating so it looked like my first
point just got solved.

The last thing that remains is the pain in the arm from the constant clicking
(_after trying out few, the magic mouse proved not to be that magical after
all_). What would be great is to have a way how to automatize this:

1. annotate the shapes in OmniGraffle that should be filled with different
   colors,
1. download one or more color scheme from Kuler, and
1. apply each permutation of the scheme and export it to PDF.

Let's see if we can address it:

1. To annotate shapes, one can use the note properties that can be found in the
   object inspector. A note can have data key/value pairs which are just
   strings. This be used to tag which shapes should have which colors:

1. Kuler has a simple [API][kuler-api] in form of a RSS feed.

1. OmniGraffle has quite an extensive AppleScript API. I have already written an
   utility about exporting OmniGraffle canvases into PDF (and others) so the
   only things remaining was to find out how to get a [list of shapes][] with
   the notes and [change fill colors][].

## Implementation

Almost there, the last thing is to put all of this together. I don't like (know)
AppleScript so I used Python [appscript][] library instead:

Import appscript module:

    {% highlight python %}
    >>> from appscript import *
    {% endhighlight %}

Load the OmniGraffle document:

    {% highlight python %}
    >>> og = app('OmniGraffle Professional 5.app') # the application handler
    >>> og.documents() # all currently opened documents - I have only one
    [app(u'/Applications/OmniGraffle Professional 5.app').documents[u'poster.graffle']]
    >>> doc = og.documents()[0]
    {% endhighlight %}

Get the canvas:

    {% highlight python %}
     >>> doc.canvases() # all canvases - I have only one
    [app(u'/Applications/OmniGraffle Professional 5.app').documents[u'poster.graffle'].canvases.ID(1)]
    >>> canvas = doc.canvases()[0]
    {% endhighlight %}

Get shapes from the canvas:

    {% highlight python %}
    >>> shapes = canvas.shapes()
    >>> shapes
    [app(u'/Applications/OmniGraffle Professional 5.app').documents[u'poster.graffle'].canvases.ID(1).graphics.ID(12661),
    ...
    ...
    app(u'/Applications/OmniGraffle Professional 5.app').documents[u'poster.graffle'].canvases.ID(1).graphics.ID(12404)]
    >>> len(shapes)
    165
    {% endhighlight %}

Now the variable `shapes` contains all the shapes, but in fact, we are only
interested in the ones that contains the annotations. We can find these when we
look at their `properties()`:

    {% highlight python %}
    >>> shapes[0].properties()
    {k.shadow_color: (0, 0, 0), k.stroke_join: k.round, k.layer: app(u'/Applications/OmniGraffle Professional 5.app').documents[u'poster.graffle'].canvases.ID(1).layers[2], k.fill_color: (65535, 65535, 65535), k.magnets: [],
    ...
    ...
    k.url: k.missing_value, k.notes: k.missing_value, k.text_placement: k.center, k.draws_shadow: False, k.shadow_vector: k.missing_value, k.vertical_padding: 5, k.arrow_width: 0.0, k.textRotation: 0.0}
    {% endhighlight %}

The right key in the properties dictionary is `k.user_data`:

    {% highlight python %}
    >>> shapes[0].properties()[k.user_data]
    k.missing_value
    {% endhighlight %}

So we filter all the shapes to include only the ones that have non empty
`user_data`:

    {% highlight python %}
    >>> shapes = [(s, s.properties()[k.user_data]) for s in shapes if s.properties()[k.user_data] != k.missing_value]
    >>> len(shapes)
    18
    >>> shapes[0]
    (app(u'/Applications/OmniGraffle Professional 5.app').documents[u'poster.graffle'].canvases.ID(1).graphics.ID(11595), {u'bgcolor': u'color3'})
    {% endhighlight %}

I also changed the data structure to contain a tuple with shape instance and the
dictionary with the user data.

Now we need to get some Kuler theme. In order to simplify that I made a small
module called [pykuler][]. It's usage is super simple:

    {% highlight python %}
    >>> from kuler import *
    >>> k = Kuler('****YOUR API KEY****')
    >>> theme = k.list().next()
    {% endhighlight %}

The `k.list()` actually returns a generator, that's why the `next()` call.

    {% highlight python %}
    >>> print theme
    Theme: 23615 (Tech Office)
    {% endhighlight %}

The colors in a theme are stored as a tuple in the `colors` property. We need
the 16 bit RGB representation for OmniGraffe:

    {% highlight python %}
    >> theme.colors[0].asRGB16()
    (22784, 20992, 16640)
    {% endhighlight %}

For convenience I will use this data structure for defining the colors tags - a
dictionary containing a `Color` instance for each color tag:

    {% highlight python %}
    >>> colors = dict(zip(['color%d' % i for i in range(5)],theme.colors))
    {% endhighlight %}

Finally, we just run a loop over all the shapes and style them approprietly:

    {% highlight python %}
    >>> for shape, styles in shapes:
    ...    shape.fill_color.set([c for c in colors[styles['bgcolor']].asRGB16()])
    {% endhighlight %}

OK, the good news is that is works as you can see below,

![Kuler](SASSRelatedWorkOverviewimages/journal/the-one-with-kuler/first-run.png "First run")

however, it obviously needs to run in a loop :)

## Experimental Results

The complete code I used is available [here][final-code]. I liked the most [Tech
Office][tech-office] so following is the result if you run the script like:

    {% highlight sh %}
    ./style.py poster.graffle ICAC ****YOUR API KEY**** tech-office 23615
    {% endhighlight %}

[![Kuler](SASSRelatedWorkOverviewimages/journal/the-one-with-kuler/results.png "Results")](/canape/images/journal/the-one-with-kuler/results-big.png)

## Conclusion

One approach of finding a good theme will be to just get say 50 most popular
Kuler schemes, but that would take a while and generate too many PDFs (50 * 5! =
6000). Also my laptop was about to explode during the process. What is better is
to just browse Kuler manually and only process the one that are to one's
linking. I guess after going through 6000 images it will be my head what will
explode. The running time can be cut quite a lot using a simple heuristics like
discarding permutations that have too dark color for various color tags.

## PS

This is the final version:

![Kuler](SASSRelatedWorkOverviewimages/journal/the-one-with-kuler/final.png "Finalist")

Happy kulering!

![Kuler](SASSRelatedWorkOverviewimages/journal/the-one-with-kuler/kuler.png "Kuler logo")

[ICAC'11]: http://www.cis.fiu.edu/conferences/icac2011/
[pykuler]: https://github.com/fikovnik/pykuler
[final-code]: https://gist.github.com/1025915
[tech-office]: http://kuler.adobe.com/#themeID/23615
[appscript]: http://appscript.sourceforge.net/
[kuler-api]: http://learn.adobe.com/wiki/display/kulerdev/B.+Feeds
[Adobe Kuler]: http://kuler.adobe.com/
[list of shapes]: http://forums.omnigroup.com/showthread.php?t=18144
[change fill colors]: http://forums.omnigroup.com/showthread.php?t=899
[Mondrianum 2]: http://www.lithoglyph.com/mondrianum/
[hex color picker]: http://wafflesoftware.net/hexpicker/
[Robin Wood post]: http://www.robinwood.com/Catalog/Technical/OtherTuts/MacColorPicker/MacColorPicker.html
[color scheme]: http://en.wikipedia.org/wiki/Color_scheme
[color wheel]: http://en.wikipedia.org/wiki/Color_wheel
[color scheme designer]: http://colorschemedesigner.com/
[OmniGraffle]: http://www.omnigroup.com/products/omnigraffle/
[LaTeXiT]: http://www.chachatelier.fr/latexit/latexit-home.php?lang=en
[inspiration1]: http://www.cns.cornell.edu/documents/ScientificPosters.pdf
[inspiration2]: http://images.google.com/search?tbm=isch&hl=en&source=hp&biw=1116&bih=929&q=scientific+poster&gbv=2&oq=scientific+poster&aq=f&aqi=g10&aql=&gs_sm=e&gs_upl=730l5931l0l19l16l1l3l4l0l610l2424l0.5.4.5-1
