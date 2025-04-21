module.exports = {
  parser: 'vue-eslint-parser',
  root: true,
  env: {
    browser: true,
    node: true
  },
  'extends': [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    requireConfigFile: false,
    parser: "@babel/eslint-parser"
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
}