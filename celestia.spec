Summary:	A real-time visual space simulation
Name:		celestia
Version:	1.6.1
Release:	2
License:	GPLv2+
Group:		Sciences/Astronomy
Url:		http://www.shatters.net/celestia/
Source0:	http://prdownloads.sourceforge.net/celestia/%{name}-%{version}.tar.gz
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Patch0:		celestia-1.6.1-gcc46.patch
Patch1:		celestia-1.6.0-cfg.patch
Patch2:		celestia-1.6.1-zlib.patch
Patch3:		celestia-1.6.1-link.patch
Patch4:		celestia-1.6.1-gcc47.patch
Patch5:		celestia-1.6.1-libpng-16.patch
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gdk-2.0)
BuildRequires:	pkgconfig(gdkglext-1.0)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(theora)

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

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING INSTALL README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0 -b .gcc
%patch1 -p0 -b .cfg
%patch2 -p0 -b .zlib
%patch3 -p0 -b .link
%patch4 -p1 -b .gcc47
%patch5 -p0 -b .png16

# support for automake 1.10: empty file
# http://celestia.cvs.sourceforge.net/celestia/celestia/admin/config.rpath?view=markup&sortby=date
touch admin/config.rpath

# (cjw) A new gettext Makefile.in.in is needed for new autotools but gettextize 
#       cannot be run from a script, so copy it manually.
#       This hack should be removed when upstream updates gettext files.
cp -f %{_datadir}/gettext/po/Makefile.in.in po/Makefile.in.in
cp -f %{_datadir}/gettext/po/Makefile.in.in po2/Makefile.in.in

%build
autoreconf -fi
%configure2_5x \
	--with-gtk \
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

%find_lang %{name} celestia_constellations %{name}.lang

