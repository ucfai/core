################################################################################
## uDocker is a Python "package" to make running Docker containers in 
##   prescribed ways simpler to the layman. 
## Learning Docker isn't nearly as important as learning the content the 
##   containers are used for.
################################################################################

import os
import argparse
from subprocess import call

import docker
from docker import img, start, build, pull

__author__  = "John Muchovej <github.com/ionlights>"
__email__   = "john@ionlights.com"

__license__ = "GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = "John Muchovej"
__copyright__  = "(c) 2018, John Muchovej"


def build(args):
  if not docker.pull(args.use_gpu):
    print(">-------------------------------------------------------------------------------")
    print(">\n> Failed to pull Docker repository, will now attempt to build.\n>")
    print(">-------------------------------------------------------------------------------")
    docker.build(args.use_gpu)


def start(args):
  docker.start(args.use_gpu, attach=args.attach)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="""
      Docker container manager for Udacity Nanodegrees. This will handle the 
      construction and launching of Docker containers for the {}.
    """.format(img)
    )

  ## setup subparser - this allows for contextual --cpu,--gpu commands
  subparsers = parser.add_subparsers(dest="cmd")
  
  ## base setup for cpu/gpu arguments
  cpu = {"action": "store_false", "dest": "use_gpu",}
  gpu = {"action": "store_true" , "dest": "use_gpu",}


  ## help messages for each toggle
  cpu["help"] = "Build the CPU-based image."
  gpu["help"] = "Build the GPU-based image."

  ## `build` subparser
  parser_build = subparsers.add_parser("build",
    help="Build the {}'s Docker container.".format(img))

  ## boolean flags
  group_build = parser_build.add_mutually_exclusive_group(required=True)
  group_build.add_argument("--cpu",  **cpu)
  group_build.add_argument("--gpu",  **gpu)


  ## help messages for each toggle
  cpu["help"] = "Start the CPU-based container."
  gpu["help"] = "Start the GPU-based container."

  ## `start` subparser
  parser_start = subparsers.add_parser("start",
    help="Start the {}'s Docker container.".format(img))
  
  ## boolean flags
  group_start = parser_start.add_mutually_exclusive_group(required=True)
  group_start.add_argument("--cpu", **cpu)
  group_start.add_argument("--gpu", **gpu)

  ## allow for running in attached mode
  attach = {"default": False, "action": "store_true", "dest": "attach", 
            "help": "Keep the container attached to this terminal wiimgow."}

  parser_start.add_argument("--attach", **attach)


  ## parse args and `build` or `start`
  args = parser.parse_args()
  eval(args.cmd)(args)