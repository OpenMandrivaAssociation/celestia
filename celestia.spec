Summary:	A real-time visual space simulation
Name:		celestia
Version:	1.5.1
Release:	%mkrel 3
License:	GPLv2+
Group:		Sciences/Astronomy
Source0:	http://prdownloads.sourceforge.net/celestia/%{name}-%{version}.tar.gz
Source1:	%{name}-16.png.bz2
Source2:	%{name}-32.png.bz2
Source3:	%{name}-48.png.bz2
Patch0:		celestia-1.5.0-gcc43.patch
Patch2:		celestia-1.5.0-kde-desktop.patch
Patch3:		celestia-1.4.1-cfg.patch
URL:		http://www.shatters.net/celestia/
BuildRequires:	libmesaglut-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gtkglarea-devel
BuildRequires:	kdelibs-devel
BuildRequires:	libarts-devel
BuildRequires:	gettext-devel
#BuildRequires:	lua-devel
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
%patch0 -p1 -b .gcc43
%patch2 -p0 -b .kde-desktop
%patch3 -p0 -b .cfg
# support for automake 1.10: empty file
# http://celestia.cvs.sourceforge.net/celestia/celestia/admin/config.rpath?view=markup&sortby=date
touch admin/config.rpath

%build
aclocal
libtoolize --force
automake
sed -i -e '/AM_GCONF_SOURCE_2/d'  configure.in
autoconf
%configure2_5x --with-gtk --with-kde --with-gnome --disable-rpath
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std transform=""

bzcat %{SOURCE1} > %{name}-16.png
bzcat %{SOURCE2} > %{name}-32.png
bzcat %{SOURCE3} > %{name}-48.png
install -D -m 644 %{name}-16.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m 644 %{name}-48.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

(cd $RPM_BUILD_ROOT

desktop-file-install --vendor="" --delete-original \
   --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde/ $RPM_BUILD_ROOT%{_datadir}/applnk/Edutainment/Science/celestia.desktop
cd -
)


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
rm -rf $RPM_BUILD_ROOT


%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL README TODO 
#%{_docdir}/HTML
%attr(755,root,root) %{_bindir}/*
%{_datadir}/apps/*
%{_datadir}/config/*
%{_datadir}/mimelnk/*
%{_datadir}/services/*
%{_datadir}/applications/kde/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
