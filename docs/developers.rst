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


Diffusion model
---------------

Config file
^^^^^^^^^^^

The config file is a json file:

.. code-block:: json

    {
        "data": "/path/to/data",
        "results": "/path/to/results",

        # Empty string means no resume
        "resume": "/path/to/resume.pt",

        # Image resolution
        "resolution": 1024,

        "unet_dim": 16,
        "unet_dim_mults": [1, 2, 4, 8],
        "timesteps": 100,

        "epochs": 100,
        "test_interval": 10,
        "batch_size": 4,
        "grad_accum": 1,
        # Number of times train set is repeated per epoch
        "train_duplicity": 1,
        "lr_start": 1e-3,
        "lr_end": 1e-6,
    }
