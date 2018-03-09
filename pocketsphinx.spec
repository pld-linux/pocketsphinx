#
# Conditional build:
%bcond_without	gstreamer	# GStreamer (0.1) plugin
%bcond_without	python		# Python extension
%bcond_without	static_libs	# static library

Summary:	CMU PocketSphinx - lightweight speech recognition system
Summary(pl.UTF-8):	CMU PocketSphinx - lekki system rozpoznawania mowy
Name:		pocketsphinx
Version:	0.8
Release:	1
License:	BSD
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/cmusphinx/%{name}-%{version}.tar.gz
# Source0-md5:	9f6fb6277d57fb33d2c49d4184587d26
URL:		https://cmusphinx.github.io/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
%if %{with gstreamer}
BuildRequires:	gstreamer0.10-devel >= 0.10.0
BuildRequires:	gstreamer0.10-plugins-base-devel >= 0.10.0
%endif
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 2.0
%endif
BuildRequires:	sphinxbase-devel >= 0.8
Requires:	sphinxbase >= 0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is PocketSphinx, one of Carnegie Mellon University's open source
large vocabulary, speaker-independent continuous speech recognition
engine.

%description -l pl.UTF-8
PocketSphinx - jeden z pochodzących z Carnegie Mellon University,
mających otwarte źródła i bogaty zasób słów, niezależnych od mówiącego
silników rozpoznawania mowy ciągłej.

%package model-en
Summary:	English language models for CMU PocketSphinx
Summary(pl.UTF-8):	Modele języka angielskiego dla silnika CMU PocketSphinx
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description model-en
English (US) language models for CMU PocketSphinx speech recognition
engine.

%description model-en -l pl.UTF-8
Modele języka angielskiego (amerykańskiego) dla silnika rozpoznawania
mowy CMU PocketSphinx.

%package model-zh
Summary:	Chinese language models for CMU PocketSphinx
Summary(pl.UTF-8):	Modele języka chińskiego dla silnika CMU PocketSphinx
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description model-zh
Chinese (both China and Taiwan) language models for CMU PocketSphinx
speech recognition engine.

%description model-zh -l pl.UTF-8
Modele języka chińskiego (dla Chin i Tajwanu) dla silnika
rozpoznawania mowy CMU PocketSphinx.

%package devel
Summary:	CMU PocketSphinx header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CMU PocketSphinx
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	sphinxbase-devel >= 0.8

%description devel
CMU PocketSphinx header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CMU PocketSphinx.

%package static
Summary:	Static CMU PocketSphinx library
Summary(pl.UTF-8):	Biblioteka statyczna CMU PocketSphinx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of CMU PocketSphinx library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki CMU PocketSphinx.

%package apidocs
Summary:	API documentation for CMU PocketSphinx library
Summary(pl.UTF-8):	Dokumentacja API biblioteki CMU PocketSphinx
Group:		Documentation

%description apidocs
API documentation for CMU PocketSphinx library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki CMU PocketSphinx.

%package -n gstreamer0.10-pocketsphinx
Summary:	PocketSphinx automatic speech recognition plugin for GStreamer
Summary(pl.UTF-8):	Wtyczka automatycznego rozpoznawania mowy PocketSphinx dla GStreamera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer0.10 >= 0.10.0
Requires:	gstreamer0.10-plugins-base >= 0.10.0

%description -n gstreamer0.10-pocketsphinx
PocketSphinx automatic speech recognition plugin for GStreamer.

%description -n gstreamer0.10-pocketsphinx -l pl.UTF-8
Wtyczka automatycznego rozpoznawania mowy PocketSphinx dla GStreamera.

%package -n python-pocketsphinx
Summary:	Python interface to CMU PocketSphinx speech recognition
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki rozpoznawania mowy CMU PocketSphinx
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-pocketsphinx
Python interface to CMU PocketSphinx speech recognition.

%description -n python-pocketsphinx -l pl.UTF-8
Interfejs Pythona do biblioteki rozpoznawania mowy CMU PocketSphinx.

%package -n python-pocketsphinx-devel
Summary:	Header file for Python interface to CMU PocketSphinx library
Summary(pl.UTF-8):	Plik nagłówkowy interfejsu Pythona do biblioteki CMU Pocketsphinx
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-pocketsphinx = %{version}-%{release}
Requires:	python-devel >= 2.0

%description -n python-pocketsphinx-devel
Header file for Python interface to CMU PocketSphinx library.

%description -n python-pocketsphinx-devel -l pl.UTF-8
Plik nagłówkowy interfejsu Pythona do biblioteki CMU Pocketsphinx.

%prep
%setup -q

%build
# rebuild ac/am/lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_python:--without-python} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpocketsphinx.la

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/libgstpocketsphinx.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/libgstpocketsphinx.a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/pocketsphinx_*
%attr(755,root,root) %{_libdir}/libpocketsphinx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpocketsphinx.so.1
%dir %{_datadir}/pocketsphinx
%dir %{_datadir}/pocketsphinx/model
%dir %{_datadir}/pocketsphinx/model/hmm
%dir %{_datadir}/pocketsphinx/model/lm
%{_mandir}/man1/pocketsphinx_*.1*

%files model-en
%defattr(644,root,root,755)
%{_datadir}/pocketsphinx/model/hmm/en
%{_datadir}/pocketsphinx/model/hmm/en_US
%{_datadir}/pocketsphinx/model/lm/en
%{_datadir}/pocketsphinx/model/lm/en_US

%files model-zh
%defattr(644,root,root,755)
%{_datadir}/pocketsphinx/model/hmm/zh
%{_datadir}/pocketsphinx/model/lm/zh_CN
%{_datadir}/pocketsphinx/model/lm/zh_TW

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpocketsphinx.so
%dir %{_includedir}/pocketsphinx
%{_includedir}/pocketsphinx/*.h
%{_pkgconfigdir}/pocketsphinx.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpocketsphinx.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*

%files -n gstreamer0.10-pocketsphinx
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libgstpocketsphinx.so

%files -n python-pocketsphinx
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pocketsphinx.so
%{py_sitedir}/PocketSphinx-%{version}-py*.egg-info

%files -n python-pocketsphinx-devel
%defattr(644,root,root,755)
%{_includedir}/pocketsphinx/pocketsphinx.pxd
