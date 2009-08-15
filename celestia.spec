Summary:	A real-time visual space simulation
Name:		celestia
Version:	1.6.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Sciences/Astronomy
Source0:	http://prdownloads.sourceforge.net/celestia/%{name}-%{version}.tar.gz
Source1:	%{name}-16.png.bz2
Source2:	%{name}-32.png.bz2
Source3:	%{name}-48.png.bz2
Patch0:		celestia-1.5.1-gcc44.patch
Patch1:		celestia-1.6.0-cfg.patch
URL:		http://www.shatters.net/celestia/
BuildRequires:	libmesaglut-devel
#BuildRequires:	gnome-libs-devel
BuildRequires:	cairo-devel
BuildRequires:	gettext-devel
BuildRequires:	libtheora-devel
BuildRequires:	gtk2-devel gtkglext-devel
BuildRequires:	lua-devel
BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p1 -b .gcc44
%patch1 -p0 -b .cfg
# support for automake 1.10: empty file
# http://celestia.cvs.sourceforge.net/celestia/celestia/admin/config.rpath?view=markup&sortby=date
touch admin/config.rpath

%build
#make -f admin/Makefile.common
%configure2_5x --with-gtk \
		--disable-rpath \
		--enable-cairo \
		--enable-theora \
		--with-lua
%make

%install
rm -rf %buildroot
%makeinstall_std

desktop-file-install --vendor='' \
	--dir %buildroot%_datadir/applications \
	--remove-category='Application' \
	--add-category='GTK;' \
	--remove-key='Version' \
	%buildroot%_datadir/applications/*.desktop

bzcat %{SOURCE1} > %{name}-16.png
bzcat %{SOURCE2} > %{name}-32.png
bzcat %{SOURCE3} > %{name}-48.png
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png

%find_lang %name %name celestia_constellations

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL README 
%attr(755,root,root) %{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
