%{?_javapackages_macros:%_javapackages_macros}
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

Name:       plexus-compiler
Version:    2.4
Release:    1.2
Epoch:      0
Summary:    Compiler call initiators for Plexus
Group:	    Development/Java
# extras subpackage has a bit different licensing
# parts of compiler-api are ASL2.0/MIT
License:    MIT and ASL 2.0
URL:        http://plexus.codehaus.org/

Source0:    https://github.com/sonatype/%{name}/archive/%{name}-%{version}.tar.gz
Source1:    http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:    LICENSE.MIT

BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugins:maven-gpg-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compilers:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.tycho:org.eclipse.jdt.core)


%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{name}-extras package.

%package extras
Summary:        Extra compiler support for %{name}
# ASL 2.0: src/main/java/org/codehaus/plexus/compiler/util/scan/
#          ...codehaus/plexus/compiler/csharp/CSharpCompiler.java
# ASL 1.1/MIT: ...codehaus/plexus/compiler/jikes/JikesCompiler.java
License:        MIT and ASL 2.0 and ASL 1.1

%description extras
Additional support for csharp, eclipse and jikes compilers

%package pom
Summary:        Maven POM files for %{name}

%description pom
This package provides %{summary}.

%package javadoc
Summary:        Javadoc for %{name}
License:        MIT and ASL 2.0 and ASL 1.1

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp %{SOURCE1} LICENSE
cp %{SOURCE2} LICENSE.MIT

%pom_disable_module plexus-compiler-aspectj plexus-compilers/pom.xml
# missing com.google.errorprone:error_prone_core
%pom_disable_module plexus-compiler-javac-errorprone plexus-compilers

# don't build/install compiler-test module, it needs maven2 test harness
%pom_disable_module plexus-compiler-test

%build
%mvn_package ":plexus-compiler{,s}" pom
%mvn_package ":*{csharp,eclipse,jikes}*" extras
# Tests are skipped because of unavailable plexus-compiler-test artifact
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE LICENSE.MIT
%files extras -f .mfiles-extras
%files pom -f .mfiles-pom

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE.MIT

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-4
- Fix license tag
- Install MIT license file

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-3
- Remove auxiliary aliases

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-2
- Add auxiliary aliases

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.2-1
- Update to upstream version 2.2
- Add license file (Resolves: #903268)

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.1-3
- Remove auxiliary aliases

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.1-2
- Build with original POM files

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-1
- Update to upstream version 2.1
- Build with xmvn

* Wed Dec 5 2012 Michal Srb <msrb@redhat.com> - 0:1.9.2-3
- Replaced dependency to plexus-container-default with plexus-containers-container-default

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.2-2
- Fix up licensing properly

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-1
- Update to upstream version 1.9.2

* Wed Aug  8 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-3
- Fix FTBFS by adding ignoreOptionalProblems function
- Use new pom_ macros instead of patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-1
- Update to upstream 1.9.1 release

* Fri Jan 13 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.3-1
- Update to upstream 1.8.3 release.
- For some reason junit is strong (not test) dependency.

* Thu Dec  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-3
- Build with maven 3
- Don't install compiler-test module (nothing should use it anyway)
- Fixes accoding to current guidelines
- Install depmaps into extras separately

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-1
- Update to latest version (1.8)
- Create extras subpackage with optional compilers
- Provide maven depmaps
- Versionless jars & javadocs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-2.3
- drop repotag

* Thu Mar 15 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.2
- Fix bug in spec that prevented unversioned symlink creation

* Thu Mar 08 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.1
- Fix license
- Disable aspectj compiler until we can put that into Fedora
- Remove vendor and distribution tags
- Removed javadoc post and postuns, with dirs being marked %%doc now
- Fix buildroot per Fedora spec

* Fri Jun 02 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-2jpp
- Fix jar naming to previous plexus conventions

* Tue May 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-1jpp
- First JPackage build
