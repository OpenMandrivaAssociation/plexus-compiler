# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define grname      plexus
%define gcj_support 1

Name:       plexus-compiler
Version:    1.5.2
Release:    %mkrel 2.2.2
Epoch:      0
Summary:    Compiler call initiators for Plexus
License:    MIT
Group:      Development/Java
URL:        http://plexus.codehaus.org/
# svn export svn://svn.plexus.codehaus.org/plexus/tags/plexus-compiler-1.5.2
# tar czf plexus-compiler-1.5.2.tar.gz plexus-compiler-1.5.2
Source0:    plexus-compiler-1.5.2.tar.gz

Source1:    plexus-compiler-1.5.2-api-build.xml
Source2:    plexus-compiler-1.5.2-compilers-aspectj-build.xml
Source3:    plexus-compiler-1.5.2-compilers-csharp-build.xml
Source4:    plexus-compiler-1.5.2-compilers-eclipse-build.xml
Source5:    plexus-compiler-1.5.2-compilers-javac-build.xml
Source6:    plexus-compiler-1.5.2-compilers-jikes-build.xml
Source7:    plexus-compiler-1.5.2-compilers-parent-build.xml
Source8:    plexus-compiler-1.5.2-manager-build.xml
Source9:    plexus-compiler-1.5.2-parent-build.xml
Source10:   plexus-compiler-1.5.2-test-build.xml

Patch0:     plexus-compiler-1.5.2-JikesCompiler.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps >= 0:1.6
BuildRequires:  junit
BuildRequires:  classworlds
BuildRequires:  eclipse-ecj
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
#BuildRequires:  aspectj >= 0:1.2
#BuildRequires:  junit
#Requires:       aspectj >= 0:1.2
Requires:       classworlds
Requires:       eclipse-ecj
Requires:       plexus-container-default
Requires:       plexus-utils

%description
Plexus Compiler adds support for using various compilers from a unified api.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n plexus-compiler-1.5.2
cp %{SOURCE1} plexus-compiler-api/build.xml
cp %{SOURCE2} plexus-compilers/plexus-compiler-aspectj/build.xml
cp %{SOURCE3} plexus-compilers/plexus-compiler-csharp/build.xml
cp %{SOURCE4} plexus-compilers/plexus-compiler-eclipse/build.xml
cp %{SOURCE5} plexus-compilers/plexus-compiler-javac/build.xml
cp %{SOURCE6} plexus-compilers/plexus-compiler-jikes/build.xml
cp %{SOURCE7} plexus-compilers/build.xml
cp %{SOURCE8} plexus-compiler-manager/build.xml
cp %{SOURCE9} build.xml
cp %{SOURCE10} plexus-compiler-test/build.xml

%patch0 -b .sav

%build
pushd plexus-compiler-api
mkdir -p target/lib
build-jar-repository -s -p target/lib \
    plexus/utils \
    plexus/container-default \
    classworlds

%{ant} jar javadoc
popd

pushd plexus-compiler-manager
mkdir -p target/lib
cp ../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
build-jar-repository -s -p target/lib \
    plexus/container-default \
    plexus/utils \
    classworlds
%{ant} jar javadoc
popd

#pushd plexus-compiler-test
## requires maven2
#mkdir -p target/lib
#cp ../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
#build-jar-repository -s -p target/lib \
#    maven \
#    plexus/utils \
#    plexus/container-default \
#    classworlds \
#    junit
#%{ant} jar javadoc
#popd

pushd plexus-compilers

# FIXME: aspectj compiler disabled until Fedora gets aspectj. 
# NOTE: Upstream does NOT build this by default anyways..

# requires aspectj-1.5.0
#pushd plexus-compiler-aspectj
# tests require plexus-compiler-test, which requires maven2 in turn
#rm -rf src/test/java/*
#
#mkdir -p target/lib
#cp ../../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
#build-jar-repository -s -p target/lib \
#    plexus/container-default \
#    plexus/utils \
#    classworlds \
#    aspectjtools \
#    aspectjrt
#%{ant} jar javadoc
#popd

pushd plexus-compiler-csharp
mkdir -p target/lib
cp ../../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
build-jar-repository -s -p target/lib \
    plexus/utils \
    plexus/container-default \
    classworlds \
    ant \
    ant/ant-nodeps
%{ant} jar javadoc
popd
pushd plexus-compiler-eclipse
# tests require plexus-compiler-test, which requires maven2 in turn
rm -rf src/test/java/*
#
mkdir -p target/lib
cp ../../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
build-jar-repository -s -p target/lib \
    plexus/utils \
    plexus/container-default \
    classworlds \
    jdtcore
%{ant} jar javadoc
popd
pushd plexus-compiler-javac
# tests require plexus-compiler-test, which requires maven2 in turn
rm -rf src/test/java/*
#
mkdir -p target/lib
cp ../../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
build-jar-repository -s -p target/lib \
    plexus/utils \
    plexus/container-default \
    classworlds
%{ant} jar javadoc
popd
pushd plexus-compiler-jikes
# tests require plexus-compiler-test, which requires maven2 in turn
rm -rf src/test/java/*
#
mkdir -p target/lib
cp ../../plexus-compiler-api/target/plexus-compiler-api-1.5.2.jar target/lib/
build-jar-repository -s -p target/lib \
    plexus/utils \
    plexus/container-default \
    classworlds
%{ant} jar javadoc
popd
popd

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 %{name}-api/target/%{name}-api-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-api-%{version}.jar
#install -pm 644 %{name}-test/target/%{name}-test-%{version}.jar \
#  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-test-%{version}.jar
install -pm 644 %{name}-manager/target/%{name}-manager-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-manager-%{version}.jar
#install -pm 644 %{grname}-compilers/plexus-compiler-aspectj/target/%{name}-aspectj-%{version}.jar \
#  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-aspectj-%{version}.jar
install -pm 644 %{grname}-compilers/plexus-compiler-csharp/target/%{name}-csharp-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-csharp-%{version}.jar
install -pm 644 %{grname}-compilers/plexus-compiler-eclipse/target/%{name}-eclipse-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-eclipse-%{version}.jar
install -pm 644 %{grname}-compilers/plexus-compiler-javac/target/%{name}-javac-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-javac-%{version}.jar
install -pm 644 %{grname}-compilers/plexus-compiler-jikes/target/%{name}-jikes-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{grname}/compiler-jikes-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/%{grname}
    for jar in *-%{version}*; do 
        ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; 
    done
)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/manager
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/test
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/aspectj
install -d -m 755 \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/csharp
install -d -m 755 \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/eclipse
install -d -m 755 \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/javac
install -d -m 755 \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/jikes
cp -pr %{name}-api/target/docs/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
cp -pr %{name}-manager/target/docs/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/manager
#cp -pr %{name}-test/target/docs/apidocs/* \
#    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/test
#cp -pr %{grname}-compilers/%{name}-aspectj/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/aspectj
cp -pr %{grname}-compilers/%{name}-csharp/target/docs/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/csharp
cp -pr %{grname}-compilers/%{name}-eclipse/target/docs/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/eclipse
cp -pr %{grname}-compilers/%{name}-javac/target/docs/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/javac
cp -pr %{grname}-compilers/%{name}-jikes/target/docs/apidocs/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/compilers/jikes
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{grname}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*
