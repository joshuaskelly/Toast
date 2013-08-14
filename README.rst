
Toast
=====

Version: 0.2.0 - Release August 13th, 2013

By Joshua Skelton

Toast is a package/framework/thing for Python built on top of Pygame. It provides many handy classes for making 16-bit style games and is easy to learn and extend.

Requirements
------------

Games created with Toast require `python <http://python.org/>`_ and `pygame <http://pygame.org/>`_.


Features
--------

Toast was intially born as a test bed for ideas rattling around in my head that needed to get out. It has evolved to provide classes and data structures to enable you to focus on making a game and not technology.

Toast fully or partially supports the following features:

- Cameras

  Support for multiple cameras, and scaling/zooming.
  
- Components

  Component are attached to game objects to implement various behaviors. Multiple components can be attached to compose complex behaviors.
  
- Events

  Broadcast and listen for events. Event messages contain a dictionary of user defined data.
  
- Game Objects

  Game objects can represent anything in the scene. Equivalent to an Entity/Actor class in other frameworks.
  
- Resource Management

  Load something, load it once, and use it anywhere.
  
- Scene

  Scenes are a hierarchical logical container for everything that exists in your game. 
  
- Sprites

  A basic game object that is capable of rendering an image within the scene.

Contributing
------------

Toast is still very much under development, I wanted to get it out into your hands as quickly as possible.

If you would like to see a particular feature, need a bug fixed, or made something cool, let me know!

Bugs
----

Please add them to the `issue tracker <https://github.com/JSkelly/Toast/issues/new>`_ with as much information as you can provide.
