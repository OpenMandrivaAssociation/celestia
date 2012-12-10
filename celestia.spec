Summary:		A real-time visual space simulation
Name:		celestia
Version:		1.6.1
Release:		1
License:		GPLv2+
Group:		Sciences/Astronomy
Source0:		http://prdownloads.sourceforge.net/celestia/%{name}-%{version}.tar.gz
Source1:		%{name}-16.png
Source2:		%{name}-32.png
Source3:		%{name}-48.png
Patch0:         celestia-1.6.1-gcc46.patch
Patch1:         celestia-1.6.0-cfg.patch
Patch2:         celestia-1.6.1-zlib.patch
Patch3:         celestia-1.6.1-link.patch
Patch4:         celestia-1.6.1-gcc47.patch
URL:		http://www.shatters.net/celestia/

BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(gdk-2.0) 
BuildRequires:	pkgconfig(gdkglext-1.0)
BuildRequires:	jpeg-devel
BuildRequires:  	pkgconfig(libpng)
BuildRequires:	pkgconfig(lua)
BuildRequires:	desktop-file-utils

%description
Celestia is a free real-time space simulation that lets you experience
our universe in three dimensions. Unlike most planetarium software,
Celestia doesn't confine you to the surface of the Earth. You can
travel throughout the solar system, to any of over 100,000 stars, or
even beyond the galaxy. All travel in Celestia is seamless; the
exponential zoom feature lets you explore space across a huge range of
scales, from galaxy clusters down to spacecraft only a few meters
across. A 'point-and-goto' interface makes it simple to navigate
through the universe to the object you want to visit.

%prep

%setup -q
%patch0 -p0 -b .gcc
%patch1 -p0 -b .cfg
%patch2 -p0 -b .zlib
%patch3 -p0 -b .link
%patch4 -p1 -b .gcc47

# support for automake 1.10: empty file
# http://celestia.cvs.sourceforge.net/celestia/celestia/admin/config.rpath?view=markup&sortby=date
touch admin/config.rpath

%build
autoreconf -fi
%configure2_5x --with-gtk \
		--disable-rpath \
		--enable-cairo \
		--enable-theora \
		--with-lua
%make

%install
%makeinstall_std

desktop-file-install --vendor='' \
	--dir %{buildroot}%{_datadir}/applications \
	--remove-category='Application' \
	--add-category='GTK;Education' \
	--remove-key='Version' \
	%{buildroot}%{_datadir}/applications/*.desktop

install -D -m 644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png


%find_lang %{name}  


%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING INSTALL README 
%attr(755,root,root) %{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/locale/*/LC_MESSAGES/celestia_constellations.mo

%changelog
* Fri Oct 07 2011 Andrey Bondrov <abondrov@mandriva.org> 1.6.1-1mdv2012.0
+ Revision: 703451
- New version: 1.6.1

  + Funda Wang <fwang@mandriva.org>
    - drop old files

* Mon Dec 06 2010 Funda Wang <fwang@mandriva.org> 1.6.0-3mdv2011.0
+ Revision: 611370
- add gentoo patch to make it build

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 1.6.0-2mdv2010.0
+ Revision: 436988
- rebuild

  + Emmanuel Andry <eandry@mandriva.org>
    - BR jpeg-devel
    - New version 1.6.0
    - use GTK frontend to be desktop agnostic
    - drop P0
    - rediff P1 (was P3)
    - add P0 from gentoo to fix GCC44 build

* Sun Nov 23 2008 Funda Wang <fwang@mandriva.org> 1.5.1-3mdv2009.1
+ Revision: 305969
- build gnome frontend
- rediff patch0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Oden Eriksson <oeriksson@mandriva.com>
    - added a gcc43 patch from fedora

* Wed May 07 2008 Funda Wang <fwang@mandriva.org> 1.5.1-1mdv2009.0
+ Revision: 202885
- New version 1.5.1

* Fri Feb 01 2008 Funda Wang <fwang@mandriva.org> 1.5.0-1mdv2008.1
+ Revision: 161002
- fix desktop file icon
- FIx desktop orig dir
- drop old patches
- add missing file
- New version 1.5.0

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.1-9mdv2008.1
+ Revision: 137975
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 16 2007 Emmanuel Andry <eandry@mandriva.org> 1.4.1-8mdv2008.0
+ Revision: 52746
- rediff patch2
- disable lua, make problems
- update patch2
- added lua support
- added patch 7 for lua
- added patches 2, 3, 4, 5, 6
- fix bugs 24720, 25752, 28572
- drop patch 1

  + Andreas Hasenack <andreas@mandriva.com>
    - rebuild to fix buildroot problem (/usr/share/apps/celestia was pointing to the buildroot)
    - support automake 1.10

  + Olivier Thauvin <nanardon@mandriva.org>
    - rebuild


* Sun Nov 05 2006 Emmanuel Andry <eandry@mandriva.org> 1.4.1-3mdv2007.0
+ Revision: 76781
-fix x86_64 build (bug#25768)
- commit-message

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - celestia-1.4.1-2mdv2007.0
    - Really fix to xdg (and to have menu entry on new menu
      not a bad one)

* Fri Aug 04 2006 Olivier Thauvin <nanardon@mandriva.org> 1.4.1-1mdv2007.0
+ Revision: 43311
- 1.4.1
- xdg menu
- patch fixing c++ and destdir
- Import celestia

