#
# Copyright (C) 2022 Dumpyara Project
#
# SPDX-License-Identifier: GPL-3.0
#

from typing import Callable, Dict
from liblp.partition_tools.lpunpack import lpunpack
from pathlib import Path
from shutil import move
from subprocess import STDOUT, check_output

from dumpyara.lib.libpayload import extract_android_ota_payload

def extract_payload(image: Path, output_dir: Path):
	extract_android_ota_payload(image, output_dir)

def extract_super(image: Path, output_dir: Path):
	unsparsed_super = output_dir / "super.unsparsed.img"

	try:
		check_output(["simg2img", image, unsparsed_super], stderr=STDOUT) # TODO: Rewrite libsparse...
	except Exception:
		pass
	else:
		move(unsparsed_super, image)

	lpunpack(image, output_dir)

MULTIPARTITIONS: Dict[str, Callable[[Path, Path], None]] = {
	"*payload.bin*": extract_payload,
	"*super*": extract_super,
}
