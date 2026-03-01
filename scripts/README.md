# Client Build Scripts

## patch-pom.py

Python script that properly merges Maven Central publishing configuration into OpenAPI-generated `pom.xml` files using XML ElementTree.

### Usage

```bash
python3 scripts/patch-pom.py <pom-path> <name> <description> [--legacy]
```

### Arguments

- `pom-path`: Path to the generated pom.xml file
- `name`: Project name (e.g., "Reborn API Client")
- `description`: Project description
- `--legacy`: Optional flag to add jackson-databind-nullable dependency for legacy clients

### What it does

1. **Updates metadata**: Sets proper name, description, and URL
2. **Replaces license**: Changes from Unlicense to Proprietary
3. **Updates SCM**: Points to the Reborn-API-Clients repository
4. **Updates developers**: Sets Reborn Team as developer
5. **Adds Maven Central plugins**:
   - `maven-gpg-plugin` for artifact signing
   - `central-publishing-maven-plugin` for Maven Central Portal
6. **Adds distributionManagement**: Configures Maven Central repository
7. **Adds dependencies** (if --legacy): Includes jackson-databind-nullable for Java 8 compatibility

### Why use XML ElementTree instead of sed?

- **Correct**: Properly parses and manipulates XML structure
- **Robust**: Handles variations in formatting and ordering
- **Maintainable**: Easy to understand and modify
- **Safe**: Validates XML structure during processing

### Example

```bash
# Regular client
python3 scripts/patch-pom.py \
  java-client/generated/pom.xml \
  "Reborn API Client" \
  "Java client for Reborn API"

# Legacy client (Java 8 compatible)
python3 scripts/patch-pom.py \
  java-legacy-client/generated/pom.xml \
  "Reborn API Client (Legacy)" \
  "Java client for Reborn API (Java 8 Compatible)" \
  --legacy
```
