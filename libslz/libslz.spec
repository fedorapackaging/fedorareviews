Name:		libslz
Version:	1.1.0
Release:	1%{?dist}
Summary:	StateLess Zip

Group:		System Environment/Libraries
License:	MIT
# TODO when upstream is ready
# URL:		http://libslz.org/
URL:		http://1wt.eu/projects/libslz/
# The tarball is currently generated manually until source tarballs
# are distributed upstream:
# V=%%version
# git archive --format=tgz --prefix=libtgz-$V/ --output=libslz-$V.tar.gz v$V
Source:		http://git.1wt.eu/web?p=%{name}.git;a=snapshot;h=v%{version};sf=tgz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc

%description
SLZ is a fast and memory-less stream compressor which produces an output that
can be decompressed with zlib or gzip. It does not implement decompression at
all, zlib is perfectly fine for this.

The purpose is to use SLZ in situations where a zlib-compatible stream is
needed and zlib's resource usage would be too high while the compression ratio
is not critical. The typical use case is in HTTP servers and gateways which
have to compress many streams in parallel with little CPU resources to assign
to this task, and without having to limit the compression ratio due to the
memory usage. In such an environment, the server's memory usage can easily be
divided by 10 and the CPU usage by 3.


%package devel

Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}


%description devel
Development files for SLZ, the zenc and zdec commands that respectively
compress using SLZ and dump the decoding process.


%prep
%setup -q -n %{name}


%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%__global_ldflags"


%install
strip libslz.so.1
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
chmod +x %{buildroot}%{_libdir}/*.so.*
rm %{buildroot}%{_libdir}/*.a


%files
%doc README
%license LICENSE
%{_libdir}/*.so.*


%files devel
%{_libdir}/*.so
%{_bindir}/*
%{_includedir}/*


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
* Sun Sep 25 2016 - Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 1.1.0-1
- Initial spec.
