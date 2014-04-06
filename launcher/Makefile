version := $(strip $(shell cat VERSION))
series := $(strip $(shell cat SERIES))
prefix := /usr
build_dir := "."
dist_name = fs-uae-launcher-$(version)
dist_dir := $(build_dir)/$(dist_name)

ifeq ($(wildcard fs_uae_launcher),)
	fs_uae_launcher_dir := "../python"
else
	fs_uae_launcher_dir := "."
endif

ifeq ($(wildcard fs_uae_workspace),)
	fs_uae_workspace_dir := "../python"
else
	fs_uae_workspace_dir := "."
endif

ifeq ($(wildcard fsbc),)
	fsbc_dir := "../python"
else
	fsbc_dir := "."
endif

ifeq ($(wildcard fsgs),)
	fsgs_dir := "../python"
else
	fsgs_dir := "."
endif

ifeq ($(wildcard fsui),)
	fsui_dir := "../python"
else
	fsui_dir := "."
endif

ifeq ($(wildcard game_center),)
	game_center_dir := "../python"
else
	game_center_dir := "."
endif

ifeq ($(wildcard lhafile),)
	lhafile_dir := "../python-lhafile"
else
	lhafile_dir := "."
endif

ifeq ($(wildcard six),)
	six_dir := "../python"
else
	six_dir := "."
endif

all: mo

share/locale/%/LC_MESSAGES/fs-uae-launcher.mo: po/%.po
	mkdir -p share/locale/$*/LC_MESSAGES
	msgfmt --verbose $< -o $@

catalogs = \
	share/locale/cs/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/da/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/de/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/es/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/fi/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/fr/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/hu/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/it/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/nb/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/pl/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/pt/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/pt_BR/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/ru/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/sr/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/sv/LC_MESSAGES/fs-uae-launcher.mo \
	share/locale/tr/LC_MESSAGES/fs-uae-launcher.mo

mo: $(catalogs)

install: mo
	mkdir -p $(DESTDIR)$(prefix)/share
	cp -a share/* $(DESTDIR)$(prefix)/share

	mkdir -p $(DESTDIR)$(prefix)/share/doc/fs-uae-launcher
	cp -a README COPYING $(DESTDIR)$(prefix)/share/doc/fs-uae-launcher

dist_dir := fs-uae-launcher-$(version)

distdir:
	rm -Rf $(dist_dir)/*
	mkdir -p $(dist_dir)

	cp -a $(fs_uae_launcher_dir)/fs_uae_launcher $(dist_dir)/
	cp -a $(fs_uae_workspace_dir)/fs_uae_workspace $(dist_dir)/
	cp -a $(fsbc_dir)/fsbc $(dist_dir)/
	cp -a $(fsgs_dir)/fsgs $(dist_dir)/
	cp -a $(fsui_dir)/fsui $(dist_dir)/
	cp -a $(game_center_dir)/game_center $(dist_dir)/
	cp -a $(lhafile_dir)/lhafile $(dist_dir)/
	cp -a $(six_dir)/six $(dist_dir)/
	cp -a share $(dist_dir)/
	mkdir $(dist_dir)/po/

	find $(dist_dir) -name "*.mo" -delete
	find $(dist_dir) -name "*.pyc" -delete
	find $(dist_dir) -name "*.pyo" -delete
	find $(dist_dir) -name __pycache__ -delete

	cp COPYING $(dist_dir)/
	cp INSTALL $(dist_dir)/
	cp Makefile $(dist_dir)/
	cp README $(dist_dir)/
	cp SERIES $(dist_dir)/
	cp VERSION $(dist_dir)/
	mkdir -p $(dist_dir)/debian
	cp debian/changelog $(dist_dir)/debian
	cp debian/compat $(dist_dir)/debian
	cp debian/control $(dist_dir)/debian
	cp debian/copyright $(dist_dir)/debian
	cp debian/links $(dist_dir)/debian
	cp debian/rules $(dist_dir)/debian
	mkdir -p $(dist_dir)/debian/source
	cp debian/source/format $(dist_dir)/debian/source
	cp fs-uae-launcher $(dist_dir)/
	cp fs-uae-launcher.spec $(dist_dir)/
	mkdir -p $(dist_dir)/icon
	cp icon/fs-uae-launcher.icns $(dist_dir)/icon
	cp icon/fs-uae-launcher.ico $(dist_dir)/icon
	mkdir -p $(dist_dir)/macosx
	cp macosx/Makefile $(dist_dir)/macosx
	cp po-update.py $(dist_dir)/
	mkdir -p $(dist_dir)/po
	cp po/cs.po $(dist_dir)/po
	cp po/da.po $(dist_dir)/po
	cp po/de.po $(dist_dir)/po
	cp po/es.po $(dist_dir)/po
	cp po/fi.po $(dist_dir)/po
	cp po/fr.po $(dist_dir)/po
	cp po/hu.po $(dist_dir)/po
	cp po/it.po $(dist_dir)/po
	cp po/nb.po $(dist_dir)/po
	cp po/pl.po $(dist_dir)/po
	cp po/pt.po $(dist_dir)/po
	cp po/pt_BR.po $(dist_dir)/po
	cp po/ru.po $(dist_dir)/po
	cp po/sr.po $(dist_dir)/po
	cp po/sv.po $(dist_dir)/po
	cp po/tr.po $(dist_dir)/po
	cp setup.py $(dist_dir)/
	cp update-version.py $(dist_dir)/
	mkdir -p $(dist_dir)/windows
	cp windows/Makefile $(dist_dir)/windows
	cp windows/fs-uae-launcher.iss $(dist_dir)/windows
	cp windows/replace-icon.py $(dist_dir)/windows
	cd $(dist_dir) && python update-version.py setup.py
	cd $(dist_dir) && python update-version.py debian/changelog
	cd $(dist_dir) && python update-version.py fs-uae-launcher --update-series
	cd $(dist_dir) && python update-version.py fs-uae-launcher.spec

dist: distdir
	find $(dist_dir) -exec touch \{\} \;
	cd "$(build_dir)" && tar zcfv $(dist_name).tar.gz $(dist_name)

windows-dist: distdir
	cd $(dist_dir)/windows && make
	mv $(dist_dir)/fs-uae-launcher_*windows* .
	rm -Rf $(dist_dir)

macosx-dist: distdir
	cd $(dist_dir)/macosx && make
	mv $(dist_dir)/fs-uae-launcher_*macosx* .
	rm -Rf $(dist_dir)

clean-dist:
	rm -Rf build dist fs-uae-launcher-* fs-uae-launcher_*
	rm -Rf debian/fs-uae-launcher*

clean:
	find share -name "*.mo" -delete
	find . -name "*.pyc" -delete

distclean: clean clean-dist