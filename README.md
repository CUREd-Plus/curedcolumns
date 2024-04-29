# Metadata generator

CUREd+ metadata generator

# Installation

# Usage

# Development

## Emulated S3 bucket

https://s3ninja.net/

The test data should be mounted to `/home/sirius/data` 

```bash
docker run --volume /home/sirius/data:/tmp/sirius/data --publish 9444:9000 scireum/s3-ninja:latest
```
