const path = require('path');

module.exports = {
    mode: 'development', // Set the mode to 'development' or 'production'
    entry: {
        // colocar todas as paginas aqui
        login: './src/pages/editor/Login/Login.js',
        dashboard: './src/pages/editor/Dashboard/Dashboard.js',
        pesquisaproducao: './src/pages/editor/PesquisaProducao/PesquisaProducao.js'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    },
    resolve: {
        fallback: {
            "fs": false,
            "path": false,
            "os": false
        }
    }
};
