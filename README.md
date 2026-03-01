# Reborn API Clients

This repository contains auto-generated clients for the Reborn API.

## Structure

- `java-client/` - Modern Java client using WebClient (Java 11+)
- `java-legacy-client/` - Legacy Java client using RestAssured (Java 8 compatible)
- `typescript-client/` - TypeScript/JavaScript client using Axios
- `scripts/` - Build scripts including POM patcher

## Publishing

Clients are automatically generated and published when:
- Client configuration files are modified
- Build scripts are updated
- Manually triggered via workflow_dispatch

The OpenAPI spec is downloaded from `https://api.smsh.sh/docs/openapi` during each workflow run.

### Java Clients

Published to Maven Central:
- `sh.smsh:reborn-api:<version>` - Modern client
- `sh.smsh:reborn-api:<version>-legacy` - Legacy client

### TypeScript Client

Published to NPM:
- `@smash-reborn/reborn-api-client`

## Development

Generated client code is placed directly in each client directory:
- `java-client/` - Contains all generated Java code
- `java-legacy-client/` - Contains all generated Java 8 code
- `typescript-client/` - Contains all generated TypeScript code

All generated files are gitignored except `.gitkeep` files.

## Secrets Required

The following GitHub secrets must be configured:

**For Java clients:**
- `GPG_PRIVATE_KEY` - Base64 encoded GPG private key
- `GPG_KEY_ID` - GPG key ID
- `MVN_CENTRAL_USERNAME` - Maven Central username
- `MVN_CENTRAL_PASSWORD` - Maven Central token

**For TypeScript client:**
- `NPM_TOKEN` - NPM authentication token

## License

Proprietary - See LICENSE file
