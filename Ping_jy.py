#!/usr/bin/env python
import sys
import gtk
import gobject
import appindicator
import subprocess


I_PING_PATH = '/home/jshuay/Testing_Grounds/Ping.jy/res/icons/ping.png'
I_PINGING_PATH = '/home/jshuay/Testing_Grounds/Ping.jy/res/icons/pinging.png'
S_PING_PATH = '/home/jshuay/Testing_Grounds/Ping.jy/scripts/ping.sh'


class Ping_jy:
    def __init__(self):
        status = appindicator.CATEGORY_APPLICATION_STATUS
        self.ind = appindicator.Indicator("debian-doc-menu",
                                          I_PING_PATH,
                                          status)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_label("Ping")
        self.menu_setup()
        self.ind.set_menu(self.menu)
        self.toggle = True
        self.ping()
        self.id = gtk.timeout_add(10000, self.ping)
        gtk.timeout_add(2000, self.animate_icon)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.update_30 = gtk.MenuItem("30 Sec")
        self.update_30.connect("activate", self.up30)
        self.update_30.show()
        self.menu.append(self.update_30)

        self.update_10 = gtk.MenuItem("10 Sec")
        self.update_10.connect("activate", self.up10)
        self.update_10.show()
        self.menu.append(self.update_10)

        self.update_2 = gtk.MenuItem("2 Sec")
        self.update_2.connect("activate", self.up2)
        self.update_2.show()
        self.menu.append(self.update_2)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def up30(self, widget):
        gobject.source_remove(self.id)
        self.id = gtk.timeout_add(30000, self.ping)

    def up10(self, widget):
        gobject.source_remove(self.id)
        self.id = gtk.timeout_add(10000, self.ping)

    def up2(self, widget):
        gobject.source_remove(self.id)
        self.id = gtk.timeout_add(2000, self.ping)

    def main(self):
        gtk.main()

    def animate_icon(self):
        if self.toggle:
            self.ind.set_icon(I_PINGING_PATH)
        else:
            self.ind.set_icon(I_PING_PATH)
        self.toggle = not self.toggle
        return True

    def ping(self):
        cmd = S_PING_PATH
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.wait()
        line = p.stdout.readline().rstrip()
        if line != '':
            self.ind.set_label(line[line.find('time=') + 5:])
        return True

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    indicator = Ping_jy()
    indicator.main()
