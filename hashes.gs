// Cryptographic hash functions for use in Google Spreadsheets
// Use with =MD5(string)
// A string or cell (or concatenation of cells) can be provided
// Output in hex
// Released to the public domain

function MD2(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.MD2, s);
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i]+256) % 256;
    hexstr += ('0'+val.toString(16)).slice(-2);
  }
  return hexstr;
}
function MD5(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, s);
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i]+256) % 256;
    hexstr += ('0'+val.toString(16)).slice(-2);
  }
  return hexstr;
}
function SHA1(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_1, s)
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i]+256) % 256;
    hexstr += ('0'+val.toString(16)).slice(-2);
  }
  return hexstr;
}
function SHA256(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s);
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i]+256) % 256;
    hexstr += ('0'+val.toString(16)).slice(-2);
  }
  return hexstr;
}
function SHA384(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_384, s);
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i]+256) % 256;
    hexstr += ('0'+val.toString(16)).slice(-2);
  }
  return hexstr;
}
function SHA512(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_512, s);
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i]+256) % 256;
    hexstr += ('0'+val.toString(16)).slice(-2);
  }
  return hexstr;
}
