# TODO:
# - browser-plugins v2
# - port to xulrunner >= 1.9.0
Summary:	GenReS browser scriptable plugin
Summary(pl.UTF-8):	GenReS - skryptowalna wtyczka do przeglądarki
Name:		browser-plugin-genres
Version:	1.0.2
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://download.savannah.nongnu.org/releases/genres/genres-%{version}.tar.bz2
# Source0-md5:	b18778368fd5f9889557ab98f4998dcd
Patch0:		genres-mozilla-config.patch
Patch1:		genres-itvp.patch
URL:		https://savannah.nongnu.org/projects/genres
BuildRequires:	pkgconfig
BuildRequires:	xulrunner-devel < 1.9.0
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

%description -l pl.UTF-8
GenReS to uniwersalna skryptowalna wtyczka dla przeglądarek z rodziny
Mozilli. Umożliwia używanie zewnętrznych programów do obsługi
znaczników EMBED i OBJECT. Wtyczka pełni rolę interfejsu między stroną
WWW/JavaScriptem, a skryptem zdefiniowanym do obsługi danego typu
MIME. Dwustronna komunikacja między skryptem a stroną oparta jest na
strumieniach we/wy, dzięki czemu tworzenie skryptów jest proste, można
je pisać w dowolnym języku. W pakiecie znajduje się przykładowy, ale w
pełni funkcjonalny skrypt napisany w Perlu osadzający mplayera oraz
mencodera i umożliwiający ich kontrolę z okna przeglądarki.

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%doc README.en.html example
%attr(755,root,root) %{_plugindir}/genres.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/genres.conf
%attr(755,root,root) %{_libdir}/genres/config.pl
%attr(755,root,root) %{_libdir}/genres/mplayer.pl
%attr(755,root,root) %{_libdir}/genres/mplayer.sh
%attr(755,root,root) %{_libdir}/genres/slaves
