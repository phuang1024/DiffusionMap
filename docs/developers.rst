Developers
==========

Details for developers.

Texture file structure
----------------------

ML model training data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    data
    |__ AssetName001
        |__ color.jpg
        |__ displacement.jpg
        |__ roughness.jpg
    ...

Global catalog
^^^^^^^^^^^^^^

e.g. ``/path/to/Catalog/``

.. code-block::

    data
    |__ AssetName001
        |__ 1         # 1K resolution
            |__ AssetName001_1K-JPG_Color.jpg
            ...
        ...

Project catalog
^^^^^^^^^^^^^^^

e.g. ``/project/Textures/``

.. code-block::

    data
    |__ AssetName001_1K
        |__ AssetName001_1K-JPG_Color.jpg
        ...
