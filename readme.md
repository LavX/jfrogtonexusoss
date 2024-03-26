
# JFrog to Nexus OSS Repository Migration Tool

This toolset is designed for migrating repositories from JFrog Artifactory to Nexus OSS. It automates the process of scanning, listing, and uploading packages between these two repository managers.

## Configuration

### `config.json`

Defines the repositories to be migrated with their names and types. Example:

```json
[
    {
      "name": "stable-yum-repos",
      "type": "rpm"
    },
    {
      "name": "stable-deb-repos",
      "type": "debian"
    },
    {
      "name": "my-maven-repos",
      "type": "maven"
    }
]
```

### `.env`

Stores environment variables for JFrog and Nexus credentials. Example:

```plaintext
JFROG_URL=your_jfrog_url
JFROG_USER=your_jfrog_user
JFROG_PASSWORD=your_jfrog_password
NEXUS_URL=your_nexus_url
NEXUS_USER=your_nexus_user
NEXUS_PASSWORD=your_nexus_password
```

### `.gitignore`

Specifies intentionally untracked files to ignore.

## Setup

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt` (ensure you have Python and pip installed).
3. Set up your `.env` file with the necessary JFrog and Nexus credentials.
4. Customize `config.json` with the repositories you intend to migrate.

## Running the Tool

To migrate repositories as configured in `config.json`, execute:

```bash
python migrate_repos.py
```

To perform a full scan of all repositories in the source JFrog instance and attempt migration, use:

```bash
python migrate_repos.py scanall
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

---

Laszlo A. Toth | [www.lavx.hu](http://www.lavx.hu) | lavx@lavx.hu
