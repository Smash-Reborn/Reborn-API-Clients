#!/usr/bin/env python3
"""
Patches the OpenAPI-generated pom.xml with Maven Central publishing configuration.
"""
import sys
from xml.etree import ElementTree as ET

def patch_pom(pom_path, name, description, is_legacy=False):
    # Register namespace to preserve xmlns
    ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')

    tree = ET.parse(pom_path)
    root = tree.getroot()

    ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}

    # Update metadata
    name_elem = root.find('maven:name', ns)
    if name_elem is not None:
        name_elem.text = name

    desc_elem = root.find('maven:description', ns)
    if desc_elem is not None:
        desc_elem.text = description

    url_elem = root.find('maven:url', ns)
    if url_elem is not None:
        url_elem.text = 'https://github.com/Smash-Reborn/Reborn-API-Clients'

    # Replace licenses
    licenses = root.find('maven:licenses', ns)
    if licenses is not None:
        root.remove(licenses)

    new_licenses = ET.Element('licenses')
    license_elem = ET.SubElement(new_licenses, 'license')
    ET.SubElement(license_elem, 'name').text = 'Proprietary'
    ET.SubElement(license_elem, 'url').text = 'https://github.com/Smash-Reborn/Reborn-API-Clients/blob/main/LICENSE'

    # Insert after description
    desc_index = list(root).index(desc_elem) + 1
    root.insert(desc_index, new_licenses)

    # Replace SCM
    scm = root.find('maven:scm', ns)
    if scm is not None:
        root.remove(scm)

    new_scm = ET.Element('scm')
    ET.SubElement(new_scm, 'connection').text = 'scm:git:git://github.com/Smash-Reborn/Reborn-API-Clients.git'
    ET.SubElement(new_scm, 'developerConnection').text = 'scm:git:ssh://github.com/Smash-Reborn/Reborn-API-Clients.git'
    ET.SubElement(new_scm, 'url').text = 'https://github.com/Smash-Reborn/Reborn-API-Clients'
    root.insert(desc_index + 1, new_scm)

    # Replace developers
    developers = root.find('maven:developers', ns)
    if developers is not None:
        root.remove(developers)

    new_developers = ET.Element('developers')
    developer = ET.SubElement(new_developers, 'developer')
    ET.SubElement(developer, 'id').text = 'reborn'
    ET.SubElement(developer, 'name').text = 'Reborn Team'
    ET.SubElement(developer, 'organization').text = 'Smash Reborn'
    ET.SubElement(developer, 'organizationUrl').text = 'https://github.com/Smash-Reborn'
    root.insert(desc_index + 2, new_developers)

    # Add GPG and Maven Central plugins to build/plugins
    build = root.find('maven:build', ns)
    if build is not None:
        plugins = build.find('maven:plugins', ns)
        if plugins is not None:
            # Add GPG plugin
            gpg_plugin = ET.Element('plugin')
            ET.SubElement(gpg_plugin, 'groupId').text = 'org.apache.maven.plugins'
            ET.SubElement(gpg_plugin, 'artifactId').text = 'maven-gpg-plugin'
            ET.SubElement(gpg_plugin, 'version').text = '3.1.0'

            executions = ET.SubElement(gpg_plugin, 'executions')
            execution = ET.SubElement(executions, 'execution')
            ET.SubElement(execution, 'id').text = 'sign-artifacts'
            ET.SubElement(execution, 'phase').text = 'verify'
            goals = ET.SubElement(execution, 'goals')
            ET.SubElement(goals, 'goal').text = 'sign'

            config = ET.SubElement(execution, 'configuration')
            gpg_args = ET.SubElement(config, 'gpgArguments')
            ET.SubElement(gpg_args, 'arg').text = '--pinentry-mode'
            ET.SubElement(gpg_args, 'arg').text = 'loopback'

            plugins.append(gpg_plugin)

            # Add Maven Central plugin
            central_plugin = ET.Element('plugin')
            ET.SubElement(central_plugin, 'groupId').text = 'org.sonatype.central'
            ET.SubElement(central_plugin, 'artifactId').text = 'central-publishing-maven-plugin'
            ET.SubElement(central_plugin, 'version').text = '0.4.0'
            ET.SubElement(central_plugin, 'extensions').text = 'true'

            plugin_config = ET.SubElement(central_plugin, 'configuration')
            ET.SubElement(plugin_config, 'publishingServerId').text = 'central'
            ET.SubElement(plugin_config, 'tokenAuth').text = 'true'
            ET.SubElement(plugin_config, 'autoPublish').text = 'true'

            plugins.append(central_plugin)

    # Add distributionManagement after build
    dist_mgmt = ET.Element('distributionManagement')
    snapshot_repo = ET.SubElement(dist_mgmt, 'snapshotRepository')
    ET.SubElement(snapshot_repo, 'id').text = 'central'
    ET.SubElement(snapshot_repo, 'url').text = 'https://central.sonatype.com/'

    build_index = list(root).index(build)
    root.insert(build_index + 1, dist_mgmt)

    # Add jackson-nullable dependency for legacy client
    if is_legacy:
        dependencies = root.find('maven:dependencies', ns)
        if dependencies is not None:
            jackson_dep = ET.Element('dependency')
            ET.SubElement(jackson_dep, 'groupId').text = 'org.openapitools'
            ET.SubElement(jackson_dep, 'artifactId').text = 'jackson-databind-nullable'
            ET.SubElement(jackson_dep, 'version').text = '0.2.6'
            dependencies.append(jackson_dep)

    # Write back with proper formatting
    tree.write(pom_path, encoding='utf-8', xml_declaration=True)
    print(f"✓ Patched {pom_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: patch-pom.py <pom-path> <name> <description> [--legacy]")
        sys.exit(1)

    pom_path = sys.argv[1]
    name = sys.argv[2]
    description = sys.argv[3]
    is_legacy = '--legacy' in sys.argv

    patch_pom(pom_path, name, description, is_legacy)
