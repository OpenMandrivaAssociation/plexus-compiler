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

%global parent  plexus
%global dirhash a7f8290
%global githash 7ca7d76

Name:       plexus-compiler
Version:    1.8
Release:    4
Summary:    Compiler call initiators for Plexus
License:    MIT
Group:      Development/Java
URL:        http://plexus.codehaus.org/

# wget  https://nodeload.github.com/sonatype/plexus-components/tarball/plexus-compiler-1.8
Source0:    sonatype-plexus-components-%{name}-%{version}-0-g%{githash}.tar.gz

Patch0:     0001-Remove-aspecj-support.patch

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  jpackage-utils
BuildRequires:  junit
BuildRequires:  classworlds
BuildRequires:  eclipse-ecj
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-containers-component-metadata

Requires:       classworlds
Requires:       plexus-container-default
Requires:       plexus-utils

%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{name}-extras package.

%package extras
Summary:        Extra compiler support for %{name}
Group:          Development/Java
Requires:       jpackage-utils
Requires:       eclipse-ecj
Requires:       %{name} = %{version}-%{release}

%description extras
Additional support for csharp, eclipse and jikes compilers

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n sonatype-plexus-components-%{dirhash}
%patch0 -p1

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:aggregate


%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/%{parent}
install -d -m 755 %{buildroot}%{_mavenpomdir}

for mod in plexus-compiler-{api,test,manager}; do
    jarname=${mod/plexus-}
    install -pm 644 $mod/target/${mod}-%{version}.jar \
                    %{buildroot}%{_javadir}/%{parent}/$jarname.jar

    install -pm 644 $mod/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-$jarname.pom
    %add_to_maven_depmap org.codehaus.plexus $mod %{version} JPP/%{parent} $jarname
done

pushd plexus-compilers
for mod in plexus-compiler-{csharp,eclipse,jikes,javac}; do
    jarname=${mod/plexus-}
    install -pm 644 $mod/target/${mod}-%{version}.jar \
                    %{buildroot}%{_javadir}/%{parent}/$jarname.jar

    install -pm 644 $mod/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-$jarname.pom
    %add_to_maven_depmap org.codehaus.plexus $mod %{version} JPP/%{parent} $jarname
done

install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-compilers.pom
%add_to_maven_depmap org.codehaus.plexus plexus-compilers %{version} JPP/%{parent} compilers
popd

install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-compiler.pom
%add_to_maven_depmap org.codehaus.plexus plexus-compiler %{version} JPP/%{parent} compiler


# javadocs
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%{_javadir}/%{parent}/compiler-api.jar
%{_javadir}/%{parent}/compiler-manager.jar
%{_javadir}/%{parent}/compiler-test.jar
%{_javadir}/%{parent}/compiler-javac.jar
%{_mavenpomdir}/*.pom
%{_mavendepmapfragdir}/%{name}

%files extras
%defattr(-,root,root,-)
%{_javadir}/%{parent}/compiler-csharp.jar
%{_javadir}/%{parent}/compiler-eclipse.jar
%{_javadir}/%{parent}/compiler-jikes.jar

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

