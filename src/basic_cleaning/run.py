#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import os
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_local_path = artifact.file()

    df = pd.read_csv(artifact_local_path)

    logger.info("Dropping outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
     name=args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    os.remove("clean_sample.csv")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Fully qualified name for the artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Fully qualified name for the artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the artifact to create",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for the artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="min price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="max price",
        required=True
    )



    args = parser.parse_args()

    go(args)
