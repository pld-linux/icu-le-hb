#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	ICU Layout Engine API on top of HarfBuzz shaping library
Summary(pl.UTF-8):	API ICU Layout Engine oparte na bibliotece tworzenia kształtów HarfBuzz
Name:		icu-le-hb
Version:	2.0.0
Release:	3
License:	ICU (MIT-like)
Group:		Libraries
Source0:	https://github.com/harfbuzz/icu-le-hb/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e8266e20d122ce872e199f7b7fb4b10b
URL:		http://www.freedesktop.org/wiki/HarfBuzz
BuildRequires:	autoconf >= 2.56
BuildRequires:	autoconf-archive
BuildRequires:	automake >= 1:1.9
BuildRequires:	harfbuzz-devel >= 2.0.0
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	harfbuzz >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
icu-le-hb is a library implementing the ICU Layout Engine (icu-le) API
using external HarfBuzz library for implementation. This is useful as
a compatibility layer to make applications using ICU Layout Engine to
use HarfBuzz without porting them to use the HarfBuzz API.

%description -l pl.UTF-8
icu-le-hb to biblioteka implementująca API ICU Layout Engine (icu-le)
przy użyciu zewnętrznej biblioteki HarfBuzz. Jest przydatna jako
warstwa zgodności, aby aplikacje wykorzystujące silnik ICU Layout
Engine mogły używać biblioteki HarfBuzz bez potrzeby portowania do API
biblioteki HarfBuzz.

%package devel
Summary:	Header files for icu-le-hb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki icu-le-hb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	harfbuzz-devel >= 2.0.0
Requires:	libicu-devel
Requires:	libstdc++-devel

%description devel
Header files for icu-le-hb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki icu-le-hb.

%package static
Summary:	Static icu-le-hb library
Summary(pl.UTF-8):	Statyczna biblioteka icu-le-hb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static icu-le-hb library.

%description static -l pl.UTF-8
Statyczna biblioteka icu-le-hb.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libicu-le-hb.la

# conflict with libicu-devel (or: split libicu and package it in subpackage)
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/icu-le.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/libicu-le-hb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libicu-le-hb.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libicu-le-hb.so
%{_includedir}/icu-le-hb
%{_pkgconfigdir}/icu-le-hb.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libicu-le-hb.a
%endif
