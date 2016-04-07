# Pilgrim 3

Pilgrim 3 provides a way to explore your proto files using a web browser. (proto version 3)
It uses protoc, the official compilation software and provides you access to files, messages services enums along with documentation to each type of object defined.

Pilgrim 3 is a simply python server that runs on you local machine, against your own protos and provides you with a clean web interface for exploring them. 

## Installation

```sh
pip install pilgrim3
```

## Usage

Generate your protos as normal. The only difference is that you should add a couple of flags to your protoc invoation.

* `--include_source_info` - This tells protoc to generate a serialized proto that includes documentation.
* `-o./proto_bundle` - The output file should be called `proto_bundle` and needs to live in the directory where you'll invoke pilgrim from.
* Run pilgrim3

```sh
protoc -Imy_protos --ruby_out=./app/protos --include_source_info -o./proto_bundle ./protos/my_protos.proto
```

The option for `-o` will output a serialized proto description of your protos. Very meta. The `--include_source_info` option tells protoc to include the source documentation. Pilgrim3 uses this output to provide you with explorable documentation.

### Running Pilgrim

Navigate over to the directory that has your `proto_bundle` file that you generated when ran `protoc`.

```sh
pilgrim3
```

Open pilgrim3 on your localhost at [http://localhost:9151](http://localhost:9151)

## Development

When developing pilgrim.

```sh
git clone git@github.com:opendoor-labs/pilgrim3.git
cd pilgrim3
git submodule update --init --recursive
```

You'll likely want to start the javascript builder. 

```sh
npm start
```

Head on over to an directory that has a proto\_bundle file and go for it. The `npm start` will re-build the Javascript as you go.
