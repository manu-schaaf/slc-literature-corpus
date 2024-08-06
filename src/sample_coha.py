from argparse import ArgumentParser
from pathlib import Path

from tqdm import tqdm

from parse.utils import sample_from_conllu

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "paths",
        type=Path,
        nargs="+",
        metavar="[INPUT_DIR ...] OUTPUT_DIR",
        help="Input directories containing CoNLL-U files and a single output directory for sampled CoNLL-U files. Input paths must be directories. Output directory will be create if it does not exist.",
    )

    parser.add_argument(
        "-k",
        "--num_sentences",
        type=int,
        default=450,
        help="Number of sentences to sample from each input directory. Default: 450.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help=(
            "Seed for random sampling. "
            "All input files will be shuffled with this seed. "
            "Default: 42."
        ),
    )

    parser.add_argument(
        "--group",
        type=str,
        default=r".*\/text_(?P<a_prefix>[^_]+)_(?P<b_date>\d{4}).*",
    )
    parser.add_argument(
        "--group-exhaustive",
        action="store_true",
        help="Require all files to match the group pattern. Default: False.",
    )

    parser.add_argument(
        "--lengths",
        type=int,
        nargs="+",
        default=[5, 10, 15, 20, 30, 40, 50, 60, 70],
    )
    parser.add_argument(
        "--period",
        type=int,
        default=3,
    )

    args = parser.parse_args()

    in_paths, out_path = args.paths[:-1], args.paths[-1]

    for in_path in in_paths:
        if not in_path.is_dir():
            raise NotADirectoryError(f"Input path is not a directory: {in_path}")

    if not out_path.exists():
        out_path.mkdir(parents=True, exist_ok=True)
    elif not out_path.is_dir():
        raise NotADirectoryError(
            f"Output path exists, but is not a directory: {out_path}"
        )

    for folder in tqdm(in_paths, "Sampling", smoothing=0):
        sample_from_conllu(
            folder=folder,
            out=out_path,
            k=args.num_sentences,
            seed=args.seed,
            lengths=args.lengths,
            period=args.period,
            group_by_regex=args.group,
            group_all_match=args.group_exhaustive,
        )