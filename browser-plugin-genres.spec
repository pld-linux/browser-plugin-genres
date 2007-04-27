Summary:	GenReS browser scriptable plugin
Summary(pl):	GenReS - skryptowalna wtyczka do przegladarki
Name:		browser-plugin-genres
Version:	0.9.2
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://download.savannah.nongnu.org/releases/genres/genres-%{version}.tar.bz2
# Source0-md5:	795f62635a28caef2b75383bc6422c50
Patch0:		genres-mozilla-config.patch
Patch1:		genres-itvp.patch
URL:		https://savannah.nongnu.org/projects/genres
BuildRequires:	XFree86-devel
BuildRequires:	mozilla-firefox-devel
Requires:	perl-Gtk2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins
%define		browsers	mozilla, mozilla-firefox

%description
GenReS is a generic reconfigurable scriptable plugin for
Mozilla/Firefox. It allows to use external programs for EMBED or
OBJECT HTML tags. The plugin is supplied with a Perl script for
embedding mplayer and mencoder in a browser and controlling it with
Javascript. It allows to play audio and video files and streams and to
record them to set of files. Manipulations with object variables in
JavaScript are translated to a Perl program. Status messages from the
controlled program (mplayer or mencoder) are translated back to
Javascript object variables, and Javascript functions are called for
notifications.

Supported browsers: %{browsers}.

%description -l pl
GenReS to uniwersalny skryptowalny plugin dla Mozilli/Firefoksa.
Umo¿liwia u¿ywanie zewnêtrznych programów do obs³ugi tagów EMBED i
OBJECT. Plugin pe³ni rolê interfejsu miêdzy stron± www/JavaScriptem, a
skryptem zdefiniowanym do obs³ugi danego typu mime. Dwustronna
komunikacja miêdzy skryptem a stron± oparta jest na strumieniach
we/wy, dziêki czemu tworzenie skryptów jest proste, mo¿na je pisaæ w
dowolnym jêzyku. W pakiecie znajduje siê przyk³adowy, ale w pe³ni
funkcjonalny skrypt napisany w Perlu embeduj±cy mplayera oraz
mencodera i umo¿liwiaj±cy ich kontrolê z okna przegl±darki.

%prep
%setup -q -n genres-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D genres.so $RPM_BUILD_ROOT%{_plugindir}/genres.so
install -D slaves/video/mplayer.sh $RPM_BUILD_ROOT%{_libdir}/genres/mplayer.sh
install -D doc/genres.conf $RPM_BUILD_ROOT%{_sysconfdir}/genres.conf
%{__make} DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/mozilla
rm -rf $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins genres.so genres.so

%triggerun -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins genres.so genres.so

%triggerin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins genres.so genres.so

%triggerun -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins genres.so genres.so

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/genres.so
%attr(644,root,root) %{_sysconfdir}/genres.conf
%attr(755,root,root) %{_libdir}/genres/config.pl
%attr(755,root,root) %{_libdir}/genres/mplayer.pl
%attr(755,root,root) %{_libdir}/genres/mplayer.sh
%attr(755,root,root) %{_libdir}/genres/slaves
%doc README.en.html example
