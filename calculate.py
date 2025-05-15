import os
import json
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", type=str, default="")
args = parser.parse_args()

root_dir = args.root_dir
fold_dirs = [f"fold_{i}" for i in range(5)]

fp_volumes = []
fn_volumes = []
dice_scores = []

output_lines = []

for fold in fold_dirs:
    fold_path = os.path.join(root_dir, fold)
    if not os.path.isdir(fold_path):
        continue

    for file in os.listdir(fold_path):
        if file.endswith(".json"):
            file_path = os.path.join(fold_path, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    fp = data["fn_fp_metrics"]["fp_volume"]
                    fn = data["fn_fp_metrics"]["fn_volume"]
                    dice = data["average_metrics"]["region"]["Dice"]

                    fp_volumes.append(fp)
                    fn_volumes.append(fn)
                    dice_scores.append(dice)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")


summary = (
    f"FP: {fp_volumes}\n"
    f"FN: {fn_volumes}\n"
    f"Dice: {dice_scores}\n"
    f"\n\n3-digit mean:"
    f"\n\nMean FP: {np.mean(fp_volumes):.3f}\n"
    f"Mean FN: {np.mean(fn_volumes):.3f}\n"
    f"Mean Dice: {np.mean(dice_scores):.3f}"
    f"\n\n1-digit mean:"
    f"\n\nMean FP: {np.mean(fp_volumes):.1f}\n"
    f"Mean FN: {np.mean(fn_volumes):.1f}\n"
    f"Mean Dice: {np.mean(dice_scores):.1f}"
)
output_lines.append(summary)


with open("summary_metrics.txt", "w") as out_file:
    out_file.write("\n".join(output_lines))


print("\n".join(output_lines))