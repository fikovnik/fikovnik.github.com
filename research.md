---
  title: Research
  layout: default
---

## Currently, I'm a PhD candidate at the [French National Centre for Scientific Research][CNRS] in the [I3S laboratory][I3S]. ##


Engineering self-adaptive systems is a particularly challenging problem. On the
one hand, it is hard to develop the right control model that drives the
adaptation; on the other hand, the implementation and integration of this
control model into the target system is a difficult and an error-prone activity.

In my research I focus on the other part, the actual development and integration
of the self-adaptive system. The main aim is to provide researchers and
engineers with a tooled approach that would help them to experiment with these
systems.

The idea is to capture the self-adaptive behavior in form of a feedback control
loops into architectural models. The main advantage of using model is that we
can then use these models as input for various tools. The models can be used to
prototype and validate new designs by translating it into some of the formal
models such as [Ptolemy][] or [Promela][]. After the model has been created and
validated it is used as the specification for the system, and the realization is
synthesized from it. The implementation code is directly generated directly from
the model by a code generator.

One of the main use cases I am using for validating this approach is modeling
adaptive behavior in [Condor][] distributed batch system. I am working on an
adaptive workflow execution, in this case maintaining high- throughput while
preventing system overload.

This work is part of the [ANR][] funded Self-Adaptive very Large disTributed sYstems ([SALTY][]) project. 

## Publications

* Filip Křikava, Philippe Collet. _On the Use of an Internal DSL for Enriching
  EMF Models_, In Proceedings of the International Workshop on OCL and Textual
  Modelling 2012 (OCL), Innsbruck, September 2012
* Filip Křikava, Philippe Collet, Robert France. _Actor-based Runtime Model of
  Adaptable Feedback Control Loops_, In Proceedings of the International
  Workshop on models@run.time 2012 (MRT), Innsbruck, September 2012
* Filip Křikava, Philippe Collet. _Using Architecture Models to Rapidly
  Prototype Feedback Control Systems_ (poster), In Proceedings of the Quatrièmes
  journées nationales du Groupement De Recherche CNRS du Génie de la
  Programmation et du Logiciel (GDR-GPL), pages 1-2, Rennes, jun 2012
* Filip Křikava, Javier Rojas Balderrama, Johan Montagnat, Philippe Collet.
  _Using Adaptation Strategies to Improve Grid Operations_ (poster), In EGI
  Technical Forum 2012, pages 1-2, sep 2012
* F. Křikava, P. Collet, _A Reflective Model for Architecting Feedback Control
  Systems_, In proceedings of the 23rd International Conference on Software
  Engineering and Knowledge Engineering (SEKE 2011), Miami, USA, July 2011,
  IEEE.
* F. Křikava, P. Collet, _Uniform and Model-Driven Engineering of Feedback
  Control Systems_, In proceedings of the 8th IEEE/ACM International Conference
  on Autonomic Computing (ICAC 2011), Karlsruhe, Germany, June 2011, ACM.
* P. Collet, F. Krikava, J. Montagnat, M. Blay-Fornarino, and D. Manset, _Issues
  And Scenarios For Self-Managing Grid Middleware_, Proceeding of the 2nd
  workshop on Grids meets autonomic computing GMAC 2010, Washington, USA, June
  2010 ACM Press.

## Teaching 
* 2012/2013: Projet de développement (Licence 3 Informatique parcours MIAGE [Polytech Nice][])
* 2012/2013: Software Engineering (M1 International at [Polytech Nice][])
* 2011/2012: Introduction to Programming using Python (both M2 Hydroprotech and
* 2010/2011: Introduction to Programming using Python (both M2 Hydroprotech and
  M2 EuroAquae at [Polytech Nice][])
  M2 EuroAquae at [Polytech Nice][])

## Other Activities 

* [Model Manipulation Using Embedded DSLs in Scala](http://www.slideshare.net/krikava/scala-workshop13) - Student talk given at [Scala Workshop 2013](http://lampwww.epfl.ch/~hmiller/scala2013/)
* [Enriching EMF Models with Scala (quick overview)](http://www.slideshare.net/krikava/enriching-emf-models-with-scala) - Presentation given at Modeling Symposium at [EclipseCon'12 Europe](http://www.eclipsecon.org/europe2012/)
* Lecturing in Super Computing and Distributed Systems Camp - [SC-CAMP][]
  * 2010 - Self Adaptive Very Large Distributed System 
  * 2011 - An Introduction to High-Throughput Computing, Condor in Action
* Collaboration with University of Wisconsin-Madison on the [Condor project][condor]


## Contact 

Laboratoire I3S  
Polytech Nice Sophia  
930 Route des Colles, BP 145  
F-06903 Sophia Antipolis Cedex  
France

[philippe]: http://www.i3s.unice.fr/~collet/
[johan]: http://www.i3s.unice.fr/~johan/
[MODALIS]: http://modalis.i3s.unice.fr/
[I3S]: http://www.i3s.unice.fr/I3S/
[CNRS]: http://www.cnrs.fr/
[ANR]: http://www.agence-nationale-recherche.fr/
[SALTY]: https://salty.unice.fr/
[Condor]: http://www.cs.wisc.edu/condor/
[SC-CAMP]: http://www.sc-camp.org/
[UNS]: http://www.unice.fr/
[Promela]: http://spinroot.com/
[Ptolemy]: http://ptolemy.eecs.berkeley.edu/ptolemyII/
[Polytech Nice]: http://www.polytech.unice.fr/