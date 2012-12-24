#!/usr/bin/python2
#
# Copyright (c) 2012 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import logging

from fileset import *
from project import *
from projects import *

temp_dir = "./tmp"

def process(url):

	newtranslated = 0
	filename = 'translations.tar.gz'

	download = DownloadFile()
	download.GetFile(url, filename)

	# Uncompress
	os.system("tar -xvf " + filename + " -C " + temp_dir + " > /dev/null")

	# Apply tm
	findFiles = FindFiles()

	for filename in findFiles.Find(temp_dir, '*.po*'):

		tmfilename = os.path.dirname(filename) + "/tm-" + os.path.basename(filename)
		os.system("msgmerge -N " + filename + " " + filename + " -C tm.po > " + tmfilename + " 2> /dev/null")

		infile = polib.pofile(filename)
		tmfile = polib.pofile(tmfilename)

		intranslated = len(infile.translated_entries())
		tmtranslated = len(tmfile.translated_entries())

		if (tmtranslated > intranslated + 20):
			new = tmtranslated - intranslated
			print filename + " original:", intranslated, ",tm:", tmtranslated, "new translated", new
			dfilename = os.path.dirname(filename) + "/diff-" + os.path.basename(filename)
			os.system("diff -u " + filename + " " + tmfilename + " >" + dfilename)
			newtranslated += new
		else:
			os.system("rm -f " + filename)
			os.system("rm -f " + tmfilename)

	return newtranslated

def main():

	newtranslated = 0
	os.system("rm -r -f " + temp_dir)
	os.system("mkdir " + temp_dir)

	newtranslated += process('http://l10n.gnome.org/languages/ca/gnome-extras/ui.tar.gz')
	newtranslated += process('http://l10n.gnome.org/languages/ca/gnome-3-8/ui.tar.gz')
	newtranslated += process('http://l10n.gnome.org/languages/ca/gnome-office/ui.tar.gz')
	newtranslated += process('http://l10n.gnome.org/languages/ca/external-deps/ui.tar.gz')
	newtranslated += process('http://l10n.gnome.org/languages/ca/gnome-infrastructure/ui.tar.gz')
	newtranslated += process('http://l10n.gnome.org/languages/ca/gnome-gimp/ui.tar.gz')
	print "Total new strings", newtranslated

if __name__ == "__main__":
    main()


