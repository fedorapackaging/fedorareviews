#
##
# Default values are --with empty --with sqlite3 --with mysql --with postgresql
#                    --without oracle 
# Note that, for Oracle, when enabled, the following options should
# also be given:
# --with-oracle-include=/opt/oracle/app/oracle/product/11.1.0/db_1/rdbms/public
# --with-oracle-lib=/opt/oracle/app/oracle/product/11.1.0/db_1/lib
# If the macros are defined, redefine them with the correct compilation flags.
%bcond_without empty
%bcond_without sqlite3
%bcond_without mysql
%bcond_without postgresql
%bcond_with oracle

%define _default_oracle_dir /opt/oracle/app/oracle/product/11.1.0/db_1
%{!?_with_oracle_incdir: %define _with_oracle_incdir --with-oracle-include=%{_default_oracle_dir}/rdbms/public}
%{!?_with_oracle_libdir: %define _with_oracle_libdir --with-oracle-lib=%{_default_oracle_dir}/lib}
#
##
#
Name:           soci
Version:        3.1.0.rc1
Release:        1%{?dist}

Summary:        The database access library for C++ programmers

Group:          System Environment/Libraries
License:        Boost
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
%{?el5:BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}

BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  libtool

%description
SOCI is a C++ database access library that provides the
illusion of embedding SQL in regular C++ code, staying entirely within
the C++ standard.


%{?with_sqlite3:%package        sqlite3
Summary:        SQLite3 backend for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  sqlite-devel

%description    sqlite3
This package contains the SQLite3 backend for SOCI, i.e.,
dynamic library specific to the SQLite3 database. If you would like to
use SOCI in your programs with SQLite3, you will need to
install %{name}-sqlite3.}

%{?with_mysql:%package        mysql
Summary:        MySQL backend for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  mysql-devel

%description    mysql
This package contains the MySQL backend for SOCI, i.e.,
dynamic library specific to the MySQL database. If you would like to
use SOCI in your programs with MySQL, you will need to
install %{name}-mysql.}

%{?with_postgresql:%package        postgresql
Summary:        PostGreSQL backend for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:  postgresql-devel

%description    postgresql
This package contains the PostGreSQL backend for SOCI, i.e.,
dynamic library specific to the PostGreSQL database. If you would like
to use SOCI in your programs with PostGreSQL, you will need to
install %{name}-postgresql.}

%{?with_oracle:%package        oracle
Summary:        Oracle backend for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    oracle
This package contains the Oracle backend for SOCI, i.e.,
dynamic library specific to the Oracle database. If you would like to
use SOCI in your programs with Oracle, you will need to install
%{name}-oracle.}


%package        devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains the header files, dynamic libraries and
development documentation for %{name}. If you would like to develop
programs using %{name}, you will need to install %{name}-devel.

%{?with_sqlite3:%package        sqlite3-devel
Summary:        SQLite3 backend for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-sqlite3 = %{version}-%{release}
Requires:       sqlite-devel

%description    sqlite3-devel
This package contains the SQLite3 backend for %{name}, i.e., header
files and dynamic libraries specific to the SQLite3 database. If you
would like to develop programs using %{name} and SQLite3, you will need
to install %{name}-sqlite3.}

%{?with_mysql:%package        mysql-devel
Summary:        MySQL backend for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-mysql = %{version}-%{release}
Requires:       mysql-devel

%description    mysql-devel
This package contains the MySQL backend for %{name}, i.e., header
files and dynamic libraries specific to the MySQL database. If you
would like to develop programs using %{name} and MySQL, you will need
to install %{name}-mysql.}

%{?with_postgresql:%package        postgresql-devel
Summary:        PostGreSQL backend for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-postgresql = %{version}-%{release}
Requires:       postgresql-devel

%description    postgresql-devel
This package contains the PostGreSQL backend for %{name}, i.e., header
files and dynamic libraries specific to the PostGreSQL database. If
you would like to develop programs using %{name} and PostGreSQL, you
will need to install %{name}-postgresql.}

%{?with_oracle:%package        oracle-devel
Summary:        Oracle backend for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-oracle = %{version}-%{release}

%description    oracle-devel
This package contains the Oracle backend for %{name}, i.e., header
files and dynamic libraries specific to the Oracle database. If you
would like to develop programs using %{name} and Oracle, you will need
to install %{name}-oracle.}


%package doc
Summary:        HTML documentation for the SOCI library
Group:          Documentation
%{?fedora:BuildArch:      noarch}
#BuildRequires:  tex(latex)
#BuildRequires:  doxygen, ghostscript

%description doc
This package contains the documentation in the HTML format of the SOCI
library. The documentation is the same as at the SOCI web page.


%prep
%setup -q

# Rename change-log and license file, so that they comply with
# packaging standard
mv src/CHANGES ChangeLog
mv src/LICENSE_1_0.txt COPYING
mv src/README .
echo "Maciej Sobczak <prog@msobczak.com> and Mateusz Loskot <mateusz@loskot.net>" > AUTHORS
echo "Sat 18 Sep 2010 - Release 3.1.0" > NEWS
rm -f src/INSTALL

# Fix some permissions and formats
find ./doc -type f -perm 755 -exec chmod 644 {} \;
chmod -x AUTHORS ChangeLog COPYING NEWS README
# find . -type f -name '*.[hc]pp' -exec chmod 644 {} \;


%build
# Support for building tests.
%define soci_testflags -DBUILD_TESTS="NONE"
%if %{with tests}
  %define soci_testflags -DSOCI_TEST=ON \
   -DSOCI_TEST_EMPTY_CONNSTR="dummy" \
   -DSOCI_TEST_SQLITE3_CONNSTR="test.db" \
   -DSOCI_TEST_POSTGRESQL_CONNSTR:STRING="dbname=soci_test" \
   -DSOCI_TEST_MYSQL_CONNSTR:STRING="db=soci_test user=mloskot password=pantera"
%endif

( echo ============================= build serial ==================
  mkdir tmpbuild
  cd tmpbuild
  %cmake -DCMAKE_INSTALL_PREFIX:PATH=$RPM_BUILD_ROOT \
   -DSOCI_EMPTY=%{?with_empty:ON}%{?without_empty:OFF} \
   -DSOCI_SQLITE3=%{?with_sqlite3:ON}%{?without_sqlite3:OFF} \
   -DSOCI_POSTGRESQL=%{?with_postgresql:ON}%{?without_postgresql:OFF} \
   -DSOCI_MYSQL=%{?with_mysql:ON}%{?without_mysql:OFF} \
   -DWITH_ORACLE=%{?with_oracle:ON %{?_with_oracle_incdir} %{?_with_oracle_libdir}}%{?without_oracle:OFF} \
   %{soci_testflags} ../src
  make VERBOSE=1 %{?_smp_mflags}
  cd ..
)

%install
rm -rf $RPM_BUILD_ROOT
cd tmpbuild
make install
cd ..
##
#  Remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT/include/%{name}/config.h
rm -f $RPM_BUILD_ROOT/lib/lib%{name}_*.la
rm -f $RPM_BUILD_ROOT/lib/lib%{name}_*.a
mkdir -p $RPM_BUILD_ROOT%{_includedir} $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/include/soci $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/lib/lib* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%{?with_sqlite3:%post sqlite3 -p /sbin/ldconfig

%postun sqlite3 -p /sbin/ldconfig}

%{?with_mysql:%post mysql -p /sbin/ldconfig

%postun mysql -p /sbin/ldconfig}

%{?with_postgresql:%post postgresql -p /sbin/ldconfig

%postun postgresql -p /sbin/ldconfig}

%{?with_oracle:%post oracle -p /sbin/ldconfig

%postun oracle -p /sbin/ldconfig}



%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_core.so.*
%{?with_empty:%{_libdir}/lib%{name}_empty.so.*}

%{?with_sqlite3:%files sqlite3
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_sqlite3.so.*}

%{?with_mysql:%files mysql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_mysql.so.*}

%{?with_postgresql:%files postgresql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_postgresql.so.*}

%{?with_oracle:%files oracle
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/lib%{name}_oracle.so.*}


%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/*.h
%{?with_empty:%{_includedir}/%{name}/empty/}
%{_libdir}/lib%{name}_core.so
%{?with_empty:%{_libdir}/lib%{name}_empty.so}

%{?with_sqlite3:%files sqlite3-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/sqlite3/
%{_libdir}/lib%{name}_sqlite3.so}

%{?with_mysql:%files mysql-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/mysql
%{_libdir}/lib%{name}_mysql.so}

%{?with_postgresql:%files postgresql-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/postgresql
%{_libdir}/lib%{name}_postgresql.so}

%{?with_oracle:%files oracle-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/oracle
%{_libdir}/lib%{name}_oracle.so}


%files doc
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README doc


%changelog
* Sat Sep 17 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.1.0.rc1-1
- Upstream integration
- New CMake build system

* Tue Sep 07 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-18
- Fixed bug #631175 (https://bugzilla.redhat.com/show_bug.cgi?id=631175)

* Sat Jan 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-16
- Added a missing cstring header include for g++-4.4 compatibility

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 3.0.0-15
- Rebuild for Boost soname bump

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 09 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-13
- Introduced distinct dependencies for different distributions

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-12
- Removed the dependency on the version of Boost, and on CPPUnit

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-11
- Removed the dependency on Latex for documentation delivery

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-10
- Burried the Boost Fusion header include for core/test/common-tests.h

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-9
- Added a missing cstdio header include for g++-4.4 compatibility

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-8
- Added missing cstdio header includes for g++-4.4 compatibility

* Tue May 05 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-7
- Added a missing cstdio header include for g++-4.4 compatibility

* Sat May 02 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-6
- Removed the unused build conditionals

* Tue Apr 28 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-5
- Simplified the conditional build rules within the RPM specification file

* Sat Apr 18 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-4
- Fixed an issue about OPTFLAGS compilation

* Tue Apr 14 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-3
- Restarted from pristine version 3.0.0 of upstream (SOCI) project

* Sat Apr  4 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-2
- Specific RPM for each backend

* Fri Mar 27 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> 3.0.0-1
- First RPM release

