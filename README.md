# X-as-Code: Everything as Code

Website: http://x-as-code.useblocks.com/

## Usage

### Requirements

- [Docker](https://www.docker.com/get-started/) installed
- [Visual Studio Code](https://code.visualstudio.com/)

Or use GitHub Codespaces and just run the devcontainer

Make sure the ubCode environment variables are available as specified here: 

## Whats inside?

### Devcontainer

- ubcode
- graphviz
- CMake

### Demo Sphinx & Sphinx-Needs Project

### Demo C++ Project

Demonstrating Codelinks & Test-Reports

### Build Scripts

The project includes several build scripts to help you build different components:

| Script | Purpose | Description |
|--------|---------|-------------|
| `./scripts/build.sh` | **Full build** | Builds documentation, C++ executable, and runs unit tests |
| `./scripts/build_app.sh` | **C++ only** | Builds the C++ project and runs tests |
| `./scripts/build_doc.sh` | **Docs only** | Builds the Sphinx + Sphinx-Needs documentation |
| `./scripts/build_doc_ubc.sh` | **Docs with ubCode** | Builds the same documentation with ubCode (`ubc build html`) |
| `./scripts/check_build_parity.py` | **Build parity** | Checks that the Sphinx and the ubCode build have the same content |
| `./scripts/test_with_coverage.sh` | **Tests with coverage** | Builds C++ project, runs tests, and generates code coverage report |
| `./scripts/clean.sh` | **Clean** | Removes all build artifacts |
| `./scripts/run_http_server.sh` | **Server generated HTML files** | Opens a http server and servers the generated html files. With this method you can view the generated html files also when developing in Codespaces |


#### Quick Start

For first-time setup or complete rebuild:

```shell
./scripts/build.sh
```

#### Targeted Builds

Build only the C++ application and tests:

```shell
./scripts/build_app.sh
```

Build only the documentation:

```shell
./scripts/build_doc.sh
```

Run tests with code coverage:

```shell
./scripts/test_with_coverage.sh
```

This will generate a coverage report in `src/build/coverage_html/index.html`.

Clean all build artifacts:

```shell
./scripts/clean.sh
```

> **💡 Tip**: Use `./scripts/build.sh` for your first build, then use targeted scripts for faster incremental builds during development.

#### Dual Build: Sphinx and ubCode

The documentation is built from the same sources with two tools:

- **Sphinx** with Sphinx-Needs, configured in [docs/conf.py](docs/conf.py) and [docs/ubproject.toml](docs/ubproject.toml)
- **ubCode** (`ubc build html`), configured in the `[build.html]` section of [docs/ubproject.toml](docs/ubproject.toml)

```shell
./scripts/build_doc.sh                   # Sphinx -> docs/_build/html
./scripts/build_doc_ubc.sh               # ubCode -> docs/_build/ubc
uv run python scripts/check_build_parity.py
```

The ubCode build needs the `ubc` CLI (0.38.0 or newer). No license key is required: this is
a public open source repository, which ubCode detects from the git remote. Both builds
render PlantUML diagrams with the bundled jar in `docs/utils/`, so Java must be installed.

`check_build_parity.py` compares the content of both builds: pages, needs, page text,
needtables, needflow diagrams, toctrees and the sidebar. The themes differ (furo vs. the
ubCode theme), so markup and styling are not compared. Differences caused by known ubCode
limitations are listed in `KNOWN_DIFFERENCES` in the script and reported separately; any
other difference fails the check. The PR checks run both builds and this script.

#### Viewing created HTML pages

```shell
./scripts/run_http_server.sh
```

## Build with Codespaces

GitHub Codespaces provides a cloud-based development environment that comes pre-configured with all the tools needed for this project.

### Prerequisites

Before using Codespaces, you need to configure the required environment variables as Codespace secrets:

1. **Navigate to your GitHub user settings**
2. **Go to Settings → Code, planning, and automation → Codespaces**
3. **Add the following Codespace user secrets** and assign them to the correct repository:
   - `UBCODE_LICENSE_KEY`: Your ubCode license key
   - `UBCODE_LICENSE_USER`: Your registered email address

This is also described here in more detail: https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces

> **⚠️ Important**: These secrets are required for the ubCode extension to function properly. Without them, the extension is not working.

### Getting Started with Codespaces

1. **Open in Codespaces**
   - Navigate to the GitHub repository
   - Click the green **Code** button
   - Select the **Codespaces** tab
   - Click **Create codespace on main** (or any other branch you prefer)

2. **Automatic Setup**
   - The devcontainer will automatically install:
     - Python environment with uv package manager
     - Java (for PlantUML diagrams)
     - Graphviz (for diagram generation)
     - CMake (for C++ project builds)
     - ubCode VS Code extension
     - Python VS Code extension

3. **First Build**
   Once the codespace is ready, run the full build:
   ```shell
   ./scripts/build.sh
   ```

### What's Included in the Codespace

The devcontainer includes:
- **Base Image**: Ubuntu 24.04.2 LTS
- **Tools**: Git, curl, wget, and other essential CLI tools
- **Development Environment**: Pre-configured VS Code with extensions
- **Build Tools**: CMake, Graphviz, Java, uv for the complete toolchain

### Working with the Project

After the codespace starts:

1. **Build the documentation**:
   ```shell
   ./scripts/build_doc.sh
   ```

2. **Build the C++ project**:
   ```shell
   ./scripts/build_app.sh
   ```

3. **View the documentation**:
   - Open the generated HTML files using:
   ```shell
   "$BROWSER" docs/_build/html/index.html
   ```

4. **Clean build artifacts**:
   ```shell
   ./scripts/clean.sh
   ```

### Environment Variables

The following environment variables need to be available for the Codespace:

- `UBCODE_LICENSE_KEY`: Your ubCode license key (from secrets)
- `UBCODE_LICENSE_USER`: Your registered email (from secrets)

Please checkout [this page](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces#adding-a-secret) on how to add account specific secrets

With settings these variables the `ubcode.toml` file is not necessary anymore for the ubCode extension functionality.

### Alternative: Manual Environment Setup

If you prefer to set environment variables manually in the CLI (for testing or local development):

```shell
export UBCODE_LICENSE_KEY="your-license-key"
export UBCODE_LICENSE_USER="your-email@example.com"
```

### Customizing the Environment

The devcontainer configuration is defined in [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json). You can modify:

- **Additional tools**: Edit [`scripts/postCreateCommand.sh`](scripts/postCreateCommand.sh) to install more packages
- **VS Code extensions**: Add extensions to the `customizations.vscode.extensions` array
- **Environment variables**: Control installations by setting variables in the post-create script

### Benefits of Using Codespaces

- ✅ **Instant Setup**: No local dependencies required
- ✅ **Consistent Environment**: Same setup across all team members
- ✅ **Pre-configured Tools**: All necessary tools installed automatically
- ✅ **Cloud Resources**: Use GitHub's cloud infrastructure for builds
- ✅ **Persistent Storage**: Your work is automatically saved
- ✅ **Secure Secrets**: License keys managed through GitHub secrets

### Troubleshooting

If you encounter issues:

1. **Check environment variables**: Verify that `UBCODE_LICENSE_KEY` and `UBCODE_LICENSE_USER` are set:
   ```shell
   echo $UBCODE_LICENSE_KEY
   echo $UBCODE_LICENSE_USER
   ```

2. **Verify secrets**: Ensure the repository secrets are properly configured in GitHub

3. **Restart the codespace**: Sometimes a fresh start resolves configuration issues

4. **Check the post-create logs**: View the terminal output during setup

5. **Rebuild container**: Use Command Palette → "Codespaces: Rebuild Container"

> **💡 Tip**: Codespaces is perfect for quick contributions, testing, or when you don't want to set up the development environment locally. The automated secret management ensures a seamless experience.

## License

This project is licensed under the [MIT License](LICENSE).


