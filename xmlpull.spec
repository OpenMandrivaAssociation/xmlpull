Name:		xmlpull
Version:	1.1.3.4c
Release:	1
Summary:	XML pull parser API
Group:		Development/Java
License:	Public Domain
URL:		http://www.xmlpull.org/
# Author git tree at the 1.1.3.4c API. The tree also ships prebuilt
# junit and sax jars under lib/. Those are removed from this archive.
%global commit abeaa4aa87b2625af70c32f658f44e11355fe568
Source0:	https://github.com/aslom/xmlpull-api-v1/archive/%{commit}.tar.gz#/xmlpull-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar

%description
XmlPull is the API that an XML pull parser implements. XStream's
default driver asks XmlPullParserFactory for one, and MXParser
registers itself as that implementation. Gradle's Groovy compiler
reaches this through XStream.

%prep
%autosetup -n xmlpull-api-v1-%{commit}

%build
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH=$JAVA_HOME/bin:$PATH
mkdir -p classes
find src/java/api -name '*.java' > sources.list
javac --release 8 -encoding UTF-8 -Xlint:-options -d classes @sources.list
jar cf %{name}.jar -C classes .
cat > %{name}.pom <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>xmlpull</groupId>
  <artifactId>xmlpull</artifactId>
  <version>%{version}</version>
  <name>XML Pull Parser API</name>
  <description>Public-domain XML pull parser API.</description>
  <url>http://www.xmlpull.org/</url>
  <licenses>
    <license>
      <name>Public Domain</name>
      <url>http://www.xmlpull.org/v1/download/unpacked/LICENSE.txt</url>
    </license>
  </licenses>
</project>
EOF

%check
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH=$JAVA_HOME/bin:$PATH
mkdir -p check
cat > check/Smoke.java <<'END'
import org.xmlpull.v1.XmlPullParser;
public class Smoke {
	public static void main(String[] args) {
		if (XmlPullParser.START_TAG != 2 || XmlPullParser.END_DOCUMENT != 1) {
			throw new AssertionError("event constants");
		}
		System.out.println("ok");
	}
}
END
javac --release 8 -encoding UTF-8 -Xlint:-options -cp %{name}.jar -d check check/Smoke.java
test "$(java -cp check:%{name}.jar Smoke)" = ok

%install
sysjar install --buildroot %{buildroot} \
	--artifact %{name}.pom:%{name}.jar \
	--file-name %{name} \
	--filelist .mfiles

%files -f .mfiles
%doc LICENSE.txt README.md
