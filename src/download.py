#!/usr/bin/python
#
#  Copyright Andrew Hunter, Luis de Bethencourt Guimera 2008
#
#    This program is free software; you may redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the Free 
#    Software Foundation; either version 2 of the License, or (at your option) 
#    any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
#    more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from shutil import move
import urllib
import threading

class Download(threading.Thread):
    def __init__(self, source, filename):
       self.source = source
       self.filename = filename
       threading.Thread.__init__(self)

    def run(self):
       tmp_file = urllib.urlretrieve(self.source)
       move(tmp_file[0], self.filename)

if __name__ == "__main__":
    source = 'https://launchpadlibrarian.net/12174626/flickbook192.jpg'
    filename = 'test.jpg'
    Download(source, filename).start()
