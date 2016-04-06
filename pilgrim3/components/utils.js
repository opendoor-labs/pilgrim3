export function relativeName(fullName, fileDescriptor) {
  let pkg = fileDescriptor.package;
  let name = fullName.replace(/^\./, '');
  let idx = name.indexOf(pkg);
  let outputName;

  if (idx < 0) {
    return name;
  } else {
    outputName = name.substr(pkg.length);
    return outputName.replace(/^\./, '');
  }
}

