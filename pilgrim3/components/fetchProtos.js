import 'babel-polyfill';
import 'whatwg-fetch';
import {createFetch, base, accept, parseJSON} from 'http-client';
import {forEach, filter, matches} from 'lodash';

let fetchPromise;
let fieldDocLoc = 2;
let oneOfDocLoc = 8;

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
    // Add a leading . because that's how proto_bundle's work
    let thingName = `.${file.package}`;

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
  let messageDocPath = [4];
  let serviceDocPath = [6];
  let enumDocPath = [5];

  state.byMessage = state.byMessage || {};
  state.byEnum = state.byEnum || {};
  state.byService = state.byService || {};

  fileDocs(file, file.sourceCodeInfo.location);
  handleTypes(file.messageType, state.byMessage, file, name, messageDocPath, handleMessage((msg, path, locs) => {
    mapNestedObjects(state, file, msg, msg.fullName, path);
  }));

  handleTypes(file.enumType, state.byEnum, file, name, enumDocPath, handleEnum((msg, path, locs) => {}));

  handleTypes(file.service, state.byService, file, name, serviceDocPath, (service, path, locs) => {
    attachFieldDocs(service.method, path.concat(fieldDocLoc), locs);
  });
}

function mapNestedObjects(state, file, msg, name, path) {
  let nestedMessageDocLog = path.concat(3);
  let nestedEnumDocLog = path.concat(4);

  handleTypes(msg.nestedType, state.byMessage, file, name, nestedMessageDocLog,
      handleMessage((nestedMsg, path, locs) => {
    mapNestedObjects(state, file, nestedMsg, nestedMsg.fullName, path);
    nestedMsg.wrapper = msg
  }));

  handleTypes(msg.enumType, state.byEnum, file, name, nestedEnumDocLog, handleEnum((theEnum, path, locs) => {
    theEnum.wrapper = msg
  }));
}

/* Message specific handling */
function handleMessage(callback) {
  let toReturn = (msg, path, locs) => {
    attachFieldDocs(msg.oneofDecl, path.concat(oneOfDocLoc), locs);
    attachFieldDocs(msg.field, path.concat(fieldDocLoc), locs);
    callback(msg, path, locs)
  };

  return toReturn;
}

/* Enum specific handling */
function handleEnum(callback) {
  let toReturn = (theEnum, path, locs) => {
    attachFieldDocs(theEnum.value, path.concat(fieldDocLoc), locs);
    callback(theEnum, path, locs)
  };

  return toReturn;
}

function handleTypes(types, registry, file, name, path, callback) {
  forEach(types, (type, i) => {
    let theName = `${name}.${type.name}`;
    let thePath = path.concat(i);
    let locs = pathDocs(thePath, file.sourceCodeInfo.location);

    type.fullName = theName;
    type.fileDescriptor = file;
    registry[theName] = type;
    attachDocs(type, locs[0]);

    if (callback != undefined) {
      callback(type, thePath, locs);
    }
  });
}

// Docs
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


function attachFieldDocs(fields, path, locs) {
  forEach(fields, (field, i) => {
    attachDocs(field, pathDocs(path.concat(i), locs)[0]);
  });
}