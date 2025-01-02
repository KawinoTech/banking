const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  devServer: {
    host: '0.0.0.0',
    port: 8000, // Change this to your desired port if needed
    open: true, // Opens the browser automatically on start
  },
};