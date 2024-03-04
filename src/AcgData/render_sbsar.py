__all__ = (
    "render_sbsar",
)

import random
from subprocess import Popen

from tqdm import trange


def render_sbsar(args):
    pbar = trange(args.count)
    for i in pbar:
        sbsar = random.choice(list(args.input.glob("*.sbsar")))
        output = args.output / f"{sbsar.stem}_{i:03d}"

        pbar.set_description(f"Rendering {sbsar.name} to {output.name}")

        p = Popen([
            "sbsrender",
            sbsar,
            "--output-name", output,
        ])
        p.wait()
