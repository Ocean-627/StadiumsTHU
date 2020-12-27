module.exports = {
  devServer: {
    https: true,
    proxy: {
      "/": {
        target: "https://cbx.iterator-traits.com",
        ws: true,
        changeOrigin: true
      }
    }
  }
};
