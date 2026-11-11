Boost 1.73 on RedHat/CentOS 8
=============================

# Overview

This directory gives the RPM specification file to package `boost1.73`.

Right now, the RPM specification is exactly the same as on Rawhide. It still
needs to be altered to embed the version into the package name, so as not
to collide with the pristine Boost (1.66) on RHEL/CentOS 8. 

## See also
* [Bugzilla #1828059 - Boost1.73 on EPEL](https://bugzilla.redhat.com/show_bug.cgi?id=1828059)
* [Spec file for `boost1.73`](https://github.com/fedorapackaging/fedorareviews/blob/master/reviews/boost/boost_xxx_boost173/boost1.73.spec)
* [Source RPM for `boost1.73-1.73.0-1`](https://denisarnaud.fedorapeople.org/boost/boost1.73/boost1.73-1.73.0-1.el8.src.rpm)
* [Boost1.73 on Copr](https://copr.fedorainfracloud.org/coprs/denisarnaud/boost1.73/)
* Successful builds:
  + [Boost1.73-1.73.0-1 (versioned package) on EPEL 8](https://koji.fedoraproject.org/koji/taskinfo?taskID=43816685)
  + [Boost-1.73.0 (standard package) on Rawhide](https://koji.fedoraproject.org/koji/taskinfo?taskID=43782815)
  + [Boost-1.73.0 (standard package) on EPEL 8](https://koji.fedoraproject.org/koji/taskinfo?taskID=43783760)
* [Supporting content](https://github.com/fedorapackaging/fedorareviews/blob/master/reviews/boost/boost_xxx_boost173/)


# Steps

## Build locally
* Retrieve the sources:
```bash
$ wget https://dl.bintray.com/boostorg/master/boost_1_73_0-snapshot.tar.gz -O ~/dev/packages/SOURCES/boost_1_73_0_rc1.tar.gz
```

* Copy the sources (patches) to `~/dev/packages/SOURCES/`:
```bash
$ cp boost1.73.spec ~/dev/packages/SPECS/boost1.73-1.73.0-1.spec
$ cp *.patch *.so ~/dev/packages/SOURCES/
$ pushd ~/dev/packages/SPECS/
$ ln -sf boost1.73-1.73.0-1.spec boost1.73.spec
$ popd
```

* Launch the build:
```bash
$ pushd ~/dev/packages/SPECS/
$ rpmbuild -bs boost1.73.spec
$ rpmbuild -ba boost1.73.spec
$ popd
```

## Build on Koji
* Launch a build on Koji:
```bash
$ koji build --arch-override=x86_64 --scratch --nowait epel8 ~/dev/packages/SRPMS/boost1.73-1.73.0-1.el8.src.rpm
Uploading srpm: /home/build/dev/packages/SRPMS/boost1.73-1.73.0-1.el8.src.rpm
[====================================] 100% 00:01:50 122.27 MiB   1.11 MiB/sec
Created task: 43816685
Task info: https://koji.fedoraproject.org/koji/taskinfo?taskID=43816685
```

* Resulting build: https://koji.fedoraproject.org/koji/taskinfo?taskID=43816685


