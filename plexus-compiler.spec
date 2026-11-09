Name:		plexus-compiler
Version:	2.18.0
Release:	1
Summary:	Uniform API for invoking Java compilers
Group:		Development/Java
License:	MIT AND Apache-2.0
URL:		https://github.com/codehaus-plexus/plexus-compiler
Source0:	https://github.com/codehaus-plexus/plexus-compiler/archive/refs/tags/plexus-compiler-%{version}.tar.gz#/plexus-compiler-%{version}.tar.gz
Source1:	LICENSE-2.0.txt
Source2:	LICENSE.MIT
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildSystem:	maven

Obsoletes:	plexus-compiler-extras < %{EVRD}
Obsoletes:	plexus-compiler-pom < %{EVRD}
Provides:	plexus-compiler-pom = %{EVRD}
Obsoletes:	plexus-compiler-javadoc < %{EVRD}

%description
Invokes javac through one API. 2.18 accepts a 1.8 release version and
passes 8 to javac --release. The package ships the API, the manager,
and the javac compiler. Eclipse, AspectJ, Error Prone, and C# are not
built. Tests need JUnit Jupiter, so they are not run.

%prep
%autosetup -n plexus-compiler-plexus-compiler-%{version}
rm -rf .github src plexus-compiler-test plexus-compiler-its
rm -rf plexus-compilers/plexus-compiler-aspectj plexus-compilers/plexus-compiler-csharp plexus-compilers/plexus-compiler-eclipse plexus-compilers/plexus-compiler-javac-errorprone plexus-compilers/pom.xml
rm -rf plexus-compiler-api/src/test plexus-compiler-manager/src/test plexus-compilers/plexus-compiler-javac/src/test
cp -p %{SOURCE1} LICENSE-2.0.txt
cp -p %{SOURCE2} LICENSE.MIT
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

def dep(deps, group, artifact, version):
    node = ET.SubElement(deps, tag("dependency"))
    add(node, "groupId", group)
    add(node, "artifactId", artifact)
    add(node, "version", version)

def write(path, artifact, parent_rel, modules, deps, title):
    root = ET.Element(tag("project"))
    add(root, "modelVersion", "4.0.0")
    if parent_rel:
        parent = ET.SubElement(root, tag("parent"))
        add(parent, "groupId", "org.codehaus.plexus")
        add(parent, "artifactId", "plexus-compiler")
        add(parent, "version", "%{version}")
        add(parent, "relativePath", parent_rel)
    else:
        add(root, "groupId", "org.codehaus.plexus")
        add(root, "version", "%{version}")
        add(root, "packaging", "pom")
    add(root, "artifactId", artifact)
    add(root, "name", title)
    if not parent_rel:
        props = ET.SubElement(root, tag("properties"))
        add(props, "maven.compiler.release", "8")
        add(props, "project.build.sourceEncoding", "UTF-8")
    if modules:
        box = ET.SubElement(root, tag("modules"))
        for name in modules:
            add(box, "module", name)
    if deps:
        box = ET.SubElement(root, tag("dependencies"))
        for item in deps:
            dep(box, *item)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

write("pom.xml", "plexus-compiler", None, (
    "plexus-compiler-api",
    "plexus-compiler-manager",
    "plexus-compilers/plexus-compiler-javac",
), None, "Plexus Compiler")
write("plexus-compiler-api/pom.xml", "plexus-compiler-api", "../pom.xml", None, (
    ("org.codehaus.plexus", "plexus-utils", "3.6.2"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
    ("org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3"),
), "Plexus Compiler Api")
write("plexus-compiler-manager/pom.xml", "plexus-compiler-manager", "../pom.xml", None, (
    ("org.codehaus.plexus", "plexus-compiler-api", "%{version}"),
    ("javax.inject", "javax.inject", "1"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
), "Plexus Compiler Manager")
write("plexus-compilers/plexus-compiler-javac/pom.xml", "plexus-compiler-javac", "../../pom.xml", None, (
    ("org.codehaus.plexus", "plexus-compiler-api", "%{version}"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2"),
    ("javax.inject", "javax.inject", "1"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
), "Plexus Compiler Javac")
PY
# Sisu loads @Named classes from this index. The indexer plugin is not packaged.
python - <<'PY'
import re
from pathlib import Path
modules = (
    "plexus-compiler-manager",
    "plexus-compilers/plexus-compiler-javac",
)
for module in modules:
    root = Path(module) / "src" / "main" / "java"
    names = []
    for path in sorted(root.rglob("*.java")):
        text = path.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//.*?$", "", text, flags=re.M)
        match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
        if not match or "@Named" not in text[:match.start()]:
            continue
        pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
        if pkg:
            names.append(pkg.group(1) + "." + match.group(1))
    if not names:
        continue
    dest = Path(module) / "src" / "main" / "resources" / "META-INF" / "sisu"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY

%files -f .mfiles
%doc LICENSE-2.0.txt LICENSE.MIT README.md
