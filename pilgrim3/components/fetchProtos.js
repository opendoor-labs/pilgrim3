import 'babel-polyfill';
import 'whatwg-fetch';
import {createFetch, base, accept, parseJSON} from 'http-client';
import {forEach, filter, matches} from 'lodash';

let fetchPromise;

const fetchProtosFetch = createFetch(
    accept('application/json'),
    parseJSON()
);

export default function fetchProtos(state) {
  if (fetchPromise) return fetchPromise;

  fetchPromise = Promise.all([
    fetchProtosFetch('/local/proto-bundle').then((localResponse) => {
      handleFileSet(state, localResponse.jsonData);
    })
  ]);

  return fetchPromise;
}

function handleFileSet(state, fileset) {
  state.byFile = state.byFile || {};
  window.state = state;

  forEach(fileset.file, (file) => {
    fileDocs(file);
    state.byFile[file.name] = file;
    let thingName = `${file.package}`;

    mapAllTheThings(state, file, file, thingName, []);
  });
}

function mapAllTheThings(state, file, thing, thingName, path) {
  path = path || [];
  handleMessages(state, file, thing.messageType, thingName, path);
  handleMessages(state, file, thing.nestedType, thingName, path);
  handleServices(state, file, thing.service, thingName, path);
  handleEnums(state, file, thing.enumType, thingName, path);
}

function handleMessages(state, file, messages, thingName, path) {
  let thisPath = path.concat(4);

  state.byMessage = state.byMessage || {};
  forEach(messages, (msg, i) => {
    let thePath = thisPath.concat(i);
    let thisName = `${thingName}.${msg.name}`;
    state.byMessage[thisName] = msg;
    msg.fullName = thisName;
    msg.fileDescriptor = file;
    let docs = pathDocs(thePath, file.sourceCodeInfo.location);
    attachDocs(msg, docs[0]);
    messageDocs(msg, docs, thePath);
    mapAllTheThings(state, file, msg, thisName, thePath);
  });
}

function handleServices(state, file, services, thingName, path) {
  state.byService = state.byService || {};

  let thisPath = path.concat(6);

  forEach(services, (service, i) => {
    let thisName = `${thingName}.${service.name}`;
    let thePath = thisPath.concat(i);
    state.byService[thisName] = service;
    service.fullName = thisName;
    service.fileDescriptor = file;
    let docs = pathDocs(thePath, file.sourceCodeInfo.location)[0];
    attachDocs(service, docs);
    mapAllTheThings(state, file, service, thisName, thePath);
  });
}

function handleEnums(state, file, enums, thingName, path) {
  state.byEnum = state.byEnum || {};
  let thisPath = path.concat(5);

  forEach(enums, (theEnum, i) => {
    let thisName = `${thingName}.${theEnum.name}`;
    let thePath = thisPath.concat(i);
    state.byEnum[thisName] = theEnum;
    theEnum.fullName = thisName;
    theEnum.fileDescriptor = file;
    let docs = pathDocs(thePath, file.sourceCodeInfo.location)[0];
    mapAllTheThings(state, file, theEnum, thisName, thePath);
  });
}

function pathDocs(path, items) {
  let matcher = matches(path);
  return filter(items, (loc) => {
    return matcher(loc.path);
  });
}

function fileDocs(fd) {
  let packageDocs = pathDocs([2], fd.sourceCodeInfo.location);
  let syntaxDocs = pathDocs([12], fd.sourceCodeInfo.location);

  attachDocs(fd, syntaxDocs[0]);
  attachDocs(fd, packageDocs[0]);
}

function attachDocs(thing, docs) {
  if (!docs) return;
  let docString = thing.documentation || '';
  forEach(docs.leadingDetachedComments, (cmt) => {
    docString = `${docString}\n${cmt}`;
  });

  if (docs.leadingComments) {
    docString = `${docString}\n${docs.leadingComments}`;
  }

  forEach(docs.trailingComments, (cmt) => {
    docString = `${docString}\n${cmt}`;
  });

  if (docString) thing.documentation = docString;
}

// locs = local docs
function messageDocs(msg, locs, path) {
  // Each of these numbers come from the file descriptor google protobuf definition.
  // Since enums can have recursive messages which can have recursive enums etc, the location structure is like this:
  // location: [TokenType, TokenIndex].  The token index is simply to support multiple tokens inside of a scope, i.e.
  // message Foo {
  //   message Bar {
  //     enum Baz1 {
  //     }
  //     enum Baz2 {
  //     }
  //   }
  // }
  //
  // The location for Foo is [4, 0]
  // The location for Bar is [4, 0, 3, 0]
  // The location for Baz1 is [4, 0, 3, 0, 4, 0]
  // The location for Baz2 is [4, 0, 3, 0, 4, 1]
  //
  // NB: enums and messages share the same position... need to find out more
  let fieldsPath = path.concat(2);
  let nestedTypePath = path.concat(3);
  let enumTypePath = path.concat(4);
  let oneOfPath = path.concat(8);

  forEach(msg.field, (field, i) => {
    let docs = pathDocs(fieldsPath.concat(i), locs)[0];
    attachDocs(field, docs);
  });

  forEach(msg.nestedType, (nestedMsg, i) => {
    let docs = pathDocs(nestedTypePath.concat(i), locs)[0];
    attachDocs(nestedMsg, docs);
  });

  forEach(msg.enumType, (enumType, i) => {
    let docs = pathDocs(enumTypePath.concat(i), locs)[0];
    attachDocs(enumType, docs);
  });

  forEach(msg.oneofDecl, (oneOf, i) => {
    let docs = pathDocs(oneOfPath.concat(i), locs)[0];
    attachDocs(oneOf, docs);
  });
}

