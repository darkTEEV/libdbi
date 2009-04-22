#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_without	doc			# don't build documentation
#
Summary:	Database Independent Abstraction Layer for C
Summary(pl.UTF-8):	Warstwa DBI dla C
Name:		libdbi
%define	_snap	20090420
Version:	0.8.4
Release:	0.%{_snap}.1
License:	LGPL v2+
Group:		Libraries
#Source0:	http://dl.sourceforge.net/libdbi/%{name}-%{version}.tar.gz
Source0:	%{name}-%{_snap}.tar.gz
# Source0-md5:	dcd546b78d4d406520caf802b24ec7c6
Patch0:		%{name}-borked_snapshot.patch
URL:		http://libdbi.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%if %{with doc}
BuildRequires:	jadetex
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	texlive-fonts-ams
BuildRequires:	texlive-fonts-type1-urw
BuildRequires:	texlive-fonts-stmaryrd
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdbi implements a database-independent abstraction layer in C,
similar to the DBI/DBD layer in Perl. Writing one generic set of code,
programmers can leverage the power of multiple databases and multiple
simultaneous database connections by using this framework.

%description -l pl.UTF-8
libdbi jest implementacją w C warstwy abstrakcyjnej niezależnej od
bazy danych, podobnej do warstwy DBI/DBD w Perlu. Używając tego
środowiska programista może za pomocą jednego, wspólnego kodu
odwoływać się do wielu różnych baz danych, także jednocześnie.

%package devel
Summary:	Development files for Database Independent Abstraction Layer for C
Summary(pl.UTF-8):	Pliki dla programistów używających warstwy DBI w C
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The libdbi-devel package contains the header files and documentation
needed to develop applications with libdbi.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i dokumentację do tworzenia
aplikacji z użyciem libdbi.

%package static
Summary:	Static Database Independent Abstraction Layer for C libraries
Summary(pl.UTF-8):	Statyczne biblioteki warstwy DBI w C
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Database Independent Abstraction Layer for C libraries.

%description static -l pl.UTF-8
Statyczne biblioteki warstwy DBI w C.

%prep
%setup -q -n %{name}
#snapshot hack below
touch doc/libdbi-versioning.sgml
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{!?with_doc:--disable-docs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/dbd,%{_pkgconfigdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cat >$RPM_BUILD_ROOT/%{_pkgconfigdir}/dbi.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/dbi

Name: libdbi
Description: database-independent abstraction layer in C
Version: %{version}
Libs: -L\${libdir} -ldbi
Cflags: -I\${includedir} -I\${includedir}/dbi
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libdbi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbi.so.0
%dir %{_libdir}/dbd

%files devel
%defattr(644,root,root,755)
%if %{with doc}
%doc doc/driver-guide doc/programmers-guide doc/programmers-guide.pdf
%endif
%attr(755,root,root) %{_libdir}/libdbi.so
%{_libdir}/libdbi.la
%{_includedir}/dbi
%{_pkgconfigdir}/dbi.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdbi.a
%endif
