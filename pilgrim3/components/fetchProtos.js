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
    state.byFile[file.name] = file;
    let thingName = `${file.package}`;

    mapFile(state, file, thingName);
  });
}

/**
 * Documentation for top level types (top level in file) are defined
 * at specific root indexes.  Nested types are not stored at the same
 * indexes, instead it is relative to the parent and at different indexes.
 *
 * It would be nice if it was recursive, but we have to parse file with one set of comment indexes,
 * and then handle nested messages separately.
 */
function mapFile(state, file, name) {
  let messageDocLoc = [4];
  let serviceDocLoc = [6];
  let enumDocLoc = [5];

  fileDocs(file, file.sourceCodeInfo.location);
  handleMessages(state, file, file.messageType, name, messageDocLoc);
  handleServices(state, file, file.service, name, serviceDocLoc);
  handleEnums(state, file, file.enumType, name, enumDocLoc);
}

function mapAllTheThings(state, file, thing, thingName, path) {
  let nestedMessageDocLog = path.concat(3);
  let nestedEnumDocLog = path.concat(4);

  handleMessages(state, file, thing.nestedType, thingName, nestedMessageDocLog);
  handleEnums(state, file, thing.enumType, thingName, nestedEnumDocLog);
}

function handleMessages(state, file, messages, thingName, thisPath) {
  state.byMessage = state.byMessage || {};
  forEach(messages, (msg, i) => {
    let thePath = thisPath.concat(i);
    let thisName = `${thingName}.${msg.name}`;
    state.byMessage[thisName] = msg;
    msg.fullName = thisName;
    msg.fileDescriptor = file;
    messageDocs(msg, thePath, pathDocs(thePath, file.sourceCodeInfo.location));
    mapAllTheThings(state, file, msg, thisName, thePath);
  });
}

function handleServices(state, file, services, thingName, thisPath) {
  state.byService = state.byService || {};

  forEach(services, (service, i) => {
    let thisName = `${thingName}.${service.name}`;
    let thePath = thisPath.concat(i);
    state.byService[thisName] = service;
    service.fullName = thisName;
    service.fileDescriptor = file;
    serviceDocs(service, thePath, pathDocs(thePath, file.sourceCodeInfo.location))
    mapAllTheThings(state, file, service, thisName, thePath);
  });
}

function handleEnums(state, file, enums, thingName, thisPath) {
  state.byEnum = state.byEnum || {};

  forEach(enums, (theEnum, i) => {
    let thisName = `${thingName}.${theEnum.name}`;
    let thePath = thisPath.concat(i);
    state.byEnum[thisName] = theEnum;
    theEnum.fullName = thisName;
    theEnum.fileDescriptor = file;
    enumDocs(theEnum, thePath, pathDocs(thePath, file.sourceCodeInfo.location));
    mapAllTheThings(state, file, theEnum, thisName, thePath);
  });
}

function pathDocs(path, items) {
  let matcher = matches(path);
  return filter(items, (loc) => {
    return matcher(loc.path);
  });
}

function fileDocs(file, locs) {
  let packageDocs = pathDocs([2], locs);
  let syntaxDocs = pathDocs([12], locs);

  attachDocs(file, syntaxDocs[0]);
  attachDocs(file, packageDocs[0]);
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
function messageDocs(msg, path, locs) {
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
  let fieldDocPath = path.concat(2);
  let oneOfDocPath = path.concat(8);

  attachDocs(msg, locs[0]);
  forEach(msg.field, (field, i) => {
    attachDocs(field, pathDocs(fieldDocPath.concat(i), locs)[0]);
  });

  forEach(msg.oneofDecl, (oneOf, i) => {
    attachDocs(oneOf, pathDocs(oneOfDocPath.concat(i), locs)[0]);
  });
}

function serviceDocs(service, path, locs) {
  let methodDocPath = path.concat(2);

  attachDocs(service, locs[0]);
  forEach(service.method, (meth, i) => {
    // Get rid of trailing . in the input type name
    meth.outputType = meth.outputType.substring(1);
    meth.inputType = meth.inputType.substring(1);
    attachDocs(meth, pathDocs(methodDocPath.concat(i), locs)[0]);
  });
}

function enumDocs(theEnum, path, locs) {
  let enumValueDocsPath = path.concat(2);

  attachDocs(theEnum, locs[0]);
  forEach(theEnum.value, (enumValue, i) => {
    attachDocs(enumValue, pathDocs(enumValueDocsPath.concat(i), locs)[0]);
  });
}
