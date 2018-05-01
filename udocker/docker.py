import os
from subprocess import call, check_output
import pyyaml

with open("udocker/config.yml", "r") as yml:
	config = pyyaml.load(yml)

## possible base images for the Dockerfiles
_base = config["base"]


## accepted Dockerfiles
accepted = ["udocker/{}.Dockerfile".format(f) for f in _base.keys()]
template =  "udocker/template.Dockerfile"


################################################################################
## Docker tagging and arguments
################################################################################
image = config["image"]

## docker image construction, host/image:tag
tag = None  ## should be unset, is based on user spec'd args
container = None

build_args = config["build-args"]

## runtime arguments
args_start = []

start_args = config["start-args"]


def _container(use_gpu):
	global tag
	tag = "gpu" if use_gpu else "cpu"

	global container
	container = "{}/{}:{}".format(image["host"], image["name"], tag)

	global args_start
	args_start += ["-v {}".format(v) for v in start_args["volumes"]]
	args_start += ["-p {}".format(p) for v in start_args["ports"]]



def start(use_gpu, attach=True):
	_container(use_gpu)

	## stop current running container
	if check_output("docker inspect -f {{.State.Running}} {}".format(img), shell=True).strip().decode("utf-8") == "true":
		call("docker stop {}".format(img))


	args_default = [
		"--runtime=nvidia" if use_gpu else "", 	## runtime
		"--rm", 								## remove on stop
		"-d" if not attach else "",				## run container in detached _mode
		"--name {}".format(img), 				## name container for simpler management
	]

	return call(" ".join(
		["docker", "run"]
		+ args_default
		+ args_start
		+ [container]
	), shell=True)


def pull(use_gpu):
	_container(use_gpu)

	return call("docker pull {}".format(container), shell=True) == 0


def build(use_gpu):
	dockerfile = "udocker/{}.Dockerfile".format(tag)
	assert dockerfile in accepted

	args_default = [
		"-t {}".format(container),	## tag the container
		"-f {}".format(dockerfile),	## dockerfile
	]

	if dockerfile not in os.listdir(os.getcwd()):
		with open(template, "r") as tmpl, open(dockerfile, "w") as outp:
			read = tmpl.read()
			read = read.replace("%%base%%", _base[tag])
			read = read.replace("%%conda%%", build_args["conda"])
			read = read.replace("%%type%%", tag)
			read = read.replace("%%name%%", img)
			outp.write(read)

	return call(" ".join(
		["docker", "build"]
		+ args_default
		+ ["udocker"]
	), shell=True)

