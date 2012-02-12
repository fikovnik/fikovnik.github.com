---
title: Observing Condor Queue with `dstat`
layout: post
---

For the experiments I do currently I need to observe the behavior of the
[Condor][condor] schedd queue while executing large workflows. What I did
usually was to use a script that would just periodically execute `condor_q` and
together with a timestamp writes the info into a file:

    {% highlight sh %}
    #!/bin/sh

    while /bin/true; do
      TS=$(date +"%d.%m.%Y-%H:%M:%S")
      CQ=$(condor_q | sed '$!d' | cut -f 3 -d ' ')

      echo $TS $CQ
      sleep 1
    done
    {% endhighlight %}

This works well, however, I usually need to correlate it with some other stats
like memory usage, system load, etc. I like to use [dstat][] for getting these
system information. It has a nice feature to export output to csv file which
can be easily read by [gnuplot][]. The problem is that one has to somehow link
the two different outputs and that can be a bit cumbersome as the execution
time of `condor_q` varies with larger number of jobs. Since dstat uses nice
plugin architecture, I decided to write a [plugin][condor-queue-dstat] that
will grab the queue info.

The usage is simple, just add `--condor-queue` flag to dstat:

    {% highlight console %}
    $ dstat --condor-queue
    ------condor-queue-----
     jobs  idle runni  held
        5     3     2     0
        5     3     2     0
        4     2     2     0
        3     1     2     0
    {% endhighlight %}

It requires to have `CONDOR_CONFIG` environment variable set and obviously
condor running. It will try to find to read the config file(s) and expand the
`BIN_DIR` variable to find path to the `condor_q`. Note, that it connects only
to the local queue. The plugin has been merged to the latest master branch of
dstat.

##Note

Executing `condor_q` can be quite expensive because `condor_schedd` has to go
over the entire jobs queue. That might take some time when there are many jobs
and it will also prevent the scheduller from doing other things so use this
with causion. 

Other way is to get the information from the `condor_collector`
using `condor_status -schedd`. The problem is that the `condor_schedd` ClassAd
is not frequently updated so the information is gotten is not very accurate.


[dstat]: https://github.com/dagwieers/dstat
[condor]: http://www.cs.wisc.edu/condor/
[gnuplot]: http://www.gnuplot.info/
[condor-queue-dstat]: https://github.com/dagwieers/dstat/blob/master/plugins/dstat_condor_queue.py
