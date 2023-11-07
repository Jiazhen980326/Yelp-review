import argparse

import azureml.core
from azureml.core import Environment, Workspace


def create_env(
    workspace,
    env_name,
    conda_yaml,
    base_image_name,
):

    azureml.core.environment.DEFAULT_CPU_IMAGE = base_image_name

    env = Environment.from_conda_specification(
        env_name, conda_yaml
    ) 

    env.register(workspace)
    build = env.build_local(
        workspace=workspace, useDocker=True, pushImageToWorkspaceAcr=True
    )


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--env_name",
        dest="env_name",
        default="nlp",
        help="Name of new environment",
        type=str,
    )
    parser.add_argument(
        "-y",
        "--conda_yaml_path",
        dest="conda_yaml_path",
        default="environment.yml",
        help="Conda environment YAML file",
        type=str,
    )
    parser.add_argument(
        "-b",
        "--base_image_name",
        dest="base_image_name",
        default="mcr.microsoft.com/azureml/curated/minimal-ubuntu20.04-py38-cpu-inference:latest",
        help="Name of Base Image",
        type=str,
    )

    args = parser.parse_args()

    ws = Workspace.from_config()

    create_env(
        ws,
        env_name=args.env_name,
        conda_yaml=args.conda_yaml_path,
        base_image_name=args.base_image_name,
    )


if __name__ == "__main__":
    main()