module.exports = {
    devServer: {
        open: process.platform === 'darwin',
        host: '127.0.0.1',
        port: 8080, // CHANGE YOUR PORT HERE!
        https: true,
        hotOnly: false,
    },
}