const fs = require('fs');
const path = require('path');

const jsonList = [];
function printAllFiles(dir) {
  const filenames = fs.readdirSync(dir);
  filenames.forEach((filename) => {
    const fullPath = path.join(dir, filename);
    const stats = fs.statSync(fullPath);
    if (stats.isFile()) {
      jsonList.push(fullPath);
    } else if (stats.isDirectory()) {
      printAllFiles(fullPath);
    }
  });
}

// カレントディレクトリ
const dir = './static/';
printAllFiles(dir);

module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'starter',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Nuxt.js project' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        type: 'text/css',
        href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
      }
    ]
  },
  modules: [
    ['bootstrap-vue/nuxt']
  ],
  postcss: {
    plugins: {
      'postcss-custom-properties': {
        warnings: false
      }
    }
  },
  env: {
    jsonList: jsonList,
  },
  /*
  ** Global CSS
  */
  css: ['~/assets/css/sb-admin-2.css'],
  /*
  ** Add axios globally
  */
  build: {
    uglify: {
      uglifyOptions: {
        compress: false
      },
      cache: '/home/mac/nuxt-express-template/cache'
    },
  },
  router: {
    middleware: 'auth'
  }
//  build: {
//    vendor: ['axios'],
//    /*
//    ** Run ESLINT on save
//    */
//    extend (config, ctx) {
//      if (ctx.isClient) {
//        config.module.rules.push({
//          enforce: 'pre',
//          test: /\.(js|vue)$/,
//          loader: 'eslint-loader',
//          exclude: /(node_modules)/
//        })
//      }
//    }
//  },
//  router: {
//    middleware: 'i18n'
//  },
//  plugins: [
//    {src: '~plugins/i18n'}
//  ]
}
