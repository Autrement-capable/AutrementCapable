const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
  // devServer: {
  //   host: '0.0.0.0',
  //   port: 8080,
  //   allowedHosts: 'all',
  //   client: {
  //     webSocketURL: 'auto://0.0.0.0/ws', // avoids IP issues
  //   },
  //   hot: false,
  //   liveReload: false,
  // }
})
