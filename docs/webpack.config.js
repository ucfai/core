const path = require('path');

module.exports = {
  entry: "./webpack/entry.js",
  output: {
    path: path.resolve(__dirname__, "assets/scripts/"),
    filename: "bundle.js"
  },
  module: {
  }
};
