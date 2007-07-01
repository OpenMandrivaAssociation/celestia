%define name celestia
%define version 1.4.1
%define release %mkrel 4

Summary:	A real-time visual space simulation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sciences/Astronomy
Source0:	http://prdownloads.sourceforge.net/celestia/%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png.bz2
Source2:	%{name}-32.png.bz2
Source3:	%{name}-48.png.bz2
Patch0:		celestia-1.4.1-cpp.patch
#Patch1:		celestia-1.4.1-destdir.patch
Patch2:		celestia-1.4.1-kde-desktop.patch
Patch3:		celestia-1.4.1-cfg.patch
Patch4:		celestia-1.4.1-kde-datadir.patch
Patch5:		celestia-1.4.1-3dsmodels.patch
Patch6:		celestia-1.4.1-locale.patch
URL:		http://www.shatters.net/celestia/
BuildRequires:	libmesaglut-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gtkglarea-devel
BuildRequires:  kdelibs-devel
BuildRequires:  libarts-devel
BuildRequires:	gettext-devel
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
%patch0 -p0 -b .cppfix
#%patch1 -p0 -b .destdir
%patch2 -p0 -b .kde-desktop
%patch3 -p0 -b .cfg
%patch4 -p0 -b .kde-datadir
%patch5 -p0 -b .3dsmodels
%patch6 -p0 -b .locale

%build

aclocal
libtoolize --force
automake
autoconf-2.5x || :

%configure2_5x --with-gtk --with-kde --with-gnome --disable-rpath --with-qt-libraries=/usr/lib/qt3/%{_lib}
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
mkdir -p ./%{_menudir}
cat > ./%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="%{_bindir}/celestia"\
title="Celestia"\
longtitle="An astronomy simultor"\
needs="x11"\
icon="%{name}.png"\
section="More Applications/Sciences/Astronomy"\
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Astronomy" \
  --add-category="Science" \
  --add-category="X-MandrivaLinux-MoreApplications-Sciences-Astronomy" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/kde/ $RPM_BUILD_ROOT%{_datadir}/%{_datadir}/applications/kde/*

)


%find_lang %name

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL README TODO 
#%{_docdir}/HTML
%attr(755,root,root) %{_bindir}/*
%{_datadir}/applnk/*
%{_datadir}/apps/*
%{_datadir}/config/*
%{_datadir}/mimelnk/*
%{_datadir}/services/*
%{_datadir}/applications/kde/%{name}.desktop
# applnk/  apps/  config/  doc/  icons/  mimelnk/  services/
%{_datadir}/%{name}
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
#%_sysconfdir/gconf/schemas/*



