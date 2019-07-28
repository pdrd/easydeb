#!/bin/env python3

import sys
import os
import json

import subprocess

import click

import tempfile

from os import path

import glob

import shutil

# https://gist.github.com/SteveClement/3755572
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def exit_error(msg):
	print(msg)
	exit(1)

def load_config(ctx, recipe):
	ctx['json'] = json.load(recipe)

def validate_config(ctx):
	pass

def copy_files(ctx):
	for filepath in ctx['json']['files']:
		buildpath = path.normpath(path.join(ctx['build_dir'], filepath))
		tmppath = path.normpath(path.join(ctx['tmp_dir'], ctx['json']['files'][filepath]))

		if path.isfile(buildpath):
			os.makedirs(path.dirname(tmppath), exist_ok=True)
			shutil.copy2(buildpath, tmppath)
		elif path.isdir(buildpath):
			globpath = buildpath
			if not (globpath.endswith('*') or globpath.endswith('**')):
				globpath = path.join(buildpath, '**')
			globs = glob.glob(globpath, recursive=True)

			for filebuildpath in globs:
				relpath = path.relpath(filebuildpath, buildpath)
				fileoutpath = path.normpath(path.join(tmppath, relpath))

				if path.isfile(filebuildpath):
					shutil.copy2(filebuildpath, fileoutpath)
				elif path.isdir(filebuildpath):
					os.makedirs(fileoutpath, exist_ok=True)
					shutil.copystat(filebuildpath, fileoutpath)
					shutil.copymode(filebuildpath, fileoutpath)
	
	ctx['size'] = get_size(ctx['tmp_dir'])

def create_meta_dir(ctx):
	ctx['meta_dir'] = path.join(ctx['tmp_dir'], 'DEBIAN')
	os.mkdir(ctx['meta_dir'])

	path_changelog = path.join(ctx['meta_dir'], 'changelog')
	path_compat = path.join(ctx['meta_dir'], 'compat')
	path_control = path.join(ctx['meta_dir'], 'control')
	path_copyright = path.join(ctx['meta_dir'], 'copyright')

	with open(path_changelog,	"w+") as f:
		line = '{} ({}) UNRELEASED; urgency=low binary-only=yes\n'.format(ctx['json']['name'], ctx['json']['version'])
		f.write(line)

		f.write('\n')

		for change in ctx['json']['changes']:
			line = '  * {}\n'.format(change)
			f.write(line)

		f.write('\n')

		line = ' -- {} <{}>  {}\n'.format(ctx['json']['maintainer'], ctx['json']['email'], ctx['json']['changed_by'])
		f.write(line)

		f.write('\n')

	with open(path_compat,	"w+") as f:
		f.write('11') # works with debian stretch

	with open(path_control,	"w+") as f:
		line = 'Package: {}\n'.format(ctx['json']['name'])
		f.write(line)

		line = 'Version: {}\n'.format(ctx['json']['version'])
		f.write(line)

		line = 'Section: {}\n'.format(ctx['json']['section'])
		f.write(line)

		line = 'Priority: optional\n'
		f.write(line)

		line = 'Architecture: {}\n'.format(ctx['json']['arch'])
		f.write(line)

		line = 'Installed-Size: {}\n'.format(ctx['size'])
		f.write(line)

		line = 'Maintainer: {} <{}>\n'.format(ctx['json']['maintainer'], ctx['json']['email'])
		f.write(line)

		line = 'Description: {}\n'.format(ctx['json']['description'])
		f.write(line)

	with open(path_copyright,	"w+") as f:
		f.write('') # stays empty


def create_deb(ctx):
	ctx['tmp_dir'] = tempfile.mkdtemp()

	copy_files(ctx)
	create_meta_dir(ctx)

	ctx['out_file'] = '{}_{}_{}.deb'.format(ctx['json']['name'], ctx['json']['version'], ctx['json']['arch'])
	ctx['out_path'] = path.join(ctx['out_dir'], ctx['out_file'])

	subprocess.call('fakeroot dpkg-deb -b "{}" "{}"'.format(ctx['tmp_dir'], ctx['out_path']), executable=ctx['json']['shell'], shell=True)

	if path.isfile(ctx['out_path']):
		print('Generated package {}.'.format(ctx['out_path']))
	else:
		print('Something went wrong..')

	shutil.rmtree(ctx['tmp_dir'])

@click.command()
@click.argument('recipe', type=click.File(mode='r'))
@click.argument('build-dir', type=click.Path(exists=True, dir_okay=True))
@click.argument('out-dir', type=click.Path(exists=True, dir_okay=True, writable=True))
def run(recipe, build_dir, out_dir):
	ctx = {
		'build_dir': path.abspath(build_dir),
		'out_dir': path.abspath(out_dir)
	}

	load_config(ctx, recipe)
	validate_config(ctx)

	create_deb(ctx)

	print('Final context:')
	print(ctx)

if __name__ == '__main__':
	run()
