Name: tdlib
Version: 1.8.0
Release: 7%{?dist}

License: BSL-1.0
URL: https://github.com/%{name}/td
Summary: Cross-platform library for building Telegram clients
#Source0: %{url}/archive/v%{version}/
Source0: %{name}-%{version}.tar.gz

BuildRequires: gperftools-devel
BuildRequires: openssl-devel
BuildRequires: ninja-build
BuildRequires: zlib-devel
BuildRequires: gcc-c++
BuildRequires: gperf
BuildRequires: cmake
BuildRequires: gcc
BuildRequires: java-devel

Provides: bundled(sqlite) = 3.31.0

# Building with default settings require at least 16 GB of free RAM.
# Builds on ARM and other low-memory architectures are failing.
ExclusiveArch: x86_64 aarch64

%description
TDLib (Telegram Database library) is a cross-platform library for
building Telegram clients. It can be easily used from almost any
programming language.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%package static
Summary: Static libraries for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%description static
%{summary}.

%prep
%autosetup -p1
sed -e 's/"DEFAULT"/"PROFILE=SYSTEM"/g' -i tdnet/td/net/SslStream.cpp

%build
%{set_build_flags}
%__cmake \
        %{!?__cmake_in_source_build:-S "%{_vpath_srcdir}"} \
        %{!?__cmake_in_source_build:-B "%{__cmake_builddir}"} \
    -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_FULL_SBINDIR:PATH=%{_bindir} -DCMAKE_INSTALL_SBINDIR:PATH=`basename %{_bindir}` -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} -DLIB_INSTALL_DIR:PATH=%{_libdir} -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} -DLIB_SUFFIX=64 -DBUILD_SHARED_LIBS:BOOL=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_LIBDIR=%{_libdir}


    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DCMAKE_INSTALL_BINDIR=%{_bindir} \
    -DTD_ENABLE_JNI:BOOL=ON \
    -DTD_ENABLE_DOTNET:BOOL=OFF \
    -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
    -DLIB_SUFFIX=64 \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DTD_INSTALL_STATIC_LIBRARIES:BOOL=ON \
    -DTD_INSTALL_SHARED_LIBRARIES:BOOL=ON

%cmake_build

%install
%cmake_install

%files
%license LICENSE_1_0.txt
%doc README.md CHANGELOG.md
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/td
%{_libdir}/lib*.so
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/lib*.a
