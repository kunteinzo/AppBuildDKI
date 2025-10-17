# Building Android App on Server(Docker)

## Docker Required

## Usage

```
cd AppBuildDKI
docker build -t appbuild .
docker run -it --name appbuild -p 8000:8000 appbuild
```
