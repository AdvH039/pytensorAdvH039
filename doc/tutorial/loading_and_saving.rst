
.. _tutorial_loadsave:

==================
Loading and Saving
==================

Python's standard way of saving class instances and reloading them
is the pickle_ mechanism. Many PyTensor objects can be *serialized* (and
*deserialized*) by ``pickle``, however, a limitation of ``pickle`` is that
it does not save the code or data of a class along with the instance of
the class being serialized. As a result, reloading objects created by a
previous version of a class can be really problematic.

Thus, you will want to consider different mechanisms depending on
the amount of time you anticipate between saving and reloading.  For
short-term (such as temp files and network transfers), pickling of
the PyTensor objects or classes is possible.  For longer-term (such as
saving models from an experiment) you should not rely on pickled PyTensor
objects; we recommend loading and saving the underlying shared objects
as you would in the course of any other Python program.


.. _pickle: http://docs.python.org/library/pickle.html


The Basics of Pickling
======================

The two modules ``pickle`` and ``cPickle`` have the same functionalities, but
``cPickle``, coded in C, is much faster.

>>> from six.moves import cPickle

You can serialize (or *save*, or *pickle*) objects to a file with
``cPickle.dump``:

.. testsetup::

   my_obj = object()

>>> f = open('obj.save', 'wb')
>>> cPickle.dump(my_obj, f, protocol=cPickle.HIGHEST_PROTOCOL)
>>> f.close()

.. note::

    If you want your saved object to be stored efficiently, don't forget
    to use ``cPickle.HIGHEST_PROTOCOL``. The resulting file can be
    dozens of times smaller than with the default protocol.

.. note::

    Opening your file in binary mode (``'b'``) is required for portability
    (especially between Unix and Windows).

To de-serialize (or *load*, or *unpickle*) a pickled file, use
``cPickle.load``:

>>> f = open('obj.save', 'rb')
>>> loaded_obj = cPickle.load(f)
>>> f.close()


You can pickle several objects into the same file, and load them all (in the
same order):

.. testsetup::

   obj1 = object()
   obj2 = object()
   obj3 = object()

>>> f = open('objects.save', 'wb')
>>> for obj in [obj1, obj2, obj3]:
...     cPickle.dump(obj, f, protocol=cPickle.HIGHEST_PROTOCOL)
>>> f.close()

Then:

>>> f = open('objects.save', 'rb')
>>> loaded_objects = []
>>> for i in range(3):
...     loaded_objects.append(cPickle.load(f))
>>> f.close()

For more details about pickle's usage, see
`Python documentation <http://docs.python.org/library/pickle.html#usage>`_.


Short-Term Serialization
========================

If you are confident that the class instance you are serializing will be
deserialized by a compatible version of the code, pickling the whole model is
an adequate solution. It would be the case, for instance, if you are saving
models and reloading them during the same execution of your program, or if the
class you're saving has been really stable for a while.

You can control what pickle will save from your object, by defining a
`__getstate__
<http://docs.python.org/library/pickle.html#object.__getstate__>`_ method,
and similarly `__setstate__
<http://docs.python.org/library/pickle.html#object.__getstate__>`_.

This will be especially useful if, for instance, your model class contains a
link to the data set currently in use, that you probably don't want to pickle
along every instance of your model.

For instance, you can define functions along the lines of:

.. testcode::

    def __getstate__(self):
        state = dict(self.__dict__)
        del state['training_set']
        return state

    def __setstate__(self, d):
        self.__dict__.update(d)
        with open(self.training_set_file, 'rb') as f:
            self.training_set = cPickle.load(f)


Robust Serialization
====================

This type of serialization uses some helper functions particular to PyTensor. It
serializes the object using Python's pickling protocol, but any ``ndarray`` or
``CudaNdarray`` objects contained within the object are saved separately as NPY
files. These NPY files and the Pickled file are all saved together in single
ZIP-file.

The main advantage of this approach is that you don't even need PyTensor installed
in order to look at the values of shared variables that you pickled. You can
just load the parameters manually with `numpy`.

.. code-block:: python

    import numpy
    numpy.load('model.zip')

This approach could be beneficial if you are sharing your model with people who
might not have PyTensor installed, who are using a different Python version, or if
you are planning to save your model for a long time (in which case version
mismatches might make it difficult to unpickle objects).

See :meth:`pytensor.misc.pkl_utils.StripPickler.dump` and :meth:`pytensor.misc.pkl_utils.StripPickler.load`.


Long-Term Serialization
=======================

If the implementation of the class you want to save is quite unstable, for
instance if functions are created or removed, class members are renamed, you
should save and load only the immutable (and necessary) part of your class.

You can do that by defining __getstate__ and __setstate__ functions as above,
maybe defining the attributes you want to save, rather than the ones you
don't.

For instance, if the only parameters you want to save are a weight
matrix *W* and a bias *b*, you can define:

.. testcode::

    def __getstate__(self):
        return (self.W, self.b)

    def __setstate__(self, state):
        W, b = state
        self.W = W
        self.b = b

If at some point in time *W* is renamed to *weights* and *b* to
*bias*, the older pickled files will still be usable, if you update these
functions to reflect the change in name:

.. testcode::

    def __getstate__(self):
        return (self.weights, self.bias)

    def __setstate__(self, state):
        W, b = state
        self.weights = W
        self.bias = b

For more information on advanced use of ``pickle`` and its internals, see Python's
pickle_ documentation.
