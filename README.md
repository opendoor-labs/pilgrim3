# Pilgrim 3

![Build status](https://api.travis-ci.org/opendoor-labs/pilgrim3.svg?branch=master)

Pilgrim 3 provides a way to explore your proto files using a web browser. (proto version 3)
It uses protoc, the official compilation software and provides you access to files, messages services enums along with documentation to each type of object defined.

Pilgrim 3 is a simply python server that runs on you local machine, against your own protos and provides you with a clean web interface for exploring them. 

## Installation

```sh
pip install pilgrim3
```

Or install from source. Clone the repo and cd into the directory.

```sh
python setup.py install
```

## Usage

### Proto3

Generate your protos as normal. The only difference is that you should add a couple of flags to your protoc invocation.

* `--include_source_info` - This tells protoc to generate a serialized proto that includes documentation.
* `-o./proto_bundle` - The output file should be called `proto_bundle` and needs to live in the directory where you'll invoke pilgrim from.
* Run pilgrim3

```sh
protoc -Imy_protos --include_source_info -o./proto_bundle ./protos/my_protos.proto
```

The option for `-o` will output a serialized proto description of your protos. Very meta. The `--include_source_info` option tells protoc to include the source documentation. Pilgrim3 uses this output to provide you with explorable documentation.

### Proto2

Basically the same as proto3 but you need to perform the compilation in two stages. 

Stage 1

Compile your protos as normal

```sh
protoc -Imy_protos ./protos/my_protos.proto
```

Stage 2

Compile your `proto_bundle` file for pilgrim to consume.

```sh
protoc -Imy_protos --include_source_info --descriptor_set_out=./proto_bundle ./protos/my_protos.proto
```

### Running Pilgrim

Navigate over to the directory that has your `proto_bundle` file that you generated when ran `protoc`.

```sh
pilgrim3 --proto-bundle=./protob_bundle
```

Open pilgrim3 on your localhost at [http://localhost:9151](http://localhost:9151)

## Development

Clone the repo:

```sh
git clone git@github.com:opendoor-labs/pilgrim3.git
cd pilgrim3
git submodule update --init --recursive
```

Start the javascript compiler from the project root:

```sh
npm start
```

The `npm start` will re-build the Javascript as you go.

Start a local server from the project root:
```sh
python -m pilgrim3.scripts.run pilgrim3/scripts/run.py --proto-bundle=path-to-proto-bundle

```

### Running Tests

```sh
./test/support/bin/compile # compile test protos
python setup.py test
```

There is a hello-world proto bundle to practice at at `dev/proto3/pilgrim-bundle`

## Dependencies

phantomjs
protoc
