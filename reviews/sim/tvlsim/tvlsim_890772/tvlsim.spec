#
%global mydocs __tmp_docdir
#
Name:           tvlsim
Version:        1.01.1
Release:        1%{?dist}

Summary:        Travel Market Simulator

License:        LGPLv2+
URL:            http://github.com/airsim/%{name}
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  readline-devel
BuildRequires:  zeromq-devel
BuildRequires:  cppzmq-devel
BuildRequires:  sevmgr-devel
BuildRequires:  soci-mysql-devel
BuildRequires:  soci-sqlite3-devel
BuildRequires:  stdair-devel
BuildRequires:  airrac-devel
BuildRequires:  rmol-devel
BuildRequires:  python3-rmol
BuildRequires:  sevmgr-devel
BuildRequires:  /usr/bin/epstopdf
BuildRequires:  airtsp-devel
BuildRequires:  simfqt-devel
BuildRequires:  airinv-devel
BuildRequires:  simcrs-devel
BuildRequires:  trademgen-devel
BuildRequires:  python3-trademgen
BuildRequires:  travelccm-devel


%description
The Travel Market Simulator project aims at providing reference implementation,
mainly in C++, of a travel market simulator, focusing on revenue management (RM)
for airlines. It is intended to be used for applied research activities only:
it is by no way intended to be used by production systems. It is a new breed of
software and aims to become the new generation PODS (http://podsresearch.com/),
which was instrumental in the inception of the Travel Market Simulator project.

Over a dozen components have been implemented and are fully functional,
encompassing for instance (but not limited to) traveler demand generation
(booking requests), travel distribution (GDS/CRS), low fare search (LFS),
price calculation and inventory availability calculation), customer choice
modeling (CCM), revenue management (RM), schedule and inventory management,
revenue accounting (RA).

The Travel Market Simulator can be used in either batch or hosted mode.
It is the main component of the Travel Market Simulator:
http://www.travel-market-simulator.com

%{name} makes an extensive use of existing open-source libraries for
increased functionality, speed and accuracy. In particular the
Boost (C++ Standard Extensions: http://www.boost.org) library is used.

The %{name} component itself aims at providing a clean API and a simple
implementation, as a C++ library, of a full travel market simulator,
focusing on revenue management (RM) for airlines. That library uses
the Standard Airline IT C++ object model (http://sf.net/projects/stdair).

Install the %{name} package if you need a library of basic C++ objects
for airline-related travel market simulation.

%package        devel
Summary:        Header files, libraries and development helper tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, shared libraries and
development helper tools for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%package        doc
Summary:        HTML documentation for the %{name} library
BuildArch:      noarch
BuildRequires:  tex(latex)
BuildRequires:  doxygen
BuildRequires:  ghostscript

%description    doc
This package contains HTML pages, as well as a PDF reference manual,
for %{name}. All that documentation is generated thanks to Doxygen
(http://doxygen.org). The content is the same as what can be browsed
online (http://%{name}.org).


%prep
%autosetup -n %{name}-%{name}-%{version} 


%build
%cmake .
%make_build

%install
%make_install

mkdir -p %{mydocs}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/html %{mydocs}
rm -f %{mydocs}/html/installdox

# Remove additional documentation files (those files are already available
# in the project top directory)
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/{NEWS,README,AUTHORS}

%check
#ctest



%files
%doc AUTHORS ChangeLog COPYING NEWS README.md
%{_bindir}/%{name}
%{_bindir}/simulate
%{_bindir}/TvlSimServer
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/simulate.1.*
%{_mandir}/man1/TvlSimServer.1.*

%files devel
%{_includedir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/CMake
%{_mandir}/man1/%{name}-config.1.*
%{_mandir}/man3/%{name}-library.3.*

%files doc
%doc %{mydocs}/html
%doc COPYING


%changelog
* Thu Jan 17 2019 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.01.1-1
- Upstream update

* Sat Apr 18 2015 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.00.0-4
- On Fedora 22+, ZeroMQ v2 is no longer the default.

* Sat Aug 31 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.00.0-3
- Took into account the remaining feedbacks of the review request (#890772)

* Mon Jul 29 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.00.0-2
- Fixed the docdir issue, following the F20 System Wide Change
- Rebuild for boost 1.54.0

* Sat Dec 29 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.00.0-1
- First RPM release
