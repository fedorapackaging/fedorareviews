#
%global mydocs __tmp_docdir
%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
#
Name:           opentrep
Version:        0.6.0
Release:        1%{?dist}

Summary:        C++ library providing a clean API for parsing travel-focused requests

Group:          System Environment/Libraries 
License:        LGPLv2+
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  cmake, python-devel, xapian-core-devel
BuildRequires:  boost-devel, libicu-devel

%description
%{name} aims at providing a clean API, and the corresponding C++
implementation, for parsing travel-focused requests.

%{name} uses Xapian (http://www.xapian.org) for the Information Retrieval part,
on freely available travel-related data (e.g., country names and codes,
city names and codes, airline names and codes, etc.).

%{name} exposes a simple, clean and object-oriented, API. For instance,
the static Parse() method takes, as input, a string containing the travel
request, and yields, as output, the list of the recognized terms as well as
their corresponding types. As an example, the travel request
"Washington DC Beijing Monday a/r +AA -UA 1 week 2 adults 1 dog" would give
the following list:
 * Origin airport: Washington, DC, USA
 * Destination airport: Beijing, China
 * Date of travel: next Monday
 * Date of return: 1 week after next Monday
 * Preferred airline: American Airlines; non-preferred airline: United Airlines
 * Number of travelers: 2 adults and a dog

The output can then be used by other systems, for instance to book the
corresponding travel or to visualize it on a map and calendar and to
share it with others.

%{name} makes an extensive use of existing open-source libraries for
increased functionality, speed and accuracy. In particular the
Boost (C++ Standard Extensions: http://www.boost.org) library is used.

%package        devel
Summary:        Header files, libraries and development helper tools for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, shared libraries and
development helper tools for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%package        doc
Summary:        HTML documentation for the %{name} library
Group:          Documentation
%if 0%{?fedora} || 0%{?rhel} > 5
BuildArch:      noarch
%endif
BuildRequires:  tex(latex), tex(sectsty.sty), tex(tocloft.sty), tex(xtab.sty)
BuildRequires:  texlive-collection-langcyrillic, texlive-cyrillic
BuildRequires:  doxygen, ghostscript

%description    doc
This package contains HTML pages, as well as a PDF reference manual,
for %{name}. All that documentation is generated thanks to Doxygen
(http://doxygen.org). The content is the same as what can be browsed
online (http://%{name}.org).


%prep
%setup -q


%build
%cmake .
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# From rpm version > 4.9.1, it may no longer be necessary to move the
# documentation out of the docdir path, as the %%doc macro no longer
# deletes the full directory before installing files into it.
mkdir -p %{mydocs}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{mydocs}
rm -f %{mydocs}/html/installdox

# Remove additional documentation files (those files are already available
# in the project top directory)
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{NEWS,README,AUTHORS}

# Python executable
install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}/
install -pm 0755 $RPM_BUILD_ROOT%{_bindir}/py%{name} $RPM_BUILD_ROOT%{python_sitelib}/%{name}/
rm -f $RPM_BUILD_ROOT%{_bindir}/py%{name}
# Python module (library)
install -d $RPM_BUILD_ROOT%{python_sitearch}/libpy%{name}
mv $RPM_BUILD_ROOT%{_libdir}/libpy%{name}.so* $RPM_BUILD_ROOT%{python_sitearch}/libpy%{name}/
mv $RPM_BUILD_ROOT%{_libdir}/python/%{name}/Travel_pb2.py* $RPM_BUILD_ROOT%{python_sitearch}/libpy%{name}/
chmod 644 $RPM_BUILD_ROOT%{python_sitearch}/libpy%{name}/Travel_pb2.py*

%check
#ctest

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}-indexer
%{_bindir}/%{name}-searcher
%{_bindir}/%{name}-dbmgr
%{_libdir}/lib%{name}.so.*
%{python_sitelib}/%{name}/
%{python_sitearch}/libpy%{name}/
%{_mandir}/man1/py%{name}.1.*
%{_mandir}/man1/%{name}-indexer.1.*
%{_mandir}/man1/%{name}-searcher.1.*
%{_mandir}/man1/%{name}-dbmgr.1.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data
%dir %{_datadir}/%{name}/data/por
%{_datadir}/%{name}/data/por/ori_por_public.csv
%{_datadir}/%{name}/data/por/create_ori_por_public_schema.sql
%{_datadir}/%{name}/data/por/ori_por_public.db
%{_datadir}/%{name}/data/por/ori_por_public_4_test.csv
%{_datadir}/%{name}/data/por/test_ori_por_public.csv
%{_datadir}/%{name}/data/por/test_ori_por_public_schema.sql


%files devel
%{_includedir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/%{name}/CMake
%{_mandir}/man1/%{name}-config.1.*
%{_mandir}/man3/%{name}-library.3.*

%files doc
%doc %{mydocs}/html
%doc COPYING


%changelog
* Sun Feb 02 2014 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.6.0-1
- Upstream update

* Mon Aug 12 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.5.3-3
- Took into account a part of the feedbacks from review request (BZ#866265):
  opentrep-config now supports multilib (32 and 64bit versions).
- Upstream update

* Mon Jul 29 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.5.3-2
- Fixed the docdir issue, following the F20 System Wide Change
- Rebuild for boost 1.54.0

* Sun Mar 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.3-1
- Upstream update

* Sun Feb 17 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.2-1
- Upstream update

* Thu Oct 25 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.0-2
- Took into account review request #866265 feedback

* Sun Oct 14 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.5.0-1
- Upstream update

* Tue Nov 01 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.4.0-1
- The build system is now based on CMake (instead of the GNU Autotools)

* Sun Mar 29 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.3.0-1
- Now relies on the new SOCI RPM

* Sun Mar 22 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.2.0-1
- RPM release for Fedora 10

